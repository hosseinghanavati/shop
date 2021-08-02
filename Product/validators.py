from django.core.exceptions import ValidationError


def discount_percent_validator(value):
    if value < 0 or value > 100:
        raise ValidationError('Enter a number between 0 and 100')

