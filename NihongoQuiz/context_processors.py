from django.db.models import Count, Q

from quiz.models import Category, Tag, Level, ArticlesTag, ArticlesCategory, BlogTag, BlogCategory


def common(request):
    context = {
        'categories': Category.objects.annotate(
            num_posts=Count('quiz', filter=Q(quiz__public=True))),
        'tags': Tag.objects.annotate(
            num_posts=Count('quiz', filter=Q(quiz__public=True))),
        'levels': Level.objects.annotate(
            num_posts=Count('quiz', filter=Q(quiz__public=True))),
        'article_tags': ArticlesTag.objects.annotate(
            num_articles=Count('articles', filter=Q(articles__public=True))),
        'article_categories': ArticlesCategory.objects.annotate(
            num_articles=Count('articles', filter=Q(articles__public=True))),
        'blog_tags': BlogTag.objects.annotate(
            num_blogs=Count('tag_blogs', filter=Q(tag_blogs__public=True))),
        'blog_categories': BlogCategory.objects.annotate(
            num_blogs=Count('category_blogs', filter=Q(category_blogs__public=True))),
    }
    return context
