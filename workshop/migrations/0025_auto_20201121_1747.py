# Generated by Django 2.2.10 on 2020-11-21 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0024_auto_20201121_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='subscribed_users',
            field=models.ManyToManyField(blank=True, related_name='club_subscriptions', to='authentication.UserProfile'),
        ),
    ]
