# Generated by Django 4.2.1 on 2023-05-13 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_profile', '0008_remove_dayoff_doc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=216, verbose_name='Название компании')),
                ('director', models.CharField(max_length=216, verbose_name='ФИО ген. директора')),
                ('application_file', models.FileField(upload_to='docPatterns', verbose_name='Шаблон заявления')),
            ],
        ),
        migrations.AddField(
            model_name='dayoff',
            name='doc',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='employee_profile.application', verbose_name='Шаблон заявления'),
        ),
    ]