from django.contrib import admin
from .models import Post, Category

from modeltranslation.admin import TranslationAdmin # импортируем модель админки


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ['title', 'date', 'rating'] # генерируем список имён всех полей для более красивого отображения
    list_filter = ('rating', 'date')
    search_fields = ('title', )


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostModelAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(Category)

