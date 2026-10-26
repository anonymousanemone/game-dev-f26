"""A stateless Responses API adapter. Model receives JSON observations, no tools."""
import json
import os
import urllib.request

MAX_OUTPUT_TOKENS = 1024

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


def request_payload(observation, history, model):
    return {'model': model, 'instructions': PROMPT,
               'input': json.dumps({'history': history, 'observation': observation}),
               'max_output_tokens': MAX_OUTPUT_TOKENS, 'store': False,
               'text': {'format': {'type': 'json_schema', 'name': 'crocodile_action', 'strict': True,
                   'schema': {'type': 'object', 'properties': {
                       'move': {'type': 'integer', 'enum': [-1, 0, 1]},
                       'face': {'type': 'integer', 'enum': [-1, 0, 1] if observation['both_sides'] else [0]},
                       'thrust': {'type': 'boolean'}, 'heka': {'type': 'boolean'}},
                       'required': ['move', 'face', 'thrust', 'heka'], 'additionalProperties': False}}}}


def cost_reservation(observation, history, model, input_price, output_price):
    payload = request_payload(observation, history, model)
    # UTF-8 byte count bounds text tokens; extra allowance covers message framing.
    # Charge all input at the uncached price, and reserve the full output cap.
    input_bound = len(payload['instructions'].encode()) + len(payload['input'].encode()) + 1024
    return (input_bound * input_price + MAX_OUTPUT_TOKENS * output_price) / 1_000_000


def choose(observation, history, model, timeout):
    payload = request_payload(observation, history, model)
    request = urllib.request.Request('https://api.openai.com/v1/responses',
        data=json.dumps(payload).encode(), headers={
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
            'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    text = ''.join(content.get('text', '') for item in result.get('output', [])
                   if item.get('type') == 'message' for content in item.get('content', [])
                   if content.get('type') == 'output_text')
    usage = result.get('usage', {})
    usage['response_model'] = result.get('model')
    usage['response_status'] = result.get('status')
    try:
        action = json.loads(text)
    except json.JSONDecodeError:
        action = None
    return action, usage, text, result.get('id')
