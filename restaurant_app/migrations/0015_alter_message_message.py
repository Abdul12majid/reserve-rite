# Generated by Django 3.2.1 on 2024-06-16 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0014_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, verbose_name='Messages'),
        ),
    ]