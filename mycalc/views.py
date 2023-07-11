from django.shortcuts import render, redirect

# Create your views here.
from .models import Calculation

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def perform_calculation(input_data):
	return input_data*2
	
    
def calculation(request):
    if request.method == 'POST':
        input_data = request.POST.get('input_data')
        output_data = perform_calculation(input_data)  # Perform your calculation here
        Calculation.objects.create(input_data=input_data, output_data=output_data)
        return redirect('calculation')
    else:
        calculations = Calculation.objects.all()
        return render(request, 'calculation.html', {'calculations': calculations})