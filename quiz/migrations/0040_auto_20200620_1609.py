# Generated by Django 3.0.6 on 2020-06-20 07:09

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0039_auto_20200620_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='content',
            field=markdownx.models.MarkdownxField(null=True),
        ),
        migrations.AlterField(
            model_name='lessongrammar',
            name='desc',
            field=markdownx.models.MarkdownxField(null=True),
        ),
    ]
