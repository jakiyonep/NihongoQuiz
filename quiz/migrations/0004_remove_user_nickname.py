# Generated by Django 3.0.6 on 2020-08-03 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20200803_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
    ]
