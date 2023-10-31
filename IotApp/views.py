from datetime import datetime, timezone
from django.shortcuts import render
from rest_framework import viewsets,status,generics
from django.http import HttpResponse
from .models import Device,TemperatureReading,HumidityReading
from .serializers import DeviceSerializer,HumiditySerializer,TemperatureSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone as django_timezone

# Create your views here.
class DeviceViewSet(viewsets.ModelViewSet):
    queryset=Device.objects.all()
    serializer_class=DeviceSerializer
    lookup_field='uid'

class TemperaturereadingViewSet(viewsets.ModelViewSet):
    queryset=TemperatureReading.objects.all()
    serializer_class=TemperatureSerializer
    

class HumidityreadingViewSet(viewsets.ModelViewSet):
    queryset=HumidityReading.objects.all()
    serializer_class=HumiditySerializer

def Graph(request):
    return HttpResponse("Hi") 

class Readings(generics.ListAPIView):   
    def list(self,request,uid,parameter):
        
        start_on = self.request.query_params.get('start_on')
        end_on = self.request.query_params.get('end_on')
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        start_date_object  = datetime.strptime(start_on, date_format)
        end_date_object = datetime.strptime(end_on, date_format)

        start_date_object = start_date_object.replace(tzinfo=timezone.utc)
        end_date_object = end_date_object.replace(tzinfo=timezone.utc)
        start_date_object = start_date_object.astimezone(django_timezone.get_current_timezone())
        end_date_object = end_date_object.astimezone(django_timezone.get_current_timezone())
        
        if parameter == 'temperature':
                model = TemperatureReading
                serializer_class = TemperatureSerializer
        elif parameter == 'humidity':
                model = HumidityReading
                serializer_class = HumiditySerializer
        else:
            return HttpResponse({'error': 'Invalid parameter'}, status=status.HTTP_400_BAD_REQUEST)
        print(start_date_object)
        print(end_date_object)
        data = model.objects.filter(
                uid=uid,
                time__gte=start_date_object,
                time__lte=end_date_object
            )
        
        serialized_data = serializer_class(data, many=True).data
        print(serialized_data)
        return Response(serialized_data)
    