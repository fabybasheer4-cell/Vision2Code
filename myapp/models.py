from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    place=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    photo=models.CharField(max_length=300)
    USER=models.OneToOneField(User,on_delete=models.CASCADE)

class Feedback(models.Model):
    feedback = models.CharField(max_length=500)
    date = models.DateField()
    CUSTOMER=models.ForeignKey(Customer,on_delete=models.CASCADE)

class History(models.Model):
    CUSTOMER=models.ForeignKey(Customer,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,default='')
    date = models.DateField(default="28-08-2025")
    image=models.CharField(max_length=200,default='')
    code_file=models.CharField(max_length=200)
    type=models.CharField(max_length=100)


