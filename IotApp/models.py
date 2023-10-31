from django.db import models

# Create your models here.
class Device(models.Model):
    uid=models.CharField(max_length=50,unique=True)
    name=models.CharField(max_length=50)

class TemperatureReading(models.Model):
    uid=models.ForeignKey(Device,on_delete=models.CASCADE,to_field='uid')
    temperature=models.FloatField()
    time=models.DateTimeField() 

class HumidityReading(models.Model):
    uid=models.ForeignKey(Device,on_delete=models.CASCADE,to_field='uid')
    humidity=models.FloatField()
    time=models.DateTimeField()