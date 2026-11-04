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

PROMPT = '''You play Crocodiles. Return one JSON object with exactly move (-1 up, 0 still,
1 down), face (-1 left, 0 unchanged, 1 right), thrust (boolean), heka (boolean).
In spell31 face must be 0. Each action lasts 0.1 simulation seconds. Thrust lands
0.0833s after initiation and cooldown lasts 0.25s. Spear reach extends 15 world
pixels along spear_direction from tip. Align vertically with an approaching
crocodile and thrust while the spear reaches its snout or silhouette. Hold heka
only for red crocodiles; heka against an ordinary crocodile loses. Three bites
lose. Letting a crocodile escape after heka activates loses. During tutorial
"thrust", thrust to begin. Movement speed is 390 world pixels/s. The engine
freezes while you decide. Earlier observations, if supplied, are bounded history;
use successive positions to estimate velocity. Choose the action yourself.
Do not provide prose or markdown. No tools are available.'''

_token = {'value': None, 'expires': 0.0}


def request_payload(observation, history):
    face_range = (-1, 1) if observation['both_sides'] else (0, 0)
    return {
        'systemInstruction': {'parts': [{'text': PROMPT}]},
        'contents': [{'role': 'user', 'parts': [
            {'text': json.dumps({'history': history, 'observation': observation})}]}],
        'generationConfig': {
            'maxOutputTokens': MAX_OUTPUT_TOKENS,
            'responseMimeType': 'application/json',
            'responseSchema': {'type': 'OBJECT', 'properties': {
                'move': {'type': 'INTEGER', 'minimum': -1, 'maximum': 1},
                'face': {'type': 'INTEGER', 'minimum': face_range[0], 'maximum': face_range[1]},
                'thrust': {'type': 'BOOLEAN'}, 'heka': {'type': 'BOOLEAN'}},
                'required': ['move', 'face', 'thrust', 'heka'],
                'propertyOrdering': ['move', 'face', 'thrust', 'heka']}}}


def cost_reservation(observation, history, model, input_price, output_price):
    payload = request_payload(observation, history)
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


def choose(observation, history, model, timeout):
    started = time.monotonic()
    token = access_token(timeout)
    request = urllib.request.Request(endpoint(model),
        data=json.dumps(request_payload(observation, history)).encode(), headers={
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
