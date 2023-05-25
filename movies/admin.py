from django.contrib import admin
from movies.models import Movie, Genre


@admin.register(Movie)
class MovieDisplay(admin.ModelAdmin):
    # list_display는 ManyToManyField 미지원
    list_display = [
        'title',
        'release_date',
        'overview',
        'vote_average',
        'poster_path',
    ]
    readonly_fields = (
        'title',
        'release_date',
        'overview',
        'vote_average',
        'genres',
        'poster_path',
    )
    list_filter = [
        'title',
        'release_date',
        'vote_average',
        'genres',
    ]
    search_fields = [
        'title',
        'release_date',
        'overview',
        'vote_average',
        'genres',
        'poster_path',
    ]