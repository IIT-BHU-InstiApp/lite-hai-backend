# Generated by Django 2.2.13 on 2022-01-23 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mess', '0003_auto_20220123_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='total_bill',
        ),
    ]