# Generated by Django 3.2.1 on 2024-06-19 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0017_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='selected_plan_paid',
        ),
        migrations.AddField(
            model_name='profile',
            name='selected_reservation',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
