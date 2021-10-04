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
                    'date_restriction': '15/10-12/05',
                    'location': 2},
                   {'intent_name': 'highTempApartment',  # Высокая температура в отапливаемом помещении
                    'category_id': 1,
                    'subcategory_id': 2,
                    'date_restriction': '15/10-12/05',
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

HOUSE_INTENTS = \
    [
        {'intent_name': 'leakingPipeHouse', # Протечка труб в подвале, на чердаке, на лестничной площадке
        'category_id': 2,
        'subcategory_id': 1,
        'location': 3
        },
        {'intent_name': 'lowTempHouse', # Низкая температура на лестничной площадке
         'category_id': 1,
         'subcategory_id': 1,
         'location': 3,
        'date_restriction': '15/10-12/05',
        },
        {'intent_name': 'NoRadiatorHouse', # Отсутствие радиатора на лестничной площадке
         'category_id': 1,
         'subcategory_id': 2,
         'location': 3
        },
        {'intent_name': 'brokenRadiatorHouse', # Повреждение отопительного прибора (радиатора и др.), запорной арматуры (вентиль, кран), протечка трубопровода системы центрального отопления на лестничной площадке/подвале/чердаке
         'category_id': 1,
         'subcategory_id': 3,
         'location': 3
        },
        {'intent_name': 'sewerageHouse', # Повреждение/засор внутреннего ливнестока
         'category_id': 3,
         'subcategory_id': 1,
         'location': 3
        },
        {'intent_name': 'brokenWaterDrainHouse', # Повреждение водосточной трубы
         'category_id': 3,
         'subcategory_id': 2,
         'location': 3
        },
        {'intent_name': 'damagedRoofHouse', # Повреждение кровли
         'category_id': 3,
         'subcategory_id': 3,
         'location': 3
        },
        {'intent_name': 'snowHouse', # Неубранный снег
         'category_id': 3,
         'subcategory_id': 4,
         'location': 3,
         'date_restriction': '15/10-12/05',
        },
        {'intent_name': 'iceHouse', # Наличие наледи на крыше
         'category_id': 3,
         'subcategory_id': 5,
         'location': 3,
         'date_restriction': '15/10-12/05',
        },
        {'intent_name': 'garbageTopHouse', # Отсутствие/неисправность крышки загрузочного люка мусоропровода
         'category_id': 4,
         'subcategory_id': 1,
         'location': 3
        },
        {'intent_name': 'cleaningScheduleHouse', # Отсутствие или несоблюдение графика уборки подъезда
         'category_id': 4,
         'subcategory_id': 2,
         'location': 3
        },
        {'intent_name': 'brokenGarbageDisposalHouse', # Отсутствие или неисправность замка мусоросборной камеры
         'category_id': 4,
         'subcategory_id': 3,
         'location': 3
        },
        {'intent_name': 'junkHouse', # Хранение вещей на лестничной площадке
         'category_id': 4,
         'subcategory_id': 4,
         'location': 3
        },
        {'intent_name': 'brokenGlassHouse', # Разбиты стекла на лестничной площадке
         'category_id': 4,
         'subcategory_id': 5,
         'location': 3
        },
        {'intent_name': 'brokenMailboxHouse', # Сломаны почтовые шкафы
         'category_id': 4,
         'subcategory_id': 6,
         'location': 3
        },
        {'intent_name': 'brokenBuzzerHouse', # Неисправный домофон
         'category_id': 4,
         'subcategory_id': 7,
         'location': 3
        },
        {'intent_name': 'brokenFrontDoorHouse', # Неисправный доводчик входной двери
         'category_id': 4,
         'subcategory_id': 8,
         'location': 3
        },
        {'intent_name': 'lightingElevatorHouse', # Неисправное освещение в лифте
         'category_id': 4,
         'subcategory_id': 9,
         'location': 3
        },
        {'intent_name': 'brokenElevatorHouse', # Неисправный лифт
         'category_id': 4,
         'subcategory_id': 10,
         'location': 3
        },
        {'intent_name': 'brokenRampHouse', # Неисправный пандус/аппарель
         'category_id': 4,
         'subcategory_id': 11,
         'location': 3
        },
        {'intent_name': 'lightingEntranceHouse', # Неисправное освещение в подъезде/на фасаде жилого здания
         'category_id': 4,
         'subcategory_id': 12,
         'location': 3
        },
        {'intent_name': 'insectsHouse', # Требуется дезинсекция (насекомые), дезинфекция в местах общего пользования (в т.ч. мусоропровода)
         'category_id': 5,
         'subcategory_id': 1,
         'location': 3
        },
        {'intent_name': 'ratsHouse', # Требуется дератизация (крысы) в местах общего пользования
         'category_id': 5,
         'subcategory_id': 2,
         'location': 3
        },
        {'intent_name': 'garbageCollectorHouse', # Засор мусоропровода
         'category_id': 5,
         'subcategory_id': 3,
         'location': 3
        },
        {'intent_name': 'illegalWritingsHouse', # Несанкционированные надписи/объявления на стенах дома
         'category_id': 6,
         'subcategory_id': 1,
         'location': 3
        },
        {'intent_name': 'paintHouse', # Неудовлетворительное состояние окраски фасада дома (кроме несанкционированных надписей/объявления на стенах дома)
         'category_id': 6,
         'subcategory_id': 2,
         'location': 3
        },
        {'intent_name': 'brokenSewageHouse', # Засор канализации/протечка канализационной трубы
         'category_id': 6,
         'subcategory_id': 3,
         'location': 3
        },
        {'intent_name': 'basementWindowsHouse', # Открыты/закрыты подвальные окна, продухи, вход в подвал
         'category_id': 6,
         'subcategory_id': 4,
         'location': 3
        }
]

# LOCATION CODES:
# UNKNOWN = 1
# APARTMENT = 2
# HOUSE = 3
# ENTRANCE = 4