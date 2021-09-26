import random

POSITIVE_ANSWERS = ['Хорошо', 'Поняла', 'Отлично', 'Поняла Вас', 'Отлично', 'Записала']


def add_positive_answer(text):
    return random.choice(POSITIVE_ANSWERS) + '. ' + text
