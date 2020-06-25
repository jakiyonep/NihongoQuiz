# Generated by Django 3.0.6 on 2020-06-25 04:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0046_correction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correction',
            name='text',
            field=models.TextField(max_length=500, validators=[django.core.validators.MaxLengthValidator(5, 'It should be less than 500 characters! Suimasen!'), django.core.validators.MinLengthValidator(1, 'Text is empty')]),
        ),
        migrations.AlterField(
            model_name='correction',
            name='type',
            field=models.IntegerField(blank=True, choices=[(1, 'Casual'), (2, 'Formal'), (3, 'SUPER formal')], null=True),
        ),
    ]
