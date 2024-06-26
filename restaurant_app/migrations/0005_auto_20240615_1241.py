# Generated by Django 3.2.1 on 2024-06-15 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0004_alter_profile_bookings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Book_Table',
        ),
        migrations.AlterField(
            model_name='profile',
            name='bookings',
            field=models.ManyToManyField(blank=True, related_name='_restaurant_app_profile_bookings_+', to='restaurant_app.Profile'),
        ),
    ]
