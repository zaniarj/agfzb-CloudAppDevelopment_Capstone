from django.db import models
from django.utils.timezone import now


# models here.

class CarMake (models.Model):
    name        = models.CharField(max_length = 100)
    description = models.TextField()

    def __str__(self):
        return self.name



class CarModel(models.Model):

    types = [("SE","Sedan"),("SU", "SUV"),("WA", "WAGON"),("CR", "Cross Over"),("TR", "Truck")]


    car_make  = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name      = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    car_type  = models.CharField(max_length=2, choices= types)
    Year      = models.DateField()
    color     = models.CharField(max_length=20)

    def __str__(self):
        return self.make





class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:

    def __init__(self,car_make,car_model,car_year,dealership,name,purchase_date,review,purchase,id,sentiment=None):
        self.car_make       = car_make
        self.car_model      = car_model
        self.car_year       = car_year
        self.dealership     = dealership
        self.name           = name
        self.purchase_date  = purchase_date
        self.review         = review
        self.purchase       = purchase
        self.id             = id
        self.sentiment      = sentiment
    
    def __str__(self):
        return self.car_make + self.car_model