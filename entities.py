from request import Request
import enum

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

def choose_location(request: Request, intent_name: str):
    location = Location.from_request(request, intent_name)
    return location

