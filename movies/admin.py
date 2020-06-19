from django.contrib import admin
from django import forms

from .models import Category, Genre, MovieShorts, Movie, Actor, Rating, RatingStar, Reviews, Serials
# Register your models here.


from ckeditor_uploader.widgets import CKEditorUploadingWidget



class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)

class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'), )
        }),
        (None, {
            'fields': ('description', 'poster')
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genre', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fess_in_usa', 'fess_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')


    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = "Опубликовать"
    publish.allowed_permission = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permission = ('change', )


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'movie', 'id')
    readonly_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ('name', 'age')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('star', 'movie', 'ip')


@admin.register(MovieShorts)
class MovieShortsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('title', 'movie')




admin.site.register(RatingStar)
admin.site.register(Serials)


admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'