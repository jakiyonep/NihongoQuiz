# Generated by Django 3.0.6 on 2020-08-10 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0016_descriptiondetail_word_in_sentence'),
    ]

    operations = [
        migrations.AddField(
            model_name='descriptiondetail',
            name='word_form',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
