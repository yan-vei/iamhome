# Базовые интенты
CREATE_INQUIRY = 'createInquiry'
CHECK_INQUIRY = 'checkInquiry'
LEARN_MORE = 'learnMore'

YANDEX_HELP = 'YANDEX.HELP'
YANDEX_CONFIRM = 'YANDEX.CONFIRM'
YANDEX_REJECT = 'YANDEX.REJECT'
YANDEX_NUMBER = 'YANDEX.NUMBER'

# Базовые сущности
YANDEX_GEO = 'YANDEX.GEO'

# Интенты для оформления заявки
CHOOSE_INQUIRY_LOCATION = 'chooseInquiryLocation'

# Интенты по категориям проблем
APARTMENT_INTENTS = [{'intent_name': 'lowTempApartment',  # Низкая температура в отапливаемом помещении
                    'category_id': 1,
                    'subcategory_id': 1,
                    'date_restriction': '15/09-12/05',
                    'location': 2},
                   {'intent_name': 'highTempApartment',  # Высокая температура в отапливаемом помещении
                    'category_id': 1,
                    'subcategory_id': 2,
                    'date_restriction': '15/09-12/05',
                    'location': 2},
                   {'intent_name': 'noColdWaterApartment',  # Отсутствие холодной воды
                    'category_id': 2,
                    'subcategory_id': 1,
                    'location': 2},
                   {'intent_name': 'noHotWaterApartment',  # Отсутствие горячей воды
                    'category_id': 2,
                    'subcategory_id': 2,
                    'location': 2},
                   {'intent_name': 'weakHotPressureApartment',  # Слабый напор горячей воды
                    'category_id': 2,
                    'subcategory_id': 3,
                    'location': 2},
                   {'intent_name': 'weakColdPressureApartment',  # Слабый напор холодной воды
                    'category_id': 2,
                    'subcategory_id': 4,
                    'location': 2},
                   {'intent_name': 'badQualityHotApartment',  # Плохое качество горячей воды
                    'category_id': 2,
                    'subcategory_id': 5,
                    'location': 2},
                   {'intent_name': 'badQualityColdApartment',  # Плохое качество холодной воды
                    'category_id': 2,
                    'subcategory_id': 6,
                    'location': 2},
                   {'intent_name': 'brokenSewageApartment',  # Неисправность канализации
                    'category_id': 3,
                    'subcategory_id': 1,
                    'location': 2},
                   {'intent_name': 'brokenVentilationApartment',  # Неисправность системы вентиляции
                    'category_id': 4,
                    'subcategory_id': 1,
                    'location': 2},
                    {'intent_name': 'leakingPipeApartment',     # Ненадлежащее содержание трубопроводов и элементов системы водоснабжения, являющихся общедомовым имуществом
                    'category_id': 3,
                    'subcategory_id': 7,
                    'location': 2},
                    {'intent_name': 'damagedRadiatorApart',     # Повреждение запорной арматуры (вентиль, кран), стояка центрального отопления
                    'category_id': 4,
                    'subcategory_id': 3,
                    'location': 2
                    }
                   ]

# LOCATION CODES:
# UNKNOWN = 1
# APARTMENT = 2
# HOUSE = 3
# ENTRANCE = 4