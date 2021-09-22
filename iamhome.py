import json

from state import STATE_REQUEST_KEY
from scenes import SCENES, DEFAULT_SCENE
from request import Request


def handler(event, context):
    print('Incoming request: ' + json.dumps(event))
    request = Request(event)
    current_scene_id = event.get('state', {}).get(STATE_REQUEST_KEY, {}).get('scene')
    if current_scene_id is None:
        return DEFAULT_SCENE().reply(request)
