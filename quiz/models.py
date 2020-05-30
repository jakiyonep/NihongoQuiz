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

    class Meta:
        ordering = ['name']

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
    level = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    question = models.TextField(blank=False, null=False, max_length=200)
    choice_long = models.BooleanField(default=False)
    choice1 = models.TextField(blank=True, max_length=100)
    choice2 = models.TextField(blank=True, max_length=100)
    choice3 = models.TextField(blank=True, max_length=100)
    choice4 = models.TextField(blank=True, max_length=100)

    class Answer(models.IntegerChoices):
        choice1 = 1
        choice2 = 2
        choice3 = 3
        choice4 = 4

    answer = models.IntegerField(choices=Answer.choices, null=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(auto_now=True, blank=True, null=True)
    public = models.BooleanField(default=True)

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
    word = models.CharField(blank=True, max_length=100)
    yomi = models.CharField(blank=True, max_length=100)
    definition = models.CharField(blank=True, max_length=100)
    usage = models.CharField(blank=True, max_length=100)
    example_ja = models.TextField(blank=True, max_length=100)
    example_yomi = models.TextField(blank=True, max_length=100)
    example_en = models.TextField(blank=True, max_length=100)

class ChoicesDetail(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    choice_explanation_1 = models.CharField(blank=True, max_length=100)
    choice_explanation_2 = models.CharField(blank=True, max_length=100)
    choice_explanation_3 = models.CharField(blank=True, max_length=100)
    choice_explanation_4 = models.CharField(blank=True, max_length=100)