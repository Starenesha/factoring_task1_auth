# Generated by Django 3.0.7 on 2020-06-30 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200629_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='depart',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='accounts.Depart', verbose_name='Depart'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_employee',
            field=models.BooleanField(default=False, verbose_name='Employer'),
        ),
    ]