from django.db import models

# Create your models here.
from phone_field import PhoneField


class farmer(models.Model):
    Name = models.CharField(max_length=100)
    Phone_Number = PhoneField(blank=True)
    Item = models.CharField(max_length=100)
    Price_Organic = models.IntegerField()
    Price_Inorganic = models.IntegerField()
    Price = models.IntegerField()
    City = models.CharField(max_length=100)
    PinCode = models.IntegerField()
    Organic_Inorganic = models.IntegerField()
    Rating = models.IntegerField()
    Quantity = models.IntegerField()
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

class Item(models.Model):
    Item = models.CharField(max_length=100)
    Index = models.IntegerField()
    OP = models.IntegerField()
    IP = models.IntegerField()

    def __str__(self):
        return self.Item+" "+str(self.Index)



class SerachingFarmer(models.Model):
    Town = models.CharField(max_length=100)
    Quantity = models.IntegerField()
    Item = models.CharField(max_length=100)
    PinCode = models.IntegerField()


class RegisterFarmer(models.Model):
    UserName = models.CharField(max_length=100)
    Password = models.IntegerField()
    ConformPassword = models.IntegerField()
    Name = models.CharField(max_length=100)
    Phone_Number = PhoneField(blank=True)
    Item = models.CharField(max_length=100)
    Organic_Inorganic = models.IntegerField()
    City = models.CharField(max_length=100)
    Quantity = models.IntegerField()
    Availability = models.IntegerField()
    PinCode = models.IntegerField()

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
    Item = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Organic_Inorganic = models.IntegerField()
    Quantity = models.IntegerField()
    Availability = models.IntegerField()
    PinCode = models.IntegerField()



        