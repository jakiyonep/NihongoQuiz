# Generated by Django 3.0.6 on 2020-06-09 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0028_lessonkanji_example_yomi'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['chapter', 'number']},
        ),
        migrations.AddField(
            model_name='lessonbody',
            name='reading',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lessongrammar',
            name='desc',
            field=models.TextField(null=True),
        ),
    ]
