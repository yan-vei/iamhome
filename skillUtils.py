import intents
import datetime

def validate_address(street, house_number):
    address_details = ['дом','этаж', 'квартира', 'парадная', 'подъезд', 'квартирой', 'этаже', 'подъезде'
                       'доме', 'дома',  'подъезду', 'квартиры', 'подъезда', 'парадной', 'парадную', 'квартиру', 'этажом',
                       'дому']
    address_values = {}
    house_details = house_number.split(' ')
    token_index = 0
    if len(house_details) == 1:
        return {'дом': house_details[0]}
    elif len(house_details) == 2:
        if house_details[0].isdigit() and house_details[1].isdigit():
            return {'дом': house_details[0], 'квартира': house_details[1]}
        else:
            return {}
    while token_index < len(house_details):
        if token_index == 0:
            if house_details[token_index].isdigit() and not house_details[token_index+1].startswith('дом'):
                address_values['дом'] = house_details[token_index]
                token_index += 1
                continue
            elif house_details[token_index].startswith('дом') and house_details[token_index+1].isdigit():
                address_values['дом'] = house_details[token_index+1]
                token_index += 2
                continue
            elif house_details[token_index].isdigit() and house_details[token_index+1].startswith('дом'):
                address_values['дом'] = house_details[token_index]
                token_index += 2
                continue
            else:
                return {}
        if house_details[token_index].isdigit() and house_details[token_index+1] in address_details:
            address_values[house_details[token_index+1]] = house_details[token_index]
        elif house_details[token_index+1].isdigit() and house_details[token_index] in address_details:
            address_values[house_details[token_index]] = house_details[token_index+1]
        else:
            return {}
        token_index += 2
    address_values['улица'] = street
    return address_values


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


def getIntentLocation(intent_name):
    for intent in intents.APARTMENT_INTENTS:
        if intent_name == intent['intent_name']:
            return intent['location']


def suggestTopIntents(location):
    suggested_intents = []
    top = []

    if location == 'Location.APARTMENT':
        top = intents.TOP_APARTMENT_INTENTS
        print(top)
        all_intents = intents.APARTMENT_INTENTS
    elif location == 'Location.HOUSE':
        top = intents.TOP_HOUSE_INTENTS
        all_intents = intents.HOUSE_INTENTS

    for top_intent in top:
        for intent in all_intents:
            if top_intent == intent['intent_name']:
                suggested_intents.append(intent['informal_name'])
                break

    if suggested_intents != []:
        return suggested_intents
    return None