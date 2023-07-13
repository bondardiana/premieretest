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
        '4': ['Салати', 'Салат з лососем та авокадо',  360, 'salad_minion.jpg'],
        '5': ['Салати', 'Салат з курячою печінкою', 165, 'salad_pechin.jpg'],
        '6': ['Салати', "Салат олів'є з телятиною", 165, 'salad_olivie.jpg'],
        '7': ['Салати', "Салат з капустою, огірком та редисом",55, 'salad_cabage.jpg'],
        '8': ['Супи', "Солонка м'ясна", 175, 'soup_solonka.jpg'],
        '9': ['Супи', "Окрошка з телятиною", 185, 'soup_okroshka.jpg'],
        '10': ['Супи', "Борщ з яловичими ребрами", 185, 'soup_borsch.jpg'],
        '11': ['Супи', "Крем-суп грибний",  125, 'soup_mashrooms.jpg'],
        '12': ['Супи', "Бульйон з домашньою лапшою та яйцем", 115, 'soup_lapsha.jpg'],
        '13': ['Десерти', "Сирники в полуничному соусі з мигдалевими пластівцями", 145, 'deserts_cheesecake.jpg'],
        '14': ['Десерти', "Чізкейк з ягідними кулями", 135, 'deserts_cheesecake2.jpg'],
        '15': ['Десерти', "Тірамісу", 125, 'deserts_tiramisu.jpg']
}


def generate_pdf(all_data):
    mytable = [['Категорія', 'Блюдо', 'Ціна', 'Кількість', 'Всього']]
    total_q = 0
    dishes = []
    for i, e in enumerate(all_data):
        #e = element.cleaned_data['element']
        n = e['input_data']
        if n != 0:
            r = datas[str(i + 1)]
            sum = int(n)*int(r[2])
            total_q += sum
            row = [r[0], r[1], r[2], n, sum]
            mytable.append(row)

            # Images pasting
            imagename = 'images/' + r[-1]
            image = Image(imagename)
            image.drawHeight = 130
            image.drawWidth = 130
            dishes.append(image)

    row = ["", "", "", "Загалом", total_q]
    mytable.append(row)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Adine_Kirnberg_Regular'),
        ('FONTSIZE', (0, 0), (-1, -1), 22),
        ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.914, 0.871, 0.804, alpha=0.5)),
        ('LINEBELOW', (0, 0), (-1, -2), 1, colors.grey),  # Add horizontal gridline below header row
        ('BACKGROUND', (0, -1), (-1, -1), colors.white),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
    ])

    table = Table(mytable)
    table.setStyle(style)

    filename = "table_example.pdf"
    pdf = SimpleDocTemplate(filename, pagesize=letter)

    #Adding Logo Image
    image = Image('images/logo.jpg')
    image.drawHeight = 100
    image.drawWidth = 170
    image.hAlign = 'LEFT'

    spacer = Spacer(1, 50)

    style_images = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align images to the top of cells
    ]
    colWidths, rowHeights = 150, 150
    if len(dishes) > 4:
        dishes_table = Table([dishes[0:4], dishes[4:]], colWidths=colWidths, rowHeights=rowHeights)
    else:
        dishes_table = Table([dishes], colWidths=colWidths, rowHeights=rowHeights)
    dishes_table.setStyle(style_images)


    #PDF BUILD
    results = [image, spacer, table, spacer, dishes_table]
    pdf.build(results)

    return filename


def calculation(request):
    all_data = []
    if request.method == 'POST':
        for i in range(0, 16):
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
