from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Barangay(models.Model):
    name=models.CharField(max_length=100,null=False,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        managed=False
        db_table= '"my_schema"."Barangay"'
