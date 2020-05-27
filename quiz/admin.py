from django.contrib import admin
from quiz.models import Category, Tag, Quiz, Level
from markdownx.admin import MarkdownxModelAdmin
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class QuizAdmin(SummernoteModelAdmin):
    summernote_fields = 'description'

admin.site.register(Level)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Quiz, QuizAdmin)
