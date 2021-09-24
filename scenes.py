from abc import ABC, abstractmethod
from typing import Optional
import inspect
import sys

from request import Request
from state import STATE_RESPONSE_KEY
import intents

class Scene(ABC):

    @classmethod
    def id(cls):
        return cls.__name__

    """Генерация ответа сцены"""
    @abstractmethod
    def reply(self, request):
        raise NotImplementedError()

    """Проверка перехода к новой сцене"""
    def move(self, request: Request):
        next_scene = self.handle_local_intents(request)
        if next_scene is None:
            next_scene = self.handle_global_intents(request)
        return next_scene

    @abstractmethod
    def handle_global_intents(self):
        raise NotImplementedError()

    @abstractmethod
    def handle_local_intents(request: Request) -> Optional[str]:
        raise NotImplementedError()

    def fallback(self, request: Request):
        return self.make_response('Извините, я вас не поняла. Пожалуйста, попробуйте повторить ваш ответ.')

    def make_response(self, text, tts=None, card=None, state=None, buttons=None, directives=None):
        response = {
            'text': text,
            'tts': tts if tts is not None else text,
        }
        if card is not None:
            response['card'] = card
        if buttons is not None:
            response['buttons'] = buttons
        if directives is not None:
            response['directives'] = directives
        webhook_response = {
            'response': response,
            'version': '1.0',
            STATE_RESPONSE_KEY: {
                'scene': self.id(),
            },
        }
        if state is not None:
            webhook_response[STATE_RESPONSE_KEY].update(state)
        return webhook_response


def GenericScene(Scene):
    def handle_global_intents(self, request):
        if intents.CREATE_INQUIRY in request.intents:
            text = ('Хорошо, давайте оформим заявку. Где проблема: в доме или в подъезде?')
            return self.make_response(text)
        elif intents.CHECK_INQUIRY in request.intents:
            text = ('Хорошо, давайте проверим вашу последнюю заявку...')
            return self.make_response(text)


class Greeting(GenericScene):
    def reply(self, request: Request):
        text = ('Здравствуйте! Я - помощник по проблемам с ЖКХ в вашем доме. \
Хотите оформить заявку или проверить статус?')
        return self.make_response(text)


def _list_scenes():
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)
    return scenes


SCENES = {
    scene.id(): scene for scene in _list_scenes()
}

DEFAULT_SCENE = Greeting