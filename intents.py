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
                    'date_pronunciation': 'с 15 октября по 12 мая',
                    'location': 2,
                    'informal_name': 'Холодно'},
                   {'intent_name': 'highTempApartment',  # Высокая температура в отапливаемом помещении
                    'category_id': 1,
                    'subcategory_id': 2,
                    'date_restriction': '15/10-12/05',
                    'date_pronunciation': 'с 15 октября по 12 мая',
                    'location': 2,
                    'informal_name': 'Жарко'},
                   {'intent_name': 'noColdWaterApartment',  # Отсутствие холодной воды
                    'category_id': 2,
                    'subcategory_id': 1,
                    'location': 2,
                    'informal_name': 'Нет холодной воды'},
                   {'intent_name': 'noHotWaterApartment',  # Отсутствие горячей воды
                    'category_id': 2,
                    'subcategory_id': 2,
                    'location': 2,
                    'informal_name': 'Нет горячей воды'},
                   {'intent_name': 'weakHotPressureApartment',  # Слабый напор горячей воды
                    'category_id': 2,
                    'subcategory_id': 3,
                    'location': 2,
                    'informal_name': 'Слабый напор горячей воды'},
                   {'intent_name': 'weakColdPressureApartment',  # Слабый напор холодной воды
                    'category_id': 2,
                    'subcategory_id': 4,
                    'location': 2,
                    'informal_name': 'Слабый напор холодной воды'},
                   {'intent_name': 'badQualityHotApartment',  # Плохое качество горячей воды
                    'category_id': 2,
                    'subcategory_id': 5,
                    'location': 2,
                    'informal_name': 'Грязная горячая вода'},
                   {'intent_name': 'badQualityColdApartment',  # Плохое качество холодной воды
                    'category_id': 2,
                    'subcategory_id': 6,
                    'location': 2,
                    'informal_name': 'Грязная холодная вода'},
                   {'intent_name': 'brokenSewageApartment',  # Неисправность канализации
                    'category_id': 3,
                    'subcategory_id': 1,
                    'location': 2,
                    'informal_name': 'Засорилась канализация'},
                   {'intent_name': 'brokenVentilationApartment',  # Неисправность системы вентиляции
                    'category_id': 4,
                    'subcategory_id': 1,
                    'location': 2,
                    'informal_name': 'Сломана вентиляция'},
                    {'intent_name': 'leakingPipeApartment',     # Ненадлежащее содержание трубопроводов и элементов системы водоснабжения, являющихся общедомовым имуществом
                    'category_id': 3,
                    'subcategory_id': 7,
                    'location': 2,
                    'informal_name': 'Течет труба'},
                    {'intent_name': 'damagedRadiatorApart',     # Повреждение запорной арматуры (вентиль, кран), стояка центрального отопления
                    'category_id': 4,
                    'subcategory_id': 3,
                    'location': 2,
                    'informal_name': 'Течет батарея'
                    }
                   ]

