from datetime import datetime, timezone
from django.shortcuts import render
from rest_framework import viewsets,status,generics
from django.http import HttpResponse
from .models import Device,TemperatureReading,HumidityReading
from .serializers import DeviceSerializer,HumiditySerializer,TemperatureSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone as django_timezone
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from io import BytesIO
import base64

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

class Graph_View(generics.ListAPIView):
    def list(self,request):
        uid=self.request.query_params.get('uid')
        temperature_data = TemperatureReading.objects.filter(uid=uid)
        humidity_data = HumidityReading.objects.filter(uid=uid)
        temperature_time = [str(data.time) for data in temperature_data]
        temperature= [data.temperature for data in temperature_data]
        humidity_time = [str(data.time) for data in humidity_data]
        humidity= [data.humidity for data in humidity_data]
        #print(temperature_time,temperature,humidity_time,humidity)
        
        fig,ax1 = plt.subplots(figsize=(10, 6))
        ax2 = ax1.twinx()
        ax1.plot(temperature_time, temperature, label='Temperature', color='blue')
        ax1.set_ylabel('Temperature', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        ax2.plot(humidity_time, humidity, label='Humidity', color='green')
        ax2.set_ylabel('Humidity', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
        plt.xticks(rotation=90)

        plt.xlabel('Time')
        plt.title('Temperature and Humidity vs. Time')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_data = base64.b64encode(buffer.read()).decode()
        plt.close()
        return render(request, 'IotApp/graph.html', {'img_data': img_data})
        

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
        #print(start_date_object)
        #print(end_date_object)
        data = model.objects.filter(
                uid=uid,
                time__gte=start_date_object,
                time__lte=end_date_object
            )
        
        serialized_data = serializer_class(data, many=True).data
        return Response(serialized_data)
    