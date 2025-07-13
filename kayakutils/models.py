from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=5, default="")

    def __str__(self):
        return self.name
    
class State(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=3)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
    
class County(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.DO_NOTHING, null=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name