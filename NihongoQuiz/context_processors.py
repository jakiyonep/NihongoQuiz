from django.db.models import Count, Q

from quiz.models import Category, Tag, Level, ArticlesTag


def common(request):
    context = {
        'categories': Category.objects.annotate(
            num_posts=Count('quiz', filter=Q(quiz__public=True))),
        'tags': Tag.objects.annotate(
            num_posts=Count('quiz', filter=Q(quiz__public=True))),
        'levels': Level.objects.annotate(
            num_posts=Count('quiz', filter=Q(quiz__public=True))),
        'article_tags': ArticlesTag.objects.annotate(
            num_posts=Count('articles', filter=Q(articles__public=True))),
    }
    return context
