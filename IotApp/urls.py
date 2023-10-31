from django.urls import path,include
from rest_framework import routers
from .views import DeviceViewSet

router=routers.DefaultRouter(trailing_slash=False)
router.register(r'api/devices',DeviceViewSet)

urlpatterns=[
    path('',include(router.urls)),  

]