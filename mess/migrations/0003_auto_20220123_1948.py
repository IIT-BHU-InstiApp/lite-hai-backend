# Generated by Django 2.2.13 on 2022-01-23 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess', '0002_auto_20220123_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='total_bill',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
