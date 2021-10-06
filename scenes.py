from abc import ABC, abstractmethod
from typing import Optional
import inspect
import sys

from request import Request
import entities
import skillUtils
from state import STATE_RESPONSE_KEY
from answers import add_positive_answer
import intents

from InquiryApi import InquiryApi


def handle_buttons(*args):
    if args is None:
        return None
    buttons = []
    for button in args:
        buttons.append({"title": button, "hide": True})
    return buttons


def handle_problem(intent_name=None, location=None, address=None, floor=None, ap_number=None):
    problem = {}
    if intent_name is not None:
        problem['intent_name'] = intent_name
    if location is not None:
        problem['location'] = location
    if address is not None:
        problem['address'] = address
    if floor is not None:
        problem['floor'] = floor
    if ap_number is not None:
        problem['apartment_number'] = ap_number
    return problem


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

    def fallback(self, request: Request, fb_problem=None):
        return self.make_response('Извините, я Вас не поняла. Пожалуйста, попробуйте повторить ваш ответ.', problem_state=fb_problem)

    def make_response(self, text, tts=None, card=None, state=None,
                      buttons=None, directives=None, application_state=None, user_state=None,
                      end_session=None, problem_state=None):

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
        if problem_state is not None:
            webhook_response[STATE_RESPONSE_KEY]['problem'] = problem_state
        return webhook_response


class Beginning(Scene):
    def reply(self, request: Request):
        last_inquiry = ''
        if request.report_state is not None:
            if InquiryApi.inquiry_receive(request.report_state) == 4:
                last_inquiry = ('Статус вашей последней заявки - выполнена.')
            else:
                last_inquiry = ('Статус вашей последней заявки - обработана.')
        if last_inquiry != '':
            text = last_inquiry + 'Хотите оформить новую заявку или узнать больше о том, что я умею?'
            return self.make_response(text, buttons=handle_buttons("Оформить заявку", "Проверить статус"), application_state={})
        else:
            text = ('Здравствуйте! Я - помощник по проблемам с ЖКХ в вашем доме. \
                    Хотите оформить заявку или проверить статус?')
            return self.make_response(text, buttons=handle_buttons("Оформить заявку", "Проверить статус"))

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
        return self.make_response(text, buttons=handle_buttons("Оформить заявку", "Проверить статус"))


class StartInquiry(Beginning):
    def reply(self, request: Request):
        text = add_positive_answer('Давайте оформим заявку. Где проблема: в доме или в квартире?')
        return self.make_response(text, buttons=handle_buttons("В доме", "В квартире"))

    def handle_local_intents(self, request: Request):
        if intents.CHOOSE_INQUIRY_LOCATION in request.intents:
            print('User selected location: ' + str(request.intents[intents.CHOOSE_INQUIRY_LOCATION]['slots']['location']['value']))
            problem = handle_problem(location=entities.choose_location(request, intents.CHOOSE_INQUIRY_LOCATION))
            return InquiryLocationCollector(problem)


class InquiryLocationCollector(Beginning):
    def __init__(self, problem=None):
        self.problem = problem

    def reply(self, request: Request):
        text = add_positive_answer('А что случилось?')
        top_intents = skillUtils.suggestTopIntents(self.problem['location'])
        if top_intents != None:
            buttons = top_intents
        return self.make_response(text, problem_state=handle_problem(location=self.problem['location']), buttons=handle_buttons(buttons[0], buttons[1], buttons[2], buttons[3]))

    def handle_local_intents(self, request: Request):
        # Выбрать подходящий массив с интентами для поиска в зависимости от локации
        location = request.problem_location
        print('location fetched ' + str(location))
        if location == 'Location.APARTMENT':
            lookup_intents = intents.APARTMENT_INTENTS
        elif location == 'Location.HOUSE':
            lookup_intents = intents.HOUSE_INTENTS

        # lookup_intents = intents.APARTMENT_INTENTS if location == 'Location.APARTMENT' else intents.HOUSE_INTENTS

        for intent in lookup_intents:
            if intent['intent_name'] in request.intents and 'date_restriction' in intent.keys():
                if not skillUtils._is_in_range(intent['date_restriction']):
                    return FailedInquiry('об этом можно сообщить только в период ' + str(intent['date_restriction']) + ".")
                else:
                    return InquiryAddressCollector(handle_problem(location=location, intent_name=intent['intent_name']))
            elif intent['intent_name'] in request.intents and 'date_restriction' not in intent.keys():
                return InquiryAddressCollector(handle_problem(location=location, intent_name=intent['intent_name']))



