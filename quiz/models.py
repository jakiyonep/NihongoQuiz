from django.db import models
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

    def __str__(self):
        return self.name


class Quiz(models.Model):
    question = models.CharField(blank=False, null=False, max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    choice1 = models.CharField(blank=True, max_length=100)
    choice2 = models.CharField(blank=True, max_length=100)
    choice3 = models.CharField(blank=True, max_length=100)
    choice4 = models.CharField(blank=True, max_length=100)
    class Answer(models.IntegerChoices):
        choice1 = 1
        choice2 = 2
        choice3 = 3
        choice4 = 4

    answer = models.IntegerField(choices=Answer.choices, null = True)

    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank =True)
    public = models.BooleanField(default=False)



    class Meta:
        ordering = ['-updated']

    def save(self, *args, **kwargs):
        if self.public and not self.publish:
            self.publish = timezon.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question
