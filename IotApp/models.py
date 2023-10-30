from django.db import models

# Create your models here.
class Device(models.Model):
    uid=models.CharField(max_length=50,unique=True)
    name=models.CharField(max_length=50)

class TemperatureReading(models.Model):
    device=models.ForeignKey(Device,on_delete=models.CASCADE)
    temperature=models.FloatField()
    time=models.DateTimeField() 

class HumidityReading(models.Model):
    device=models.ForeignKey(Device,on_delete=models.CASCADE)
    humidity=models.FloatField()
    time=models.DateTimeField()