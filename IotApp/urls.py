from django.urls import path,include
from rest_framework import routers
from .views import DeviceViewSet

router=routers.DefaultRouter()
router.register('',DeviceViewSet)

urlpatterns=[
    path('api/devices/',include(router.urls)),  
]