class InquiryAddressCollector(Beginning):
    def __init__(self, problem=None):
        self.problem = problem

    def reply(self, request: Request):
        text = add_positive_answer('Подскажете адрес?')
        return self.make_response(text, problem_state=self.problem)

    def handle_local_intents(self, request: Request):
        location = request.problem_location
        intent_name = request.intent_name
        for entity in request.entities:
            if entity['type'] == intents.YANDEX_GEO:
                if 'street' in entity['value'].keys() and 'house_number' in entity['value'].keys():
                    address = skillUtils.validate_address(entity['value']['street'], entity['value']['house_number'])
                    problem_address = {'street': entity['value']['street'],
                                       'house_number': entity['value']['house_number']
                                       }
                    self.problem = handle_problem(location=location, intent_name=intent_name, address=problem_address)

                    if location == 'Location.APARTMENT':
                        if 'квартира' not in address.keys():
                            return InquiryGetApartment(self.problem)
                        else:
                            return InquiryAccepted(self.problem)
                    elif location == 'Location.HOUSE':
                        if 'этаж' not in address.keys():
                            return InquiryGetFloor(self.problem)
                        else:
                            return InquiryAccepted(self.problem)
                    else:
                        if address != {}:
                            return InquiryAccepted(self.problem)


class InquiryGetApartment(InquiryAddressCollector):
    def reply(self, request: Request):
        intent_name = request.intent_name
        text = ('Не могли бы Вы подсказать номер квартиры?')
        return self.make_response(text, problem_state=self.problem)

    def handle_local_intents(self, request: Request):
        self.problem = handle_problem(location=request.problem_location, intent_name=request.intent_name,
                                      address=request.problem_address)
        for entity in request.entities:
            if entity['type'] == intents.YANDEX_NUMBER:
                self.problem['apartment_number'] = entity.get('value', 0)
                return InquiryAccepted(self.problem)


class InquiryGetFloor(InquiryAddressCollector):
    def reply(self, request: Request):
        intent_name = request.intent_name
        text = ('Хотите уточнить этаж?')
        return self.make_response(text, problem_state=self.problem)

    def handle_local_intents(self, request: Request):
        self.problem = handle_problem(location=request.problem_location, intent_name=request.intent_name,
                                      address=request.problem_address)
        for entity in request.entities:
            if entity['type'] == intents.YANDEX_NUMBER:
                print('User added the floor.')
                self.problem['floor'] = entity['value']
                return InquiryAccepted(self.problem)
        if intents.YANDEX_CONFIRM in request.intents:
            return InquiryGetFloorConfirmation(self.problem)
        elif intents.YANDEX_REJECT in request.intents:
            return InquiryAccepted(self.problem)


class InquiryGetFloorConfirmation(InquiryGetFloor):
    def reply(self, request: Request):
        intent_name = request.intent_name
        text = add_positive_answer('Какой этаж?')
        return self.make_response(text, problem_state=self.problem)

    def handle_local_intents(self, request: Request):
        self.problem = handle_problem(location=request.problem_location, intent_name=request.intent_name,
                                      address=request.problem_address)
        for entity in request.entities:
            if entity['type'] == intents.YANDEX_NUMBER:
                self.problem['floor'] = entity['value']
                print('User added the floor.')
                return InquiryAccepted(self.problem)


class InquiryAccepted(InquiryAddressCollector):

    def reply(self, request: Request):
        # Регистрация заявки с помощью вызова класса InquiryApi
        inquiry_id = InquiryApi.inquiry_make(self.problem)
        text = ('Ваша заявка зарегистрирована. Спасибо за обращение! Хотите оформить еще одну заявку?')
        return self.make_response(text, buttons=handle_buttons("Да", "Нет"), application_state={'report_id': inquiry_id})

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
            text = ('Давайте проверим вашу последнюю заявку под номером.' + str(request.report_state) + '. Хотите сообщить об еще одной проблеме?')
            if InquiryApi.inquiry_receive(1) == 4:
                return self.make_response(text, application_state={})  # обнуляем хранилище
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


SCENES = {
    scene.id(): scene for scene in _list_scenes()
}

DEFAULT_SCENE = Beginning