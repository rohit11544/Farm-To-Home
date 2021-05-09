from django.db import models

# Create your models here.
from phone_field import PhoneField


class land(models.Model):
    Name = models.CharField(max_length=100)
    Phone_Number = PhoneField(blank=True)
    City = models.CharField(max_length=100)
    Pin_Code = models.IntegerField()
    Acres = models.IntegerField()
    Rent = models.IntegerField()
    Share = models.IntegerField()
    R_or_S = models.IntegerField()
    Availability = models.IntegerField()
    Target = models.IntegerField()
    UserName = models.CharField(max_length=100)
    Password = models.IntegerField()

    def __str__(self):
        return self.Name+" "+self.City


class city(models.Model):
    City = models.CharField(max_length=100)
    Index = models.IntegerField()

    def __str__(self):
        return self.City+" "+str(self.Index)


class SerachingLand(models.Model):
    Town = models.CharField(max_length=100)
    Acres = models.IntegerField()
    PinCode = models.IntegerField()


class RegisterLand(models.Model):
    UserName = models.CharField(max_length=100)
    Password = models.IntegerField()
    ConformPassword = models.IntegerField()
    Name = models.CharField(max_length=100)
    Phone_Number = PhoneField(blank=True)
    City = models.CharField(max_length=100)
    PinCode = models.IntegerField()
    Acres = models.IntegerField()
    Rent = models.IntegerField()
    Share = models.IntegerField()
    R_or_S = models.IntegerField()
    Availability = models.IntegerField()
    

class GetDetailsLogin(models.Model):
    GivenUserNum = models.IntegerField()
    UserName = models.CharField(max_length=100)
    Password = models.IntegerField()

class ForgetPassword(models.Model):
    GivenUserNum = models.IntegerField()
    Name = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Password = models.IntegerField()
    ConformPassword = models.IntegerField()

class FinalUpdate(models.Model):
    GivenUserNum = models.IntegerField()
    Name = models.CharField(max_length=100)
    Phone_Number = PhoneField(blank=True)
    City = models.CharField(max_length=100)
    PinCode = models.IntegerField()
    Acres = models.IntegerField()
    Rent = models.IntegerField()
    Share = models.IntegerField()
    R_or_S = models.IntegerField()
    Availability = models.IntegerField()







        