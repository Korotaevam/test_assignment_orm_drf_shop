from django.urls import path, include
from rest_framework import routers

from shop_main.views import ShopViewSet, CityViewSet, StreetViewSet, StreetOfCityAPIView

router = routers.DefaultRouter()
router.register(r'shop', ShopViewSet)
router.register(r'street', StreetViewSet)
router.register(r'city', CityViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('city/<int:city_id>/street/', StreetOfCityAPIView.as_view()),
]
