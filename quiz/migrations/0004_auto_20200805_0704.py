# Generated by Django 3.0.6 on 2020-08-04 22:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20200805_0702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='like',
        ),
        migrations.AddField(
            model_name='quiz',
            name='like',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
