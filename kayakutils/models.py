from django.db import models

class Country(models.Model):
    class Meta:
        verbose_name_plural = "Countries"

    name = models.CharField(max_length=50, unique=True)
    abbr = models.CharField(max_length=5, default="")

    def __str__(self):
        return self.name
    
class State(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbr = models.CharField(max_length=3)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
    
class County(models.Model):
    class Meta:
        verbose_name_plural = "Counties"
        
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
    
class City(models.Model):
    class Meta:
        verbose_name_plural = "Cities"

    name = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.DO_NOTHING, null=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name