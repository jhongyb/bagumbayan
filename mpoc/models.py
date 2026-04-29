from django.db import models
import os

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
            
    