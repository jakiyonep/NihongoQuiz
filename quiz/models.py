from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.utils import timezone
from django.core.validators import MaxLengthValidator, MinLengthValidator

# Create your models here.
# BeforeYouStart

class BeforeYouStart(models.Model):
    content = MarkdownxField(null=True, blank=True)

    def markdown(self):
        return markdownify(self.content)


class BeforeYouStartImage(models.Model):
    before = models.ForeignKey(BeforeYouStart, on_delete=models.CASCADE)
    before_image = models.ImageField(upload_to='before_image/', null=True, blank=True)


# Quiz


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
    definition = models.TextField(blank=True, max_length=200)
    usage = models.TextField(blank=True, max_length=200)
    example_ja = models.TextField(blank=True, max_length=200)
    example_yomi = models.TextField(blank=True, max_length=200)
    example_en = models.TextField(blank=True, max_length=200)

    def markdown_definition(self):
        return markdownify(self.definition)

    def markdown_usage(self):
        return markdownify(self.usage)



class ChoicesDetail(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    choice_explanation_1 = models.CharField(blank=True, max_length=200)
    choice_explanation_2 = models.CharField(blank=True, max_length=200)
    choice_explanation_3 = models.CharField(blank=True, max_length=200)
    choice_explanation_4 = models.CharField(blank=True, max_length=200)




# Articles


class ArticlesTag(models.Model):
    name = models.CharField(null=True, max_length=255)
    slug = models.CharField(blank=False, max_length=255)
    order = models.IntegerField(null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name



class Articles(models.Model):
    title = models.CharField(null=True, max_length=255)
    title_slug=models.TextField(max_length=100, null=True, blank=False, unique=True)

    article_category = (
        (1, 'Nihongo'),
        (2, 'Nihon'),
    )
    category = models.IntegerField(choices=article_category, blank=True, null=True)
    tag = models.ManyToManyField(ArticlesTag, null=True, blank=True)
    content = MarkdownxField(null=True)
    summary = models.TextField(null=True, blank=True, max_length=100)
    order = models.IntegerField(null=True, blank=True)
    public = models.BooleanField(default=False)
    update = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='article_thumbnail/', null=True, blank=True)


    related_basics = models.ManyToManyField('self', blank=True, null=True)

    class Meta:
        ordering = ['-update']

    def __str__(self):
        return self.title

    def markdown(self):
        return markdownify(self.content)


class ArticleImage(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    article_image = models.ImageField(upload_to='article_image/', null=True, blank=True)



# Basics

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
    title_slug=models.TextField(max_length=100, null=True, blank=False, unique=True)
    category = models.ForeignKey(BasicsCategory, on_delete=models.CASCADE)
    content = MarkdownxField(null=True)
    order = models.IntegerField(null=True)
    public = models.BooleanField(default=False)
    image = models.ImageField(upload_to='basics_image/', null=True, blank=True)
    related_basics = models.ManyToManyField('self', blank=True, null=True)
    related_articles = models.ManyToManyField(Articles, blank=True, null=True )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def markdown(self):
        return markdownify(self.content)


class BasicImage(models.Model):
    basic = models.ForeignKey(Basics, on_delete=models.CASCADE)
    basic_image = models.ImageField(upload_to='basics_image/', null=True, blank=True)




# Lessons

class Lesson(models.Model):
    chapter = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    title = models.TextField(null=True, max_length=300)
    public = models.BooleanField(default=False)

    reading = models.BooleanField(default=False)
    vocab = models.BooleanField(default=False)
    exercise = models.BooleanField(default=False)

    class Meta:
        ordering = ['chapter', 'number']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class LessonBody(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    person = models.CharField(null=True, max_length=300, blank=True)
    sentence = models.TextField(null=True, max_length=300, blank=True)
    sentence_yomi = models.TextField(null=True, max_length=300, blank=True)
    sentence_en = models.TextField(null=True, max_length=300, blank=True)
    sentence_casual = models.TextField(null=True, blank=True, max_length=500)

    class Meta:
        ordering = ['lesson', 'id']


class LessonVocabulary(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    word = models.CharField(blank=True, max_length=300, null=True)
    yomi = models.CharField(blank=True, max_length=300, null=True)
    definition = models.CharField(blank=True, max_length=300, null=True)
    usage = models.CharField(blank=True, max_length=300, null=True)
    casual = models.BooleanField(default=False)

    class Meta:
        ordering = ['lesson', 'order']


class LessonQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    number = models.IntegerField(default=1, blank=True, null=True)
    question = models.TextField(null=True, max_length=300, blank=True)
    question_yomi = models.TextField(null=True, max_length=300, blank=True)
    question_en = models.TextField(null=True, max_length=300, blank=True)
    answer = models.TextField(null=True, max_length=300, blank=True)
    answer_yomi = models.TextField(null=True, max_length=300, blank=True)
    answer_en = models.TextField(null=True, max_length=300, blank=True)

    class Meta:
        ordering = ['lesson', 'id']


class LessonGrammar(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grammar = models.CharField(null=True, max_length=300)
    desc = MarkdownxField(null=True)
    casual = models.BooleanField(default=False)

    def __str__(self):
        return self.grammar

    class Meta:
        ordering = ['lesson', 'id']

    def markdown(self):
        return markdownify(self.desc)


class LessonGrammarImage(models.Model):
    lesson_grammar = models.ForeignKey(LessonGrammar, on_delete=models.CASCADE)
    lesson_gramamr_image = models.ImageField(upload_to='grammar_image/', null=True, blank=True)


class LessonKanji(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    kanji = models.CharField(null=True, max_length=300, blank=True)
    yomi = models.CharField(null=True, max_length=300, blank=True)
    definition = models.CharField(null=True, max_length=300, blank=True)
    example = models.TextField(null=True, max_length=300, blank=True)
    example_yomi = models.TextField(null=True, max_length=300, blank=True)
    example_en = models.TextField(null=True, max_length=300, blank=True)

    class Meta:
        ordering = ['lesson', 'id']


class Correction(models.Model):
    title = models.TextField(max_length=100, null=True, blank=True, default="New!")
    title_slug=models.TextField(max_length=100, null=True, blank=False, unique=True)
    public = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(max_length=500,
                            validators=[
                                MaxLengthValidator(500, 'Text should be less than 500 characters! Suimasen!'),
                                MinLengthValidator(1, 'Text is empty')
                                        ])
    desc = models.TextField(max_length=500, null=True, blank=True)
    type_choices = (
        (1, 'SUPER Casual'),
        (2, 'Casual'),
        (3, 'Formal'),
        (4, 'SUPER Formal'),
    )
    type = models.IntegerField(choices=type_choices, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta():
        ordering =['public','-updated']

    def title_new(self):
        if not self.title:
            self.title = "New!!"

        return self.title



class CorrectionSentences(models.Model):
    correction = models.ForeignKey(Correction, on_delete=models.CASCADE)
    original = models.TextField(max_length=50000, blank=True, null=True)
    corrected = models.TextField(max_length=50000, blank=True, null=True)
    corrected_yomi = models.TextField(max_length=50000, blank=True, null=True)
    desc = models.TextField(max_length=50000, blank=True, null=True)

    def markdown(self):
        return markdownify(self.desc)

    def markdown_corrected(self):
        return markdownify(self.corrected)


