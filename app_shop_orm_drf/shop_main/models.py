from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime

from django.db.models import Q

CURRENT_TIME = datetime.now().time()


class CityModels(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название Города')

    def __str__(self):
        return self.name


class StreetModels(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название Улицы')
    city = models.ForeignKey('CityModels', on_delete=models.PROTECT, verbose_name='Город')

    def __str__(self):
        return f'{self.name}, {self.city}'


class ShopQuerySet(models.QuerySet):
    def open_shop(self):
        return self.filter(time_open__lte=CURRENT_TIME, time_close__gte=CURRENT_TIME)

    def close_shop(self):
        return self.filter(Q(time_open__gte=CURRENT_TIME) | Q(time_close__lte=CURRENT_TIME))


class ShopManager(models.Manager):
    def get_queryset(self):
        return ShopQuerySet(self.model)

    def open_shop(self):
        return self.get_queryset().open_shop()

    def close_shop(self):
        return self.get_queryset().close_shop()


class ShopModels(models.Model):
    objects = ShopManager()

    name = models.CharField(max_length=255, verbose_name='Название Магазина')
    city = models.ForeignKey('CityModels', on_delete=models.PROTECT, verbose_name='Город')
    street = models.ForeignKey('StreetModels', on_delete=models.PROTECT, verbose_name='Улица')
    house = models.CharField(max_length=255, verbose_name='Дом')
    time_open = models.TimeField(verbose_name='время открытия')
    time_close = models.TimeField(verbose_name='время закрытия')

    def __str__(self):
        return self.name

    @property
    def is_open(self):
        return 'Open' if self.time_open <= CURRENT_TIME <= self.time_close else 'Close'

    def clean(self, *args, **kwargs):
        if self.street.city != self.city:
            raise ValidationError(
                {'city': 'указанная улица не принадлежит указанному городу'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

