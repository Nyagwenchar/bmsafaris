# tours/models.py
from django.db import models

class Tour(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    region      = models.CharField(max_length=50)
    duration    = models.PositiveSmallIntegerField(help_text="Days")
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image       = models.ImageField(upload_to='tours/')
    featured    = models.BooleanField(default=False)

    def __str__(self):
        return self.name
