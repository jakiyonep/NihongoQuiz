# Generated by Django 3.0.6 on 2020-08-04 02:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import markdownx.models
import quiz.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('title_slug', models.TextField(max_length=100, null=True, unique=True)),
                ('content', markdownx.models.MarkdownxField(null=True)),
                ('summary', models.TextField(blank=True, max_length=200, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('public', models.BooleanField(default=False)),
                ('update', models.DateTimeField(auto_now=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='article_thumbnail/')),
            ],
            options={
                'ordering': ['-update'],
            },
        ),
        migrations.CreateModel(
            name='ArticlesCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ArticlesTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BasicsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.CharField(max_length=255)),
                ('order', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='BeforeYouStart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', markdownx.models.MarkdownxField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=True)),
                ('aki', models.BooleanField(default=False)),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='quiz.Articles')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Correction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, default='New!', max_length=100, null=True)),
                ('title_slug', models.TextField(max_length=100, null=True, unique=True)),
                ('public', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('text', models.TextField(max_length=500, validators=[django.core.validators.MaxLengthValidator(500, 'Text should be less than 500 characters! Suimasen!'), django.core.validators.MinLengthValidator(1, 'Text is empty')])),
                ('desc', models.TextField(blank=True, max_length=500, null=True)),
                ('type', models.IntegerField(blank=True, choices=[(1, 'SUPER Casual'), (2, 'Casual'), (3, 'Formal'), (4, 'SUPER Formal')], null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['public', '-updated'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.IntegerField(null=True)),
                ('number', models.IntegerField(null=True)),
                ('title', models.TextField(max_length=300, null=True)),
                ('public', models.BooleanField(default=False)),
                ('reading', models.BooleanField(default=False)),
                ('vocab', models.BooleanField(default=False)),
                ('exercise', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['chapter', 'number'],
            },
        ),
        migrations.CreateModel(
            name='LessonGrammar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grammar', models.CharField(max_length=300, null=True)),
                ('desc', markdownx.models.MarkdownxField(null=True)),
                ('casual', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Lesson')),
            ],
            options={
                'ordering': ['lesson', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=True)),
                ('aki', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='quiz.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('public', models.BooleanField(default=True)),
                ('question', models.TextField(max_length=200)),
                ('question_yomi', models.TextField(blank=True, max_length=200)),
                ('question_en', models.TextField(blank=True, max_length=200)),
                ('choice_long', models.BooleanField(default=False)),
                ('choice1', models.TextField(blank=True, max_length=100)),
                ('choice1_detail', models.TextField(blank=True, max_length=100)),
                ('choice2', models.TextField(blank=True, max_length=100)),
                ('choice2_detail', models.TextField(blank=True, max_length=100)),
                ('choice3', models.TextField(blank=True, max_length=100)),
                ('choice3_detail', models.TextField(blank=True, max_length=100)),
                ('choice4', models.TextField(blank=True, max_length=100)),
                ('choice4_detail', models.TextField(blank=True, max_length=100)),
                ('answer', models.IntegerField(choices=[(1, 'Choice1'), (2, 'Choice2'), (3, 'Choice3'), (4, 'Choice4')], null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('publish', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz.Category')),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='quiz.Level')),
                ('tags', models.ManyToManyField(blank=True, to='quiz.Tag')),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
        migrations.CreateModel(
            name='LessonVocabulary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('word', models.CharField(blank=True, max_length=300, null=True)),
                ('yomi', models.CharField(blank=True, max_length=300, null=True)),
                ('definition', models.CharField(blank=True, max_length=300, null=True)),
                ('usage', models.CharField(blank=True, max_length=300, null=True)),
                ('casual', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Lesson')),
            ],
            options={
                'ordering': ['lesson', 'order'],
            },
        ),
        migrations.CreateModel(
            name='LessonQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, default=1, null=True)),
                ('question', models.TextField(blank=True, max_length=300, null=True)),
                ('question_yomi', models.TextField(blank=True, max_length=300, null=True)),
                ('question_en', models.TextField(blank=True, max_length=300, null=True)),
                ('answer', models.TextField(blank=True, max_length=300, null=True)),
                ('answer_yomi', models.TextField(blank=True, max_length=300, null=True)),
                ('answer_en', models.TextField(blank=True, max_length=300, null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Lesson')),
            ],
            options={
                'ordering': ['lesson', 'id'],
            },
        ),
        migrations.CreateModel(
            name='LessonKanji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kanji', models.CharField(blank=True, max_length=300, null=True)),
                ('yomi', models.CharField(blank=True, max_length=300, null=True)),
                ('definition', models.CharField(blank=True, max_length=300, null=True)),
                ('example', models.TextField(blank=True, max_length=300, null=True)),
                ('example_yomi', models.TextField(blank=True, max_length=300, null=True)),
                ('example_en', models.TextField(blank=True, max_length=300, null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Lesson')),
            ],
            options={
                'ordering': ['lesson', 'id'],
            },
        ),
        migrations.CreateModel(
            name='LessonGrammarImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_gramamr_image', models.ImageField(blank=True, null=True, upload_to='grammar_image/')),
                ('lesson_grammar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.LessonGrammar')),
            ],
        ),
        migrations.CreateModel(
            name='LessonBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.CharField(blank=True, max_length=300, null=True)),
                ('sentence', models.TextField(blank=True, max_length=300, null=True)),
                ('sentence_yomi', models.TextField(blank=True, max_length=300, null=True)),
                ('sentence_en', models.TextField(blank=True, max_length=300, null=True)),
                ('sentence_casual', models.TextField(blank=True, max_length=500, null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Lesson')),
            ],
            options={
                'ordering': ['lesson', 'id'],
            },
        ),
        migrations.CreateModel(
            name='DescriptionDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(blank=True, max_length=200)),
                ('yomi', models.CharField(blank=True, max_length=200)),
                ('definition', models.TextField(blank=True, max_length=200)),
                ('usage', models.TextField(blank=True, max_length=200)),
                ('example_ja', models.TextField(blank=True, max_length=200)),
                ('example_yomi', models.TextField(blank=True, max_length=200)),
                ('example_en', models.TextField(blank=True, max_length=200)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='CorrectionSentences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.TextField(blank=True, max_length=50000, null=True)),
                ('corrected', models.TextField(blank=True, max_length=50000, null=True)),
                ('corrected_yomi', models.TextField(blank=True, max_length=50000, null=True)),
                ('desc', models.TextField(blank=True, max_length=50000, null=True)),
                ('correction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Correction')),
            ],
        ),
        migrations.CreateModel(
            name='ChoicesDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_explanation_1', models.CharField(blank=True, max_length=200)),
                ('choice_explanation_2', models.CharField(blank=True, max_length=200)),
                ('choice_explanation_3', models.CharField(blank=True, max_length=200)),
                ('choice_explanation_4', models.CharField(blank=True, max_length=200)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='BeforeYouStartImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('before_image', models.ImageField(blank=True, null=True, upload_to='before_image/')),
                ('before', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.BeforeYouStart')),
            ],
        ),
        migrations.CreateModel(
            name='Basics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('title_slug', models.TextField(max_length=100, null=True, unique=True)),
                ('content', markdownx.models.MarkdownxField(null=True)),
                ('order', models.IntegerField(null=True)),
                ('public', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='basics_image/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.BasicsCategory')),
                ('related_articles', models.ManyToManyField(blank=True, null=True, to='quiz.Articles')),
                ('related_basics', models.ManyToManyField(blank=True, null=True, related_name='_basics_related_basics_+', to='quiz.Basics')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='BasicImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_image', models.ImageField(blank=True, null=True, upload_to='basics_image/')),
                ('basic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Basics')),
            ],
        ),
        migrations.AddField(
            model_name='articles',
            name='category2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.ArticlesCategory'),
        ),
        migrations.AddField(
            model_name='articles',
            name='related_basics',
            field=models.ManyToManyField(blank=True, null=True, related_name='_articles_related_basics_+', to='quiz.Articles'),
        ),
        migrations.AddField(
            model_name='articles',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='quiz.ArticlesTag'),
        ),
        migrations.CreateModel(
            name='ArticleReferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=500, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Articles')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_image', models.ImageField(blank=True, null=True, upload_to='article_image/')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Articles')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス')),
                ('nickname', models.CharField(blank=True, max_length=150, unique=True, verbose_name='ニックネーム')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', quiz.models.CustomUserManager()),
            ],
        ),
    ]
