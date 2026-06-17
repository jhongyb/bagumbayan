from django.db import models
from usr.models import Barangay

class OscaStatus(models.Model):
    status_description=models.CharField(max_length=100)
    def __str__(self):
        return self.status_description

class OscaCategory(models.Model):
    category_description=models.CharField(max_length=100)
    def __str__(self):
            return self.category_description

class Osca_Informations(models.Model):
     idno=models.CharField(max_length=10,unique=True)
     lastname=models.CharField(max_length=100)
     firstname=models.CharField(max_length=100)
     middlename=models.CharField(max_length=100,null=True,blank=True)
     extname=models.CharField(max_length=100,null=True,blank=True)
     birthday=models.DateField()
     sex=models.CharField(max_length=10,choices=[('M','MALE'),('F','FEMALE')])
     purok=models.CharField(max_length=50,blank=True)
     barangay=models.ForeignKey(Barangay,on_delete=models.CASCADE,related_name='oscabarangay')
     date_issued=models.DateField(blank=True)
     status=models.ForeignKey(OscaStatus,on_delete=models.CASCADE,related_name='oscastatus')
     category=models.ForeignKey(OscaCategory,on_delete=models.CASCADE,related_name='oscacategory')
     member_status=models.CharField(max_length=50,choices=[('A','ACTIVE'),('I','INACTIVE')])
     
     def __str__(self):
          return self.idno


