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







# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
