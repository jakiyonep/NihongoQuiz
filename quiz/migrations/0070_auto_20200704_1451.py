# Generated by Django 3.0.6 on 2020-07-04 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0069_auto_20200704_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='category2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.ArticlesCategory'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='category',
            field=models.IntegerField(blank=True, choices=[(1, 'Nihongo'), (2, 'Nihon')], null=True),
        ),
    ]
