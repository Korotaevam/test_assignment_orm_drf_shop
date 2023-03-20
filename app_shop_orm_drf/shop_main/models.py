from django.db import models


class ShopModels(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название Магазина')
    city = models.ForeignKey('CityModels', on_delete=models.PROTECT, verbose_name='Город')
    street = models.ForeignKey('StreetModels', on_delete=models.PROTECT, verbose_name='Улица')
    house = models.CharField(max_length=255, verbose_name='Дом')
    time_open = models.TimeField(verbose_name='время открытия')
    time_close = models.TimeField(verbose_name='время закрытия')


class CityModels(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название Города')


class StreetModels(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название Улицы')
    city = models.ForeignKey('CityModels', on_delete=models.PROTECT, verbose_name='Город')

