# Generated by Django 2.2.13 on 2022-01-23 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess', '0004_remove_bill_total_bill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='extra_charges',
            field=models.IntegerField(default=0),
        ),
    ]
