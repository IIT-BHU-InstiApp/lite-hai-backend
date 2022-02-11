# Generated by Django 2.2.13 on 2022-01-23 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0015_auto_20220123_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Mess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('menu', models.URLField()),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mess.Hostel')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthlybills', models.IntegerField()),
                ('extracharges', models.IntegerField()),
                ('totalbill', models.IntegerField()),
                ('mess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mess.Mess')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.UserProfile')),
            ],
        ),
    ]
