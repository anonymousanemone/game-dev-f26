"""A stateless Vertex AI Gemini adapter. Model receives JSON observations, no tools.

Standard library only. Authenticates with Google Application Default Credentials
(`gcloud auth application-default login`), the same credentials the course
starter's `setup_check --provider vertex` uses.
"""
import json
import os
from pathlib import Path
import time
import urllib.parse
import urllib.request

MAX_OUTPUT_TOKENS = 1024
TOKEN_URL = 'https://oauth2.googleapis.com/token'

BASE_PROMPT = '''You play Crocodiles. Return one JSON object with exactly move (-1 up, 0 still,
1 down), face (-1 left, 0 unchanged, 1 right), thrust (boolean), heka (boolean: hold
the magic key during the action), look (boolean). In spell31 face must be 0. Each
action lasts 0.1 simulation seconds. Thrust lands 0.0833s after initiation and
cooldown lasts 0.25s. Spear reach extends 15 world pixels along spear_direction
from tip. Align vertically with an approaching crocodile and thrust while the
spear reaches its snout or silhouette. You lose when health reaches 0. During tutorial "thrust",
thrust to begin. Movement speed is 390 world pixels/s. look reads the word of power
shown above the fight, as a player clicking it would; while you read, your other
controls are ignored for 1.0 s and the crocodiles keep coming. heka_word_glowing
says when that word glows. message is what the game last said; notes keeps what
you have read. Each crocodile also has dx_from_tip and dy_from_tip (its snout minus
the spear tip, world pixels), side (left or right of you) and seconds_to_bearer
(time until its snout reaches you at the speed it was seen moving; null until it
has been seen moving). in_reach, if present, is true when the spear's thrust would
touch that crocodile where it is now; it keeps moving before a thrust lands. memory, if supplied, lists what happened earlier in this
episode, oldest first: your thrusts and looks, crocodiles turned back, bites and
what the game said. The engine freezes while you decide. Earlier observations, if
supplied, are bounded history; use successive positions to estimate velocity.
Choose the action yourself. Do not provide prose or markdown. No tools are
available.'''

# Final tuned prompt selected by the student on 2026-11-04.
# Keep the pre-tuning control available for reproducible comparisons.
COMBAT_INSTRUCTION = '''Line up with approaching crocodiles by matching the spear tip's y level to the crocodile's snout y level (dy_from_tip near zero). Positive dy_from_tip means the crocodile is below your spear: move=1 moves down toward it. Negative dy_from_tip means it is above: move=-1 moves up toward it. Use move=0 once lined up; a movement action shifts you about 39 world pixels.
For each decision, choose the approaching crocodile with the smallest nonnegative
seconds_to_bearer; if none has an estimate, use the closest visible snout to the
bearer. Use that same target for facing, vertical alignment, timing and heka.
In spell32 face=-1 for a target on your left and face=1 for one on your right;
in spell31 keep face=0. Reassess the target on the next observation.
When attacking a red crocodile use heka=true; when attacking an ordinary
crocodile use heka=false. Heka on an ordinary crocodile loses the encounter.
Do not keep heka on indiscriminately after reading the word.
Estimate target velocity from successive visible snout positions and times.
Predict its snout position 5/60 seconds ahead, when the thrust lands, and compare
with the spear stroke at your chosen facing. Turning changes the tip position:
reflect tip.x about player_x if you turn. Thrust only when vertically aligned
and the predicted snout or silhouette will meet the spear stroke. When thrusting
hold move=0 to preserve alignment. If thrusting is already true, do not request
another thrust; use subsequent observations to wait for attack availability.
Reading with look costs 1.0 simulation seconds; avoid reading during an imminent
attack. No visible target: stay still with thrust=false and heka=false.'''
PROMPT = BASE_PROMPT + '\n' + COMBAT_INSTRUCTION

_token = {'value': None, 'expires': 0.0}


