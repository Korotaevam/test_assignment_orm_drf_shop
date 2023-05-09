from rest_framework import generics, viewsets, mixins, serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from shop_main.models import ShopModels, StreetModels, CityModels
from shop_main.serializers import ShopSerializers, CitySerializers, StreetSerializers, ShopCreateSerializers


class ShopViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = ShopModels.objects.all()
    serializer_class = ShopSerializers

    # def get_serializer_class(self):
    #     if self.action in ('list', 'retrieve',):
    #         return ShopDetailSerializer
    #     return super().get_serializer_class()  # for create/destroy/update

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        street = request.query_params.get('street')
        city = request.query_params.get('city')
        open = request.query_params.get('open')

        if street or city:
            queryset = queryset.filter(street=street) if street else queryset
            queryset = queryset.filter(city=city) if city else queryset

        if open:
            queryset = queryset.open_shop() if int(open) else queryset.close_shop()

        serializer = ShopSerializers(queryset, many=True)

        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return super().get_serializer_class()
        return ShopCreateSerializers  # for create/destroy/update


class CityViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = CityModels.objects.all()
    serializer_class = CitySerializers


class StreetViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = StreetModels.objects.all()
    serializer_class = StreetSerializers


class StreetOfCityAPIView(generics.ListAPIView):
    serializer_class = StreetSerializers

    def get_queryset(self):
        city_id = self.kwargs.get('city_id')

        if not StreetModels.objects.filter(id=city_id).exists():
            raise serializers.ValidationError(
                {"error": "города с таким id не существует"}
            )

        return StreetModels.objects.filter(city_id=city_id).order_by('name')

# class ShopAPIView(generics.ListCreateAPIView):
#     queryset = ShopModels.objects.all()
#     serializer_class = ShopSerializers
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#
#         street = request.query_params['street']
#         city = request.query_params['city']
#         open = request.query_params['open']
#
#         if open == '1':
#             queryset = queryset.open_shop().filter(city=city).filter(street=street)
#         elif open == '0':
#             queryset = queryset.close_shop().filter(city=city).filter(street=street)
#
#         serializer = ShopSerializers(queryset, many=True)
#
#         return Response(serializer.data)
