from django.contrib import admin
from quiz.models import Category, Tag, Quiz, Level, DescriptionDetail,ChoicesDetail
from markdownx.admin import MarkdownxModelAdmin
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.



class DescriptionDetailInline(admin.TabularInline):
    model = DescriptionDetail
    extra = 4

class ChoiceDetailInline(admin.TabularInline):
    model = ChoicesDetail
    extra = 1



class QuizAdmin(SummernoteModelAdmin):
    summernote_fields = 'description'
    inlines = [
        DescriptionDetailInline,
        ChoiceDetailInline
    ]

admin.site.register(Level)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Quiz, QuizAdmin)

