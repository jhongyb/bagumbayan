from django.db import models


class Department(models.Model):
    department=models.CharField(max_length=20,unique=True, null=False)
    description=models.CharField(max_length=250,null=False)
    def __str__(self):
        return self.department

class Employee(models.Model):
    biometric_number=models.CharField(max_length=20,unique=True,null=True)
    employee_id=models.CharField(max_length=20,unique=True,null=True)
    lastname=models.CharField(max_length=100,null=False)
    firstname=models.CharField(max_length=100,null=False)
    middlename=models.CharField(max_length=100)
    extname=models.CharField(max_length=10,null=True,blank=True) 
    birthday=models.DateField(null=True)
    sex=models.CharField(max_length=6,null=False)
    dept=models.ForeignKey('Department',on_delete=models.CASCADE)
    position=models.CharField(max_length=250,null=True,blank=True)
    type=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='./media',blank=True,null=True)
    def __str__(self):
        return f'{self.lastname}, {self.firstname} {self.middlename} {self.extname}'


class Biometric(models.Model):
    bio_id=models.CharField(max_length=15,null=False,blank=False)
    bio_date=models.DateField()
    bio_time=models.TimeField() 
    bio_punchstate=models.CharField(max_length=50)
  


