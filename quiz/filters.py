import django_filters
from .models import Quiz, Articles

class QuizFilter(django_filters.FilterSet):
    class Meta:
        model = Quiz
        fields = ('level', 'category', 'tags')

class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Articles
        fields = ('category2', 'tag')