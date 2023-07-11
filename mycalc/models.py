from django.db import models

# Create your models here.

class Calculation(models.Model):
    input_data = models.CharField(max_length=100)
    output_data = models.CharField(max_length=100)