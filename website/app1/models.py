from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Movie(models.Model):
    Movie_id = models.IntegerField(primary_key=True)
    Movie_name = models.CharField(max_length=128)
    Movie_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    #link to min/max resource: https://stackoverflow.com/questions/42425933/how-do-i-set-a-default-max-and-min-value-for-an-integerfield-django
    Movie_year = models.IntegerField()
    Movie_genre = models.CharField(max_length=128)