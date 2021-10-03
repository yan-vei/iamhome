import random

POSITIVE_ANSWERS = ['Хорошо', 'Поняла', 'Отлично', 'Поняла Вас', 'Ясно', 'Понятно', 'Записала']


def add_positive_answer(text):
    return random.choice(POSITIVE_ANSWERS) + '. ' + text
