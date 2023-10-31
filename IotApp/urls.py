from django.urls import path,include
from rest_framework import routers
from .views import DeviceViewSet,TemperaturereadingViewSet,HumidityreadingViewSet
from IotApp.views import Readings
from . import views
app_name='IotApp'
router=routers.DefaultRouter(trailing_slash=False)
router.register(r'api/devices',DeviceViewSet)
router.register(r'api/temperature',TemperaturereadingViewSet)
router.register(r'api/humidity',HumidityreadingViewSet)
urlpatterns=[
    path('api/devices/<str:uid>/readings/<str:parameter>/',Readings.as_view()),
    path('devices-graph/',views.Graph),
    path('',include(router.urls)),  
    

]