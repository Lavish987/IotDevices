from django.shortcuts import render
from rest_framework import viewsets,status
from django.http import HttpResponse
from .models import Device,TemperatureReading,HumidityReading
from .serializers import DeviceSerializer,HumiditySerializer,TemperatureSerializer
from rest_framework.decorators import action

# Create your views here.
class DeviceViewSet(viewsets.ModelViewSet):
    queryset=Device.objects.all()
    serializer_class=DeviceSerializer

    @action(detail=True,methods=['get'])
    def readings(self,request,device_id,parameter):
        start_on = self.request.query_params.get('start_on')
        end_on = self.request.query_params.get('end_on')
        #print(start_on,end_on,device,parameter)
        if parameter == 'temperature':
                model = TemperatureReading
                serializer_class = TemperatureSerializer
        elif parameter == 'humidity':
                model = HumidityReading
                serializer_class = HumiditySerializer
        else:
            return HttpResponse({'error': 'Invalid parameter'}, status=status.HTTP_400_BAD_REQUEST)

        data = model.objects.filter(
                device_id=device_id,
                time__gte=start_on,
                time__lte=end_on
            )
        return HttpResponse(data)