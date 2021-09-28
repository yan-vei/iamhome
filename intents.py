# Базовые интенты
CREATE_INQUIRY = 'createInquiry'
CHECK_INQUIRY = 'checkInquiry'
YANDEX_HELP = 'YANDEX.HELP'
YANDEX_CONFIRM = 'YANDEX.CONFIRM'
YANDEX_REJECT = 'YANDEX.REJECT'
LEARN_MORE = 'learnMore'

# Базовые сущности
YANDEX_GEO = 'YANDEX.GEO'

# Интенты для оформления заявки
CHOOSE_INQUIRY_LOCATION = 'chooseInquiryLocation'

# Интенты по категориям проблем
PROBLEM_INTENTS = [{'intent_name': 'lowTempApartment', 'category_id': 1, 'subcategory_id': 1, 'date_restriction': '15/09-12/05',
                    'location': 2}]

# LOCATION CODES:
# UNKNOWN = 1
# APARTMENT = 2
# HOUSE = 3
# ENTRANCE = 4