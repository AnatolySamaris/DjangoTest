from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Employee, Payment, Dayoff
from .forms import ApplicationForm


@login_required
def profile(request):
    if request.user.is_authenticated:
        user = Employee.objects.get(user=request.user)
        # Перечисляем данные явно, иначе не показывает фото
        user_data = {
            'name': user.name,
            'birthday': user.birthday,
            'salary': user.salary,
            'photo': user.photo
        }
        return render(request, 'profile.html', user_data)
    else:
        return redirect('login')


@login_required
def payments(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'payments.html', {'payments': payments})


@login_required
def dayoff(request):
    dayoff = Dayoff.objects.filter(user=request.user)
    return render(request, 'dayoff.html', {'dayoff': dayoff})


# Переделать в модальное с ajax или починить редирект
@login_required 
def application_form(request):
    form = ApplicationForm()
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            data = {
                'date_from': form.cleaned_data['date_from'],
                'date_to': form.cleaned_data['date_to'],
                'reason': form.cleaned_data['reason']
            }
            return redirect('dayoff')
        else:
            return render(request, 'application_form.html', {'form': form})
    else:
        return render(request, 'application_form.html', {'form': form})
