from datetime import datetime

from rest_framework.exceptions import ValidationError


def year_validator(value):
    if value > datetime.now().year:
        raise ValidationError((f'{value} год из будущего. '
                               'Укажите год из прошлого или настоящего!'),)


def score_validator(value):
    if value < 1 or value > 10:
        raise ValidationError('Оценка может быть от 1 до 10.')
