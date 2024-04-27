from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone


def real_age(value: datetime) -> None:
    today = timezone.localtime(timezone.now()).date()
    age = (today - value.date()).days / 365
    if age < 1 or age > 120:
        raise ValidationError(
            'Ожидается возраст от 1 года до 120 лет'
        )
