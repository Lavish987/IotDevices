from django.urls import path,include
from rest_framework import routers
from .views import DeviceViewSet
from IotApp.views import Readings

app_name='IotApp'
router=routers.DefaultRouter(trailing_slash=False)
router.register(r'api/devices',DeviceViewSet)

urlpatterns=[
    path('api/devices/<str:uid>/readings/<str:parameter>/',Readings.as_view()),
    path('',include(router.urls)),  
    

]