from django.db import models
from django import forms
from django.core.exceptions import ValidationError

from django import forms

# Create your models here.
def validate_integer_only(value):
    if not value.isnumeric():
        raise ValidationError("Тільки числові значення")

class Calculationdb(models.Model):
    input_data = models.IntegerField(max_length=100, validators = [validate_integer_only], default ='0')


class Calculation(forms.ModelForm):
    class Meta:
        model = Calculationdb
        labels = {
            'input_data': ''
        }
        fields = ['input_data']

