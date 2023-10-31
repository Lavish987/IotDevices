from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets,status,generics
from django.http import HttpResponse
from .models import Device,TemperatureReading,HumidityReading
from .serializers import DeviceSerializer,HumiditySerializer,TemperatureSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class DeviceViewSet(viewsets.ModelViewSet):
    queryset=Device.objects.all()
    serializer_class=DeviceSerializer
    lookup_field='uid'


class Readings(generics.ListAPIView):   
    def list(self,request,uid,parameter):
        
        start_on = self.request.query_params.get('start_on')
        end_on = self.request.query_params.get('end_on')
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        start_date_object  = datetime.strptime(start_on, date_format)
        end_date_object = datetime.strptime(end_on, date_format)
        print(start_date_object)
    
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
                time__date__gte=start_date_object.date(),
                time__date__lte=end_date_object.date()
            )
        print(model.objects.all())
        print("--------")
        print(data)
        serialized_data = serializer_class(data, many=True,context={'request':request}).data

        return Response(serialized_data)
    