from rest_framework import serializers 
from .models import Device, TemperatureReading, HumidityReading
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device 
        fields='__all__'

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model=TemperatureReading 
        fields='__all__' 
class HumiditySerializer(serializers.ModelSerializer):  
   # url = serializers.HyperlinkedIdentityField(view_name='humidityreading-detail', lookup_field='uid')
    class Meta:
        model=HumidityReading
        fields='__all__'