HOUSE_INTENTS = \
    [
        {'intent_name': 'leakingPipeHouse', # Протечка труб в подвале, на чердаке, на лестничной площадке
        'category_id': 2,
        'subcategory_id': 1,
        'location': 3,
        'informal_name': 'Течет труба'
        },
        {'intent_name': 'lowTempHouse', # Низкая температура на лестничной площадке
         'category_id': 1,
         'subcategory_id': 1,
         'location': 3,
        'informal_name': 'Холодно',
        'date_restriction': '15/10-12/05',
         'date_pronunciation': 'с 15 октября по 12 мая'
        },
        {'intent_name': 'NoRadiatorHouse', # Отсутствие радиатора на лестничной площадке
         'category_id': 1,
         'subcategory_id': 2,
         'location': 3,
        'informal_name': 'Нет батареи',
        },
        {'intent_name': 'brokenRadiatorHouse', # Повреждение отопительного прибора (радиатора и др.), запорной арматуры (вентиль, кран), протечка трубопровода системы центрального отопления на лестничной площадке/подвале/чердаке
         'category_id': 1,
         'subcategory_id': 3,
         'location': 3,
        'informal_name': 'Сломана батарея'
        },
        {'intent_name': 'sewerageHouse', # Повреждение/засор внутреннего ливнестока
         'category_id': 3,
         'subcategory_id': 1,
         'location': 3,
        'informal_name': 'Засорилась ливневка'
        },
        {'intent_name': 'brokenWaterDrainHouse', # Повреждение водосточной трубы
         'category_id': 3,
         'subcategory_id': 2,
         'location': 3,
        'informal_name': 'Сломалась водосточная труба'
        },
        {'intent_name': 'damagedRoofHouse', # Повреждение кровли
         'category_id': 3,
         'subcategory_id': 3,
         'location': 3,
        'informal_name': 'Повреждена крыша'
        },
        {'intent_name': 'snowHouse', # Неубранный снег
         'category_id': 3,
         'subcategory_id': 4,
         'location': 3,
         'date_restriction': '15/10-12/05',
         'date_pronunciation': 'с 15 октября по 12 мая',
        'informal_name': 'Не чистят снег'
        },
        {'intent_name': 'iceHouse', # Наличие наледи на крыше
         'category_id': 3,
         'subcategory_id': 5,
         'location': 3,
         'date_restriction': '15/10-12/05',
        'date_pronunciation': 'с 15 октября по 12 мая',
        'informal_name': 'Наледь на крыше'
        },
        {'intent_name': 'garbageTopHouse', # Отсутствие/неисправность крышки загрузочного люка мусоропровода
         'category_id': 4,
         'subcategory_id': 1,
         'location': 3,
        'informal_name': 'Сломана крышка мусоропровода'
        },
        {'intent_name': 'cleaningScheduleHouse', # Отсутствие или несоблюдение графика уборки подъезда
         'category_id': 4,
         'subcategory_id': 2,
         'location': 3,
        'informal_name': 'Не убирают в парадной'
        },
        {'intent_name': 'brokenGarbageDisposalHouse', # Отсутствие или неисправность замка мусоросборной камеры
         'category_id': 4,
         'subcategory_id': 3,
         'location': 3,
        'informal_name': 'Сломан замок мусоропровода'
        },
        {'intent_name': 'junkHouse', # Хранение вещей на лестничной площадке
         'category_id': 4,
         'subcategory_id': 4,
         'location': 3,
        'informal_name': 'Соседи захламили лестничную площадку'
        },
        {'intent_name': 'brokenGlassHouse', # Разбиты стекла на лестничной площадке
         'category_id': 4,
         'subcategory_id': 5,
         'location': 3,
        'informal_name': 'Разбито окно'
        },
        {'intent_name': 'brokenMailboxHouse', # Сломаны почтовые шкафы
         'category_id': 4,
         'subcategory_id': 6,
         'location': 3,
        'informal_name': 'Сломан почтовый ящик'
        },
        {'intent_name': 'brokenBuzzerHouse', # Неисправный домофон
         'category_id': 4,
         'subcategory_id': 7,
         'location': 3,
        'informal_name': 'Сломан домофон'
        },
        {'intent_name': 'brokenFrontDoorHouse', # Неисправный доводчик входной двери
         'category_id': 4,
         'subcategory_id': 8,
         'location': 3,
        'informal_name': 'Сломался доводчик двери'
        },
        {'intent_name': 'lightingElevatorHouse', # Неисправное освещение в лифте
         'category_id': 4,
         'subcategory_id': 9,
         'location': 3,
        'informal_name': 'Не горит свет в лифте'
        },
        {'intent_name': 'brokenElevatorHouse', # Неисправный лифт
         'category_id': 4,
         'subcategory_id': 10,
         'location': 3,
        'informal_name': 'Не работает лифт'
        },
        {'intent_name': 'brokenRampHouse', # Неисправный пандус/аппарель
         'category_id': 4,
         'subcategory_id': 11,
         'location': 3,
        'informal_name': 'Сломан пандус'
        },
        {'intent_name': 'lightingEntranceHouse', # Неисправное освещение в подъезде/на фасаде жилого здания
         'category_id': 4,
         'subcategory_id': 12,
         'location': 3,
        'informal_name': 'Не работает освещение'
        },
        {'intent_name': 'insectsHouse', # Требуется дезинсекция (насекомые), дезинфекция в местах общего пользования (в т.ч. мусоропровода)
         'category_id': 5,
         'subcategory_id': 1,
         'location': 3,
        'informal_name': 'Завелись насекомые'
        },
        {'intent_name': 'ratsHouse', # Требуется дератизация (крысы) в местах общего пользования
         'category_id': 5,
         'subcategory_id': 2,
         'location': 3,
        'informal_name': 'Завелись крысы'
        },
        {'intent_name': 'garbageCollectorHouse', # Засор мусоропровода
         'category_id': 5,
         'subcategory_id': 3,
         'location': 3,
        'informal_name': 'Засорился мусоропровод'
        },
        {'intent_name': 'illegalWritingsHouse', # Несанкционированные надписи/объявления на стенах дома
         'category_id': 6,
         'subcategory_id': 1,
         'location': 3,
        'informal_name': 'Изрисованы стены'
        },
        {'intent_name': 'paintHouse', # Неудовлетворительное состояние окраски фасада дома (кроме несанкционированных надписей/объявления на стенах дома)
         'category_id': 6,
         'subcategory_id': 2,
         'location': 3,
        'informal_name': 'Осыпалась краска на фасаде'
        },
        {'intent_name': 'brokenSewageHouse', # Засор канализации/протечка канализационной трубы
         'category_id': 6,
         'subcategory_id': 3,
         'location': 3,
        'informal_name': 'Засорилась канализация'
        },
        {'intent_name': 'basementWindowsHouse', # Открыты/закрыты подвальные окна, продухи, вход в подвал
         'category_id': 6,
         'subcategory_id': 4,
         'location': 3,
        'informal_name': 'Открыты подвальные окна'
        }
]


TOP_HOUSE_INTENTS = ['brokenSewageHouse', 'iceHouse', 'cleaningScheduleHouse', 'illegalWritingsHouse']
TOP_APARTMENT_INTENTS = ['leakingPipeApartment', 'lowTempApartment', 'noColdWaterApartment', 'brokenSewageApartment']

# LOCATION CODES:
# UNKNOWN = 1
# APARTMENT = 2
# HOUSE = 3
# ENTRANCE = 4