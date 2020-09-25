# Generated by Django 3.0.7 on 2020-09-25 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20200925_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='c_id',
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='c_id',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='customer.CustomerRegistrationModel'),
        ),
    ]
