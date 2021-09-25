from abc import ABC, abstractmethod
from typing import Optional
import inspect
import sys
import enum

from request import Request
from state import STATE_RESPONSE_KEY
import intents


# Entities
class Location(enum.Enum):
    UNKNOWN = 1
    APARTMENT = 2
    HOUSE = 3
    ENTRANCE = 4

    @classmethod
    def from_request(cls, request: Request, intent_name: str):
        slot = request.intents[intent_name]['slots']['location']['value']
        if slot == 'apartment':
            return cls.APARTMENT
        elif slot == 'house':
            return cls.HOUSE
        elif slot == 'entrance':
            return cls.ENTRANCE
        else:
            return cls.UNKNOWN


# Выбор локации, по которой обращается пользователь
def choose_inquiry_location(request: Request, intent_name: str):
    location = Location.from_request(request, intent_name)
    if location == Location.HOUSE:
        return HouseInquiry()
    elif location == Location.APARTMENT:
        return ApartmentInquiry()
    elif location == Location.ENTRANCE:
        return EntranceInquiry()


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

    def make_response(self, text, tts=None, card=None, state=None,
                      buttons=None, directives=None, application_state=None, user_state=None, end_session=None):
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
        if end_session is not None:
            response['end_session'] = end_session

        webhook_response = {
            'response': response,
            'version': '1.0',
            STATE_RESPONSE_KEY: {
                'scene': self.id(),
            },
        }
        if user_state is not None:
            webhook_response['user_state_update'] = user_state
        if application_state is not None:
            webhook_response['application_state'] = application_state
        if state is not None:
            webhook_response[STATE_RESPONSE_KEY].update(state)
        return webhook_response


class Beginning(Scene):
    def reply(self, request: Request):
        text = ('Здравствуйте! Я - помощник по проблемам с ЖКХ в вашем доме. \
Хотите оформить заявку или проверить статус?')
        return self.make_response(text)

    def handle_global_intents(self, request):
        if intents.YANDEX_HELP in request.intents:
            print('User requested help.')
            return Help()

    def handle_local_intents(self, request: Request):
        if intents.CREATE_INQUIRY in request.intents:
            print('User wants to create an inquiry.')
            return StartInquiry()
        elif intents.CHECK_INQUIRY in request.intents:
            print('User wants to check inquiry.')
            return StartCheck()


class Help(Beginning):
    def reply(self, request: Request):
        text = ('Давайте я подскажу вам, что я могу сделать. \
                    Например, я могу оформить заявку о засорившемся мусоропроводе, или, \
                    если вы уже создали заявку, я могу ее проверить. Хотите оформить заявку или проверить статус?')
        return self.make_response(text, application_state={'report_id' : 1})

    def handle_local_intents(self, request: Request):
        pass


class StartInquiry(Beginning):
    def reply(self, request: Request):
        text = ('Хорошо, давайте оформим заявку. Где проблема: в доме или в квартире?')
        return self.make_response(text)

    def handle_local_intents(self, request: Request):
        if intents.CHOOSE_INQUIRY_LOCATION in request.intents:
            print('User selected location: ' + str(request.intents[intents.CHOOSE_INQUIRY_LOCATION]['slots']['location']['value']))
            return choose_inquiry_location(request, intents.CHOOSE_INQUIRY_LOCATION)


class GenericInquiry(Beginning):
    def reply(self, request: Request):
        text = ('Записала. А что случилось?')
        return self.make_response(text)


class HouseInquiry(GenericInquiry):
    def handle_local_intents(self, request: Request):
        pass


class ApartmentInquiry(GenericInquiry):
    def handle_local_intents(self, request: Request):
        for intent in intents.APARTMENT_INTENTS:
            if intent['intent_name'] in request.intents:
                return DetailsCollector()


class EntranceInquiry(GenericInquiry):
    def handle_local_intents(self, request: Request):
        pass


class DetailsCollector(Beginning):
    def reply(self, request: Request):
        text = ('Поняла вас. Подскажете адрес?')
        return self.make_response(text)

    def handle_local_intents(self, request: Request):
        if request.requested_entities != {}:
            print(request.requested_entities)


class StartCheck(Beginning):
    def reply(self, request: Request):
        if request.session_state is not None:
            text = ('Хорошо, давайте проверим вашу последнюю заявку под номером ' + request.session_state)
            return self.make_response(text)
        else:
            text = ('Пока что вы не оставляли никаких заявок. Хотите оставить свою первую заявку?')
            return self.make_response(text)

    def handle_local_intents(self, request: Request):
        pass


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

DEFAULT_SCENE = Beginning