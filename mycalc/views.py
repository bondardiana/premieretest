from django.shortcuts import render, redirect
from django import forms
# Create your views here.
from .models import Calculation, Calculationdb
from django.http import HttpResponse

from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.shortcuts import render
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

fp2 = "static/fonts/Adine_Kirnberg_Regular.ttf"
pdfmetrics.registerFont(TTFont('Adine_Kirnberg_Regular',  fp2))

datas = {
        '1': ['Салати', 'Салат Цезар з куркою та беконом',  240, 'salad_cesar.jpg'],
        '2': ['Салати', 'Салат Грецький',  155, 'salad_greek.jpg'],
        '3': ['Салати', 'Теплий Салат з філе міньйон',270, 'salad_cesar.jpg'],
        '4': ['Салати', 'Салат з лососем та авокадо',  360, 'salad_cesar.jpg'],
        '5': ['Салати', 'Салат з курячою печінкою', 165, 'salad_cesar.jpg'],
        '6': ['Салати', "Салат олів'є з телятиною", 165, 'salad_cesar.jpg'],
        '7': ['Салати', "Салат з капустою, огірком та редисом",55, 'salad_cabage.jpg'],
        '8': ['Супи', "Солонка м'ясна", 175, 'salad_cesar.jpg'],
        '9': ['Супи', "Окрошка з телятиною", 185, 'salad_cesar.jpg'],
        '10': ['Супи', "Борщ з яловичими ребрами", 185, 'soup_borsch.jpg'],
        '11': ['Супи', "Крем-суп грибний",  125, 'salad_cesar.jpg'],
        '12': ['Супи', "Бульйон з домашньою лапшою та яйцем", 115, 'soup_lapsha.jpg']}


def generate_pdf(all_data):

    mytable = [['Категорія', 'Блюдо', 'Ціна', 'Кількість', 'Всього']]
    for i, e in enumerate(all_data):
        #e = element.cleaned_data['element']
        print('lol')
        print(i, e)
        n = e['input_data']
        if n != 0:
            r = datas[str(i + 1)]
            row = [r[0], r[1], r[2], n, int(n)*int(r[2])]
            mytable.append(row)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Adine_Kirnberg_Regular'),
        ('FONTSIZE', (0, 0), (-1, -1), 22),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
    ])

    table = Table(mytable)
    table.setStyle(style)

    filename = "table_example.pdf"
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    pdf.build([table])
    return filename


def calculation(request):
    all_data = []
    if request.method == 'POST':
        for i in range(0, 13):
            form = Calculation(request.POST, prefix=f'form{i}')
            if form.is_valid():
                data = form.cleaned_data  # Get the cleaned data from the form
                all_data.append(data)

        pdf_name = generate_pdf(all_data)

        with open(pdf_name, "rb") as file:
            response = HttpResponse(file.read(), content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="example.pdf"'

        #response = FileResponse(mypdf)
        return response
        #return render(request, 'success.html')

    else:
        forms = [Calculation(prefix=f'form{i}') for i in range(20)]


    #return render(request, 'my_form.html', {'forms': forms, 'datas': datas})
    return render(request, 'my_form.html', {'forms_data': zip(forms, [[x[0], x[1]] for x in datas.values()])})
