# Generated by Django 3.1 on 2021-01-30 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0028_auto_20210130_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogjapanese1detail',
            name='definition',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='blogjapanese1detail',
            name='usage',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='blogjapanese1detail',
            name='yomi',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='blogjapanese2detail',
            name='definition',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='blogjapanese2detail',
            name='usage',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='blogjapanese2detail',
            name='yomi',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
