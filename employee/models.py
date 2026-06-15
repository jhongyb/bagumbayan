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
    middlename=models.CharField(max_length=100,blank=True,null=True)
    extname=models.CharField(max_length=10,null=True,blank=True) 
    birthday=models.DateField(null=True,blank=True)
    sex=models.CharField(max_length=6,choices=[('M','MALE'),('F','FEMALE')],blank=True)
    civilstatus=models.CharField(max_length=15,null=True,blank=True,choices=[
        ('S','SINGLE'),
        ('M','MARRIED'),
        ('SEP','SEPERATED'),
        ('W','WIDOWED'),
        ('WDR','WIDOWER')])
    dept=models.ForeignKey('Department',on_delete=models.CASCADE)
    position=models.CharField(max_length=250,null=True,blank=True)
    type=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='employee/',blank=True,null=True)
    height=models.FloatField(blank=True,null=True)
    weight=models.FloatField(blank=True,null=True)
    citizenship=models.CharField(max_length=15,null=True,blank=True)
    bloodtype=models.CharField(max_length=15,null=True,blank=True)
    add_block=models.CharField(max_length=50,null=True,blank=True)
    add_street=models.CharField(max_length=50,null=True,blank=True)
    add_village=models.CharField(max_length=50,null=True,blank=True)
    add_barangay=models.CharField(max_length=50,null=True,blank=True)
    add_municipality=models.CharField(max_length=50,null=True,blank=True)
    add_province=models.CharField(max_length=50,null=True,blank=True)
    zip_code=models.CharField(max_length=50,null=True,blank=True)
    telephone=models.CharField(max_length=50,null=True,blank=True)
    mobile=models.CharField(max_length=50,null=True,blank=True)
    email=models.EmailField(max_length=50,null=True,blank=True)
    umid=models.CharField(max_length=50,null=True,blank=True)
    pagibig=models.CharField(max_length=50,null=True,blank=True)
    philhealth=models.CharField(max_length=50,null=True,blank=True)
    philsys=models.CharField(max_length=50,null=True,blank=True)
    tin=models.CharField(max_length=50,null=True,blank=True)
    gsis=models.CharField(max_length=50,null=True,blank=True)


    def __str__(self):
        return f'{self.lastname}, {self.firstname} {self.middlename} {self.extname}'


class Biometric(models.Model):
    bio_id=models.CharField(max_length=15,null=False,blank=False)
    bio_date=models.DateField()
    bio_time=models.TimeField() 
    bio_punchstate=models.CharField(max_length=50)
  