def request_payload(observation, history, memory=None):
    face_range = (-1, 1) if observation['both_sides'] else (0, 0)
    return {
        'systemInstruction': {'parts': [{'text': PROMPT}]},
        'contents': [{'role': 'user', 'parts': [
            {'text': json.dumps({'history': history, 'observation': observation,
                                 **({'memory': memory} if memory is not None else {})})}]}],
        'generationConfig': {
            'maxOutputTokens': MAX_OUTPUT_TOKENS,
            'responseMimeType': 'application/json',
            'responseSchema': {'type': 'OBJECT', 'properties': {
                'move': {'type': 'INTEGER', 'minimum': -1, 'maximum': 1},
                'face': {'type': 'INTEGER', 'minimum': face_range[0], 'maximum': face_range[1]},
                'thrust': {'type': 'BOOLEAN'}, 'heka': {'type': 'BOOLEAN'}, 'look': {'type': 'BOOLEAN'}},
                'required': ['move', 'face', 'thrust', 'heka', 'look'],
                'propertyOrdering': ['move', 'face', 'thrust', 'heka', 'look']}}}


def cost_reservation(observation, history, model, input_price, output_price, memory=None):
    payload = request_payload(observation, history, memory)
    # UTF-8 byte count bounds text tokens; extra allowance covers message framing.
    # Charge all input at the uncached price, and reserve the full output cap
    # (Gemini bills reasoning tokens as output and counts them against the cap).
    input_bound = (len(PROMPT.encode()) + len(payload['contents'][0]['parts'][0]['text'].encode())
                   + 1024)
    return (input_bound * input_price + MAX_OUTPUT_TOKENS * output_price) / 1_000_000


def credentials_path():
    configured = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if configured:
        return Path(configured)
    return Path.home()/'.config'/'gcloud'/'application_default_credentials.json'


def access_token(timeout):
    """Refresh an ADC user token; cached until five minutes before expiry."""
    if _token['value'] and time.time() < _token['expires']:
        return _token['value']
    path = credentials_path()
    if not path.exists():
        raise RuntimeError('No Google credentials; run gcloud auth application-default login.')
    credentials = json.loads(path.read_text())
    if credentials.get('type') != 'authorized_user':
        raise RuntimeError('Only authorized_user Application Default Credentials are supported.')
    body = urllib.parse.urlencode({'grant_type': 'refresh_token',
        'client_id': credentials['client_id'], 'client_secret': credentials['client_secret'],
        'refresh_token': credentials['refresh_token']}).encode()
    with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=timeout) as response:
        result = json.load(response)
    _token['value'] = result['access_token']
    _token['expires'] = time.time() + int(result.get('expires_in', 3600)) - 300
    return _token['value']


def endpoint(model):
    project = os.environ['GOOGLE_CLOUD_PROJECT']
    location = os.environ.get('GOOGLE_CLOUD_LOCATION') or 'global'
    host = 'aiplatform.googleapis.com' if location == 'global' else f'{location}-aiplatform.googleapis.com'
    return (f'https://{host}/v1/projects/{urllib.parse.quote(project)}/locations/'
            f'{urllib.parse.quote(location)}/publishers/google/models/{urllib.parse.quote(model)}:generateContent')


def choose(observation, history, model, timeout, memory=None):
    started = time.monotonic()
    token = access_token(timeout)
    request = urllib.request.Request(endpoint(model),
        data=json.dumps(request_payload(observation, history, memory)).encode(), headers={
            'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    remaining = max(.01, timeout - (time.monotonic() - started))
    with urllib.request.urlopen(request, timeout=remaining) as response:
        result = json.load(response)
    candidates = result.get('candidates') or [{}]
    candidate = candidates[0]
    text = ''.join(part.get('text', '') for part in candidate.get('content', {}).get('parts', [])
                   if not part.get('thought'))
    metadata = result.get('usageMetadata', {})
    response_tokens = metadata.get('candidatesTokenCount', 0)
    thought_tokens = metadata.get('thoughtsTokenCount', 0)
    usage = {'input_tokens': metadata.get('promptTokenCount', 0),
             # Reasoning tokens are billed at the output price.
             'output_tokens': response_tokens + thought_tokens,
             'response_tokens': response_tokens, 'thought_tokens': thought_tokens,
             'total_tokens': metadata.get('totalTokenCount'),
             'response_model': result.get('modelVersion'),
             'finish_reason': candidate.get('finishReason')}
    try:
        action = json.loads(text)
    except json.JSONDecodeError:
        action = None
    return action, usage, text, result.get('responseId')
