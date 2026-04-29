from django.db import models
from django.contrib.auth.models import User

class Page(models.Model):
    page_description=models.CharField(max_length=100)
    def __str__(self):
        return f'{self.id} {self.page_description}'

class ViewAccess(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    page=models.ForeignKey(Page,on_delete=models.CASCADE)
    
    