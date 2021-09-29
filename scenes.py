from abc import ABC, abstractmethod
from typing import Optional
import inspect
import sys
import datetime

from request import Request
import entities
from state import STATE_RESPONSE_KEY
from answers import add_positive_answer
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

    def make_response(self, text, tts=None, card=None, state=None,
                      buttons=None, directives=None, application_state=None, user_state=None, user_problem=None,
                      problem_location=None, end_session=None):

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
        if user_problem is not None:
            webhook_response[STATE_RESPONSE_KEY]['user_problem'] = user_problem
        if problem_location is not None:
            webhook_response[STATE_RESPONSE_KEY]['problem_location'] = problem_location
        if state is not None:
            webhook_response[STATE_RESPONSE_KEY].update(state)
        return webhook_response


class Beginning(Scene):
    def reply(self, request: Request):
        last_inquiry = ''
        if request.report_state is not None:
            # вставить API вызов для проверки статуса
            last_inquiry = ('Статус вашей последней заявки... ')
        if last_inquiry != '':
            text = last_inquiry + 'Хотите оформить новую заявку или узнать больше о том, что я умею?'
        else:
            text = ('Здравствуйте! Я - помощник по проблемам с ЖКХ в вашем доме. \
                    Хотите оформить заявку или проверить статус?')
        return self.make_response(text)

    def handle_global_intents(self, request):
        if intents.YANDEX_HELP in request.intents or intents.LEARN_MORE in request.intents:
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
        return self.make_response(text)


class StartInquiry(Beginning):
    def reply(self, request: Request):
        text = add_positive_answer('Давайте оформим заявку. Где проблема: в доме или в квартире?')
        return self.make_response(text)

    def handle_local_intents(self, request: Request):
        if intents.CHOOSE_INQUIRY_LOCATION in request.intents:
            print('User selected location: ' + str(request.intents[intents.CHOOSE_INQUIRY_LOCATION]['slots']['location']['value']))
            location = entities.choose_location(request, intents.CHOOSE_INQUIRY_LOCATION)
            return InquiryLocationCollector(location)


class InquiryLocationCollector(Beginning):
    def __init__(self, location=None):
        self.location = location

    def reply(self, request: Request):
        text = add_positive_answer('А что случилось?')
        return self.make_response(text, problem_location=self.location)

    def handle_local_intents(self, request: Request):
        for intent in intents.APARTMENT_INTENTS:
            if intent['intent_name'] in request.intents and 'date_restriction' in intent.keys():
                if not _is_in_range(intent['date_restriction']):
                    return FailedInquiry('об этом можно сообщить только в период ' + str(intent['date_restriction']) + ".")
                else:
                    return InquiryAddressCollector(intent['intent_name'])
            elif intent['intent_name'] in request.intents and 'date_restriction' not in intent.keys():
                return InquiryAddressCollector(intent['intent_name'])


class InquiryAddressCollector(Beginning):
    def __init__(self, user_problem=None):
        self.user_problem = user_problem

    def reply(self, request: Request):
        text = add_positive_answer('Подскажете адрес?')
        return self.make_response(text, user_problem=self.user_problem)

    def handle_local_intents(self, request: Request):
        for entity in request.entities:
            if entity['type'] == intents.YANDEX_GEO:
                if 'street' in entity['value'].keys() and 'house_number' in entity['value'].keys():
                    return InquiryAccepted()


class InquiryAccepted(InquiryAddressCollector):
    def reply(self, request: Request):
        user_problem = request.user_problem
        # Вставить вызов API с регистрацией заявки и обновлением статуса в хранилище состояний
        text = ('Ваша заявка зарегистрирована. Спасибо за обращение! Хотите оформить еще одну заявку?')
        return self.make_response(text)

    def handle_local_intents(self, request: Request):
        if intents.YANDEX_CONFIRM in request.intents:
            print('User wants to create a new inquiry.')
            return StartInquiry()
        elif intents.YANDEX_REJECT in request.intents:
            return End()


class FailedInquiry(InquiryLocationCollector):
    def __init__(self, reason=None):
        self.reason = reason

    def reply(self, request: Request):
        text = 'Извините, но '
        response = text + self.reason + ' Хотите оформить другую заявку?'
        return self.make_response(response)

    def handle_local_intents(self, request: Request):
        if intents.YANDEX_CONFIRM in request.intents:
            print('User wants to create a new inquiry.')
            return StartInquiry()
        elif intents.YANDEX_REJECT in request.intents:
            return End()


class StartCheck(Beginning):
    def reply(self, request: Request):
        if request.report_state is not None:
            text = add_positive_answer('Давайте проверим вашу последнюю заявку под номером ' + str(request.session_state) + '. Хотите сообщить об еще одной проблеме?')
        # вставить вызов API
        # проверить статус, в зависимости от статуса составить ответ, обновить хранилище состояний, если нужно
        else:
            text = ('Пока что вы не оставляли никаких заявок. Хотите оставить свою первую заявку?')
        return self.make_response(text)

    def handle_local_intents(self, request: Request):
        if intents.YANDEX_CONFIRM in request.intents:
            print('User wants to create a new inquiry.')
            return StartInquiry()
        elif intents.YANDEX_REJECT in request.intents:
            return End()


class End(Beginning):
    def reply(self, request: Request):
        text = add_positive_answer('До новых встреч!')
        return self.make_response(text, end_session=True)


def _list_scenes():
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)
    return scenes


def _is_in_range(restriction):
    today = datetime.datetime.now()
    year = today.strftime("%Y")

    start_date = restriction.split('-')[0]
    finish_date = restriction.split('-')[1]

    start_month = start_date.split('/')[1]
    end_month = finish_date.split('/')[1]

    start_str = start_date + '/' + year
    if start_month > end_month:
        year = str(int(year) + 1)
    finish_str = finish_date + '/' + year

    start = datetime.datetime.strptime(start_str, "%d/%m/%Y")
    finish = datetime.datetime.strptime(finish_str, "%d/%m/%Y")
    return start <= today <= finish


SCENES = {
    scene.id(): scene for scene in _list_scenes()
}

DEFAULT_SCENE = Beginning