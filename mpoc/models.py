from django.db import models
from usr.models import Barangay
from django.utils import timezone
import os
import uuid

class ExecutiveOrder(models.Model):
    eo_date=models.DateField()
    eo_title=models.CharField(max_length=1000)
    eo_number=models.CharField(max_length=100,unique=True)
    eo_file=models.FileField(upload_to='eo/',blank=True,null=True)
    def __str__(self):
        return f'{self.eo_title}'
    # def save(self, *args,**kwargs):
    #     if self.pk:
    #         old=ExecutiveOrder.objects.get(pk=self.pk)
    #         if old.eo_file.path:
    #             os.remove(old.eo_file.path)
    #         else:
    #             super().save(*args,**kwargs)
            
class Ordinance(models.Model):
    ordinance_date=models.DateField()
    ordinance_title=models.CharField(max_length=1000)
    ordinance_number=models.CharField(max_length=100,unique=True)
    ordinance_file=models.FileField(upload_to='ordinance/',blank=True,null=True)
    def __str__(self):
        return f'{self.ordinance_title}'
    
class Incident(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    incident_number=models.CharField(max_length=50)
    barangay=models.ForeignKey(Barangay,on_delete=models.CASCADE, related_name='barangay',default=1)
    purok=models.CharField(max_length=100,blank=True)
    incident_type=models.CharField(max_length=100,blank=True)
    crime_category=models.CharField(max_length=250,blank=True)
    incident_datetime=models.DateTimeField(blank=True)
    date_reported=models.DateTimeField(blank=True)
    status=models.CharField(max_length=200,blank=True)
    action_taken=models.TextField(blank=True)
    narrative=models.TextField(blank=True)
    incident_file=models.FileField(upload_to='incident/',null=True,blank=True)
    def __str__(self):
        return self.incident_number

