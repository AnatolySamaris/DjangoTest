from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from .models import Employee, Payment, Dayoff, Application
from .forms import ApplicationForm

import os, mimetypes
from PyPDF2 import PdfReader
from fpdf import FPDF

import datetime


def prepare_text(text: list, line_width=80) -> list:
    '''
    Функция обрабатывает список строк, переписывая их так, чтобы
    в итоговом файле количество слов в строке было соразмерно
    свободному месту в строке.
    '''
    words = []  # Собираем список слов из всех строк
    for line in text:
        words.extend(line.split())
    new_text = []
    line = ''
    for word in words:
        if len(line) + len(word) <= line_width:
            line += ' ' + word
        else:
            new_text.append(line)
            line = word
    if line: # Если осталась неполная последняя строка
        new_text.append(line)
    return new_text


def make_application(template: str, data: dict, line_width=80):
    in_file = PdfReader(template)
    page = in_file.pages[0].extract_text()
    for data_pair in data.items():  # Подставляем свои данные
        page = page.replace(*data_pair)
    page = page.split('\n')
    page = list(map(lambda x: x.strip(), page))
    # Обработка текста заявления после строки "Заявление об отгуле"
    page[6:-3] = prepare_text(page[6:-1])

    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.add_font('Times', '', os.path.join(settings.MEDIA_ROOT, 'fonts', 'TimesNewRoman', 'timesnrcyrmt.ttf'), uni=True)
    pdf.set_font('times', size=14)

    line = 0
    while 'Заявление' not in page[line]: # До заголовка заявления
        pdf.cell(0, 10, txt=page[line], ln=1, align='R')
        line += 1
    pdf.cell(0, 10, txt=page[line], ln=1, align='C') # Заголовок заявления
    line += 1
    pdf.set_font('times')
    while line != len(page)-1: # Основной текст заявления
        pdf.cell(0, 10, txt=page[line], ln=1, align='L')
        line += 1
    pdf.cell(0, 10, txt=page[line], ln=1, align='R') # Дата и подпись

    filepath = os.path.join(settings.MEDIA_ROOT, 'applications', 'DayoffApplication.pdf')
    pdf.output(filepath)

    with open(filepath, 'rb') as file:  # Скачиваем файл
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(file, 
                                content_type=mime_type,
                                headers={
                                    'Content-Disposition': 'attachment; filename=%s' %filepath
                                })
        return response


@login_required
def profile(request):
    user = Employee.objects.get(user=request.user)
    # Перечисляем данные явно, иначе не показывает фото
    user_data = {
        'name': user.name,
        'birthday': user.birthday,
        'salary': user.salary,
        'photo': user.photo
    }
    return render(request, 'profile.html', user_data)


@login_required
def payments(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'payments.html', {'payments': payments})


@login_required
def dayoff(request):
    try:
        dayoff = Dayoff.objects.filter(user=request.user)
        return render(request, 'dayoff.html', {'dayoff': dayoff})
    except:
        return render(request, 'dayoff.html', {'dayoff': None})


@login_required 
def application_form(request):
    form = ApplicationForm()
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # Предполагается, что мы храним только один шаблон заявления
            pattern = Application.objects.all()[0]
            user = Employee.objects.get(user=request.user)
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            date_delta = date_to - date_from
            file_data = {
                '{{company}}': pattern.company_name,
                '{{SEO_name}}': pattern.seo_name,
                '{{employee_name}}' : user.name,
                '{{reason}}': form.cleaned_data['reason'],
                '{{date_from}}': date_from.strftime('%d.%m.%Y'),
                '{{amount_days}}': str(date_delta.days),
                '{{current_data}}': str(datetime.datetime.today().strftime('%d.%m.%Y')),
            }
            #new_dayoff = Dayoff(request.user, date_from=date_from, date_to=date_to, reason=form.cleaned_data['reason'])
            #new_dayoff.save()
            #return redirect(reverse('dayoff'))
            return make_application(pattern.application_file, file_data)
        else:
            return render(request, 'application_form.html', {'form': form})
    else:
        return render(request, 'application_form.html', {'form': form})
