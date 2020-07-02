"""NihongoQuiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import resolve_url


"""
class BasicsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def location(self, obj):
        return resolve_url('blog:detail', pk=obj.pk)

    def lastmod(self, obj):
        return obj.created_at


sitemaps = {
    'posts': PostSitemap,
}

"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('markdownx/', include('markdownx.urls')),
]

