from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active',
                    'is_staff', 'confirmation_code',
                    'first_name', 'last_name', 'bio',
                    'role')
    search_fields = ('username',)
    list_filter = ('email',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    search_fields = ('name', 'year')
    list_filter = ('name', 'year',)
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('genre', 'title')
    search_fields = ('genre', 'title')
    list_filter = ('genre', 'title')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date', 'title', 'score', 'text')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date', 'review', 'text')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
