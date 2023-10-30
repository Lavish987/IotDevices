from rest_framework import serializers 
from .models import Device, TemperatureReading, HumidityReading
class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Device 
        fields='__all__'

class TemperatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=TemperatureReading 
        fields='__all__' 
class HumiditySerializer(serializers.HyperlinkedModelSerializer):  
    class Meta:
        model=HumidityReading
        fields='__all__'


