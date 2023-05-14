# Generated by Django 4.2.1 on 2023-05-12 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата выплаты')),
                ('amount', models.FloatField(verbose_name='Размер выплаты')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='ФИО')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('salary', models.FloatField(verbose_name='Зарплата')),
                ('photo', models.ImageField(upload_to='', verbose_name='Фото сотрудника')),
            ],
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='employee_profile.user')),
                ('login', models.CharField(max_length=20, verbose_name='Логин')),
                ('password', models.CharField(max_length=20, verbose_name='Пароль')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_profile.user'),
        ),
    ]
