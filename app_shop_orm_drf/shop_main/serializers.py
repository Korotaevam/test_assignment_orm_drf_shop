from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from shop_main.models import CityModels, StreetModels, ShopModels


class CitySerializers(serializers.ModelSerializer):
    """Сериализатор для модели города"""

    class Meta:
        model = CityModels
        fields = ('id', 'name',)


class StreetSerializers(serializers.ModelSerializer):
    class Meta:
        model = StreetModels
        fields = ('id', 'name', 'city')
        validators = [
            UniqueTogetherValidator(
                queryset=StreetModels.objects.all(),
                fields=('name', 'city',)
            ),
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance).copy()
        data['city'] = instance.city.name
        return data


class ShopSerializers(serializers.ModelSerializer):
    """
         Сериализатор для модели Shop, представляющий реляционные поля.
         "город" и "улица" в виде текста при отображении списка магазинов
         """
    city = serializers.SlugRelatedField(slug_field='name', read_only=True)
    street = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = ShopModels
        fields = ('name', 'city', 'street', 'is_open', 'house', 'time_open', 'time_close')

    def to_representation(self, instance):
        data = super().to_representation(instance).copy()
        data['city'] = instance.city.name
        data['street'] = instance.street.name
        return data


class ShopIdSerializer(serializers.ModelSerializer):
    """
         Сериализатор для модели магазина, который представляет магазин только как
         поле id после создания нового магазина
         """

    class Meta:
        model = ShopModels
        fields = ('id',)


class ShopCreateSerializers(serializers.ModelSerializer):


    class Meta:
        model = ShopModels
        fields = ('name', 'city', 'street', 'is_open', 'house', 'time_open', 'time_close')

        validators = [
            UniqueTogetherValidator(
                queryset=ShopModels.objects.all(),
                fields=('name', 'city', 'street', 'house',)
            ),
        ]

    def to_representation(self, instance):
        """Return only shop_id after creating a new store"""
        if self.context['request'].method == 'POST':
            serializer = ShopIdSerializer(instance)
            return serializer.data
        return super().to_representation(instance)

    def validate(self, data):
        errors = {}

        if data['city'] != data['street'].city:
            errors['city'] = 'указанная улица не принадлежит указанному городу'

        if data['time_open'] > data['time_close']:
            errors['opening_time'] = errors['closing_time'] = (
                'время закрытия магазина должно быть позже времени открытия'
            )

        if errors:
            raise serializers.ValidationError(errors)

        return data
