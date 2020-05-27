from django.contrib import admin
from quiz.models import Category, Tag, Quiz, Level
from markdownx.admin import MarkdownxModelAdmin
# Register your models here.

admin.site.register(Level)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Quiz, MarkdownxModelAdmin)