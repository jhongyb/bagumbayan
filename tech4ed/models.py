from django.db import models

class Tech4edFiles(models.Model):
    title=models.CharField(max_length=1000)
    file=models.FileField(upload_to='tech4ed/')
