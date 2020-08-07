# Generated by Django 3.0.6 on 2020-08-06 10:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_quiz_answered_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='answered_user',
        ),
        migrations.AddField(
            model_name='quiz',
            name='answered_user',
            field=models.ManyToManyField(blank=True, null=True, related_name='answered_quiz', to=settings.AUTH_USER_MODEL),
        ),
    ]
