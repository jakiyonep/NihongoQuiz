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

class QuizAdmin(admin.ModelAdmin):

    inlines = [
        DescriptionDetailInline,
        ChoiceDetailInline
    ]
    list_display = ('question', 'level', 'category',)
    search_fields = ['question', 'choice1','choice2','choice3','choice4','descriptiondetail__word']
    exclude = ('answered_user', 'first_try_correct', 'choice1_count', 'choice2_count', 'choice3_count', 'choice4_count', 'likes')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ['order']

class BasicsImage(admin.TabularInline):
    model = BasicImage
    extra = 1

class BasicsAdmin(MarkdownxModelAdmin):
    list_display = ('title','category','order','public')
    list_editable = ['order']
    inlines = [BasicsImage]


#Aritlces

class ArticlesImage(admin.TabularInline):
    model = ArticleImage
    extra = 1

class ArticlesReferences(admin.TabularInline):
    model = ArticleReferences
    extra = 1

class ArticlesAdmin(MarkdownxModelAdmin):
    list_display = ('title','order','public')
    list_editable = ['order',]
    inlines = [
        ArticlesReferences,
        ArticlesImage,
               ]

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

class LessonGrammarImage(admin.TabularInline):
    model = LessonGrammarImage
    extra = 1

class LessonGrammarAdmin(MarkdownxModelAdmin):
    list_display = ('grammar', 'lesson')
    inlines = [LessonGrammarImage]

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

class BeforeImage(admin.TabularInline):
    model = BeforeYouStartImage
    extra = 1

class BeforeYouStartAdmin(MarkdownxModelAdmin):
    inlines = [BeforeImage]

class CorrectionInline(admin.TabularInline):
    model=CorrectionSentences
    extra = 3

class CorrectionAdmin(MarkdownxModelAdmin):
    inlines=[
        CorrectionInline,
    ]
    list_display = ('title','public')
    list_editable = ['public']


# Blog

class BlogJapanese1(admin.TabularInline):
    model = BlogJapanese1
    extra = 1


class BlogDetail1(admin.TabularInline):
    model = BlogJapanese1Detail
    extra = 2


class BlogJapanese2(admin.TabularInline):
    model = BlogJapanese2
    extra = 1


class BlogDetail2(admin.TabularInline):
    model = BlogJapanese2Detail
    extra = 2


class BlogAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'public')
    list_editable = ['public']
    inlines = (
        BlogJapanese1,
        BlogDetail1,
        BlogJapanese2,
        BlogDetail2,
    )


#User
admin.site.register(User)

#BeforeYouStart
admin.site.register(BeforeYouStart, BeforeYouStartAdmin)

#quiz
admin.site.register(Level)
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(Quiz, QuizAdmin)

#Basics
admin.site.register(BasicsCategory)
admin.site.register(Basics, BasicsAdmin)

#Aritlces
admin.site.register(ArticlesTag)
admin.site.register(ArticlesCategory)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Comment)
admin.site.register(Reply)

#Lessons
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonGrammar, LessonGrammarAdmin)

#Correction
admin.site.register(Correction, CorrectionAdmin)

#Blog
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory)
admin.site.register(BlogTag)