from django.contrib import admin
from quiz.models import *
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
    list_display = ('question', 'level', 'category',)
    search_fields = ['question', 'choice1','choice2','choice3','choice4','descriptiondetail__word']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ['order']

class BasicsImage(admin.TabularInline):
    model = BasicImage
    extra = 1

class BasicsAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'category','order')
    list_editable = ['order']
    inlines = [BasicsImage]


#Aritlces

class ArticlesAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'category','order')
    list_editable = ['order']

#lesson

class LessonBodyInline(admin.TabularInline):
    model = LessonBody
    extra = 4

class LessonQuestionInline(admin.TabularInline):
    model = LessonQuestion
    extra = 2

class LessonVocabularyInline(admin.TabularInline):
    model = LessonVocabulary
    extra = 4

class LessonGrammarInline(admin.TabularInline):
    model = LessonGrammar
    extra = 2

class LessonGrammarAdmin(MarkdownxModelAdmin):
    list_display = ('grammar', 'lesson')

class LessonKanjiInline(admin.TabularInline):
    model = LessonKanji
    extra = 3

class LessonAdmin(MarkdownxModelAdmin):
    inlines = [
        LessonBodyInline,
        LessonQuestionInline,
        LessonVocabularyInline,
        LessonGrammarInline,
        LessonKanjiInline,
    ]
    list_display = ('title', 'chapter', 'number')
    list_editable = ('chapter', 'number')


#BeforeYouStart
admin.site.register(BeforeYouStart, MarkdownxModelAdmin)

#quiz
admin.site.register(Level)
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(Quiz, QuizAdmin)

#Basics
admin.site.register(BasicsCategory)
admin.site.register(Basics, BasicsAdmin)

#Aritlces
admin.site.register(ArticlesCategory)
admin.site.register(Articles, ArticlesAdmin)

#Lessons
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonGrammar, LessonGrammarAdmin)