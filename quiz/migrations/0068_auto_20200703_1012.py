# Generated by Django 3.0.6 on 2020-07-03 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0067_auto_20200702_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='category',
            field=models.IntegerField(blank=True, choices=[(1, 'Nihongo'), (2, 'Nihon')], null=True),
        ),
        migrations.AddField(
            model_name='articles',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='article_thumbnail/'),
        ),
    ]
