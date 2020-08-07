from django.db import models

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.utils import timezone
from django.core.validators import MaxLengthValidator, MinLengthValidator

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin, AbstractUser

from django.core.mail import send_mail, BadHeaderError

# Create your models here.
# BeforeYouStart

class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Please enter an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    email = models.EmailField(_('Email'), unique=True)
    nickname = models.CharField(_('Nickname'), max_length=150, blank=False, unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email

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
    public = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, null=True, related_name='liked_quiz', blank=True)
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
    explanation = models.TextField(blank=True, null=True)
    answered_user = models.ManyToManyField(User, null=True, blank=True, related_name='answered_quiz')
    choice1_count = models.ManyToManyField(User, null=True, blank=True, related_name='choice1_users')
    choice2_count = models.ManyToManyField(User, null=True, blank=True, related_name='choice2_users')
    choice3_count = models.ManyToManyField(User, null=True, blank=True, related_name='choice3_users')
    choice4_count = models.ManyToManyField(User, null=True, blank=True, related_name='choice4_users')
    first_try_correct = models.ManyToManyField(User, null=True, blank=True, related_name='question_first_try_correct')

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

    def total_likes(self):
        return self.likes.count()

    def total_user_answered(self):
        return self.answered_user.count()

class DescriptionDetail(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.name

class ArticlesCategory(models.Model):
    name = models.CharField(null=True, max_length=255)
    slug = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name

class Articles(models.Model):
    title = models.CharField(null=True, max_length=255)
    title_slug=models.TextField(max_length=100, null=True, blank=False, unique=True)
    likes = models.ManyToManyField(User, null=True, related_name='liked_article')
    category2 = models.ForeignKey(ArticlesCategory, null=True, blank=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField(ArticlesTag, null=True, blank=True)
    content = MarkdownxField(null=True)
    summary = models.TextField(null=True, blank=True, max_length=200)
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

    def total_likes(self):
        return self.likes.count()

class ArticleImage(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    article_image = models.ImageField(upload_to='article_image/', null=True, blank=True)

class ArticleReferences(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    reference = models.CharField(max_length=500, null=True, blank=True)

#  Article Comments

class Comment(models.Model):
    article = models.ForeignKey(
        Articles, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    author = models.CharField(max_length=50, null=True, blank=True)
    login_author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    aki = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text

class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.CharField(max_length=50)
    login_author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    aki = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text

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

# Correction

class Correction(models.Model):
    title = models.TextField(max_length=100, null=True, blank=True, default="New!")
    title_slug=models.TextField(max_length=100, null=True, blank=False, unique=True)
    public = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    login_name = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="submitted_corrections")
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


