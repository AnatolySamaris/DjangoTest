from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='Пользователь')
    name = models.CharField(max_length=128, verbose_name='ФИО')
    birthday = models.DateField(verbose_name='Дата рождения')
    salary = models.FloatField(verbose_name='Зарплата')
    photo = models.ImageField(upload_to='images', verbose_name='Фото сотрудника')
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата выплаты')
    amount = models.FloatField(verbose_name='Размер выплаты')


# Данные отсюда будут использоваться при создании файла. Задаёт шаблон заявления, не больше
class Application(models.Model):
    company_name = models.CharField(max_length=216, verbose_name='Название компании')
    seo_name = models.CharField(max_length=216, verbose_name='ФИО ген. директора')
    application_file = models.FileField(upload_to='docPattern', verbose_name='Шаблон заявления')


class Dayoff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_from = models.DateField(verbose_name='От:')
    date_to = models.DateField(verbose_name='До:')
    reason = models.TextField(max_length=256, verbose_name='Причина')