from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name

class Quiz(models.Model):
    description = models.TextField(blank=True)
    public = models.BooleanField(default=True)
    level = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    question = models.TextField(blank=False, null=False, max_length=200)
    question_yomi = models.TextField(blank=True, max_length=200)
    question_en = models.TextField(blank=True, max_length=200)
    choice_long = models.BooleanField(default=False)
    choice1 = models.TextField(blank=True, max_length=100)
    choice1_detail = models.TextField(blank=True, max_length=100)
    choice2 = models.TextField(blank=True, max_length=100)
    choice2_detail = models.TextField(blank=True, max_length=100)
    choice3 = models.TextField(blank=True, max_length=100)
    choice3_detail = models.TextField(blank=True, max_length=100)
    choice4 = models.TextField(blank=True, max_length=100)
    choice4_detail = models.TextField(blank=True, max_length=100)

    class Answer(models.IntegerChoices):
        choice1 = 1
        choice2 = 2
        choice3 = 3
        choice4 = 4

    answer = models.IntegerField(choices=Answer.choices, null=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(auto_now=True, blank=True, null=True)


    class Meta:
        ordering = ['-updated']

    def markdown(self):
        return markdownify(self.description)

    def save(self, *args, **kwargs):
        if self.public and not self.publish:
            self.publish = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

class DescriptionDetail(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    word = models.CharField(blank=True, max_length=200)
    yomi = models.CharField(blank=True, max_length=200)
    definition = models.CharField(blank=True, max_length=200)
    usage = models.CharField(blank=True, max_length=200)
    example_ja = models.TextField(blank=True, max_length=200)
    example_yomi = models.TextField(blank=True, max_length=200)
    example_en = models.TextField(blank=True, max_length=200)

class ChoicesDetail(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    choice_explanation_1 = models.CharField(blank=True, max_length=200)
    choice_explanation_2 = models.CharField(blank=True, max_length=200)
    choice_explanation_3 = models.CharField(blank=True, max_length=200)
    choice_explanation_4 = models.CharField(blank=True, max_length=200)


class BasicsCategory(models.Model):
    name = models.CharField(null=True, max_length=255)
    slug = models.CharField(blank=False, max_length=255)
    order = models.IntegerField(null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Basics(models.Model):
    title = models.CharField(null=True, max_length=255)
    category = models.ForeignKey(BasicsCategory, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    order = models.IntegerField(null=True)
    public = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


#Lessons

class Lesson(models.Model):
    chapter = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    title = models.TextField(null=True, max_length=300)
    public = models.BooleanField(default=True)


    class Meta:
        ordering = ['chapter']



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class LessonBody(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    person = models.CharField(null=True, max_length=300, blank=True)
    sentence = models.TextField(null=True, max_length=300, blank=True)
    sentence_yomi = models.TextField(null=True, max_length=300, blank=True)
    sentence_en = models.TextField(null=True, max_length=300, blank=True)


class LessonVocabulary(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    word = models.CharField(blank=True, max_length=300, null=True)
    yomi = models.CharField(blank=True, max_length=300, null=True)
    definition = models.CharField(blank=True, max_length=300, null=True)
    usage = models.CharField(blank=True, max_length=300, null=True)

class LessonQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    question = models.TextField(null=True, max_length=300, blank=True)
    question_en = models.TextField(null=True, max_length=300, blank=True)
    answer = models.TextField(null=True, max_length=300, blank=True)
    answer_en = models.TextField(null=True, max_length=300, blank=True)

class LessonGrammar(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    grammar = models.CharField(null=True, max_length=300)
    desc = models.TextField(null=True, max_length=1500)

    def __str__(self):
        return self.grammar

class LessonKanji(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    kanji = models.CharField(null=True, max_length=300, blank=True)
    definition = models.CharField(null=True, max_length=300, blank=True)
    yomi = models.CharField(null=True, max_length=300, blank=True)
    example = models.TextField(null=True, max_length=300, blank=True)
    example_en = models.TextField(null=True, max_length=300, blank=True)

