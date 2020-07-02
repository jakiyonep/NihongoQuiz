from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url, reverse

from . models import (
    Basics,
    Articles,
    Correction,
    Quiz,
    Lesson,
)



class BasicsSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Basics.objects.all()

    def location(self, obj):
        return resolve_url('quiz:basic_post', title_slug=obj.title_slug)


class ArticlesSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Articles.objects.all()

    def location(self, obj):
        return resolve_url('quiz:article_post', title_slug=obj.title_slug)

    def lastmod(self, obj):
        return obj.update

class LessonsSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Lesson.objects.all()

    def location(self, obj):
        return resolve_url('quiz:lesson_post', pk=obj.pk)

class CorrectionsSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Correction.objects.all()

    def location(self, obj):
        return resolve_url('quiz:basic_post', title_slug=obj.title_slug)

class QuizLevelPostSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Quiz.objects.all()

    def location(self, obj):
        return resolve_url('quiz:level_post', level_slug=obj.level.slug)

class QuizCategoryPostSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Quiz.objects.all()

    def location(self, obj):
        return resolve_url('quiz:category_post', category_slug=obj.category.slug)






class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return [
            'quiz:toppage',
            'quiz:quiz',
            'quiz:basics',
            'quiz:articles',
            'quiz:lessons',
            'quiz:lesson_vocabulary',
            'quiz:lesson_grammar',
            'quiz:lesson_kanji',
            'quiz:correction',
            'quiz:correction_add',
            'quiz:after_submit',
        ]

    def location(self, item):
        return reverse(item)