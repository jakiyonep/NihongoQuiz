# Generated by Django 3.0.6 on 2020-08-06 09:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20200806_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='choice1_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='choice2_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='choice3_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='choice4_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked_quiz', to=settings.AUTH_USER_MODEL),
        ),
    ]
