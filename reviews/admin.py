from django.contrib import admin
from reviews.models import Review


@admin.register(Review)
class ReviewDisplay(admin.ModelAdmin):
    def get_movie(self, obj):
        return obj.movie.title
    
    # list_display는 ManyToManyField 미지원
    list_display = [
        'get_movie',
        'user',
        'content',
        'rating',
        'created_at',
        'updated_at',
    ]
    fields = [
        'movie',
        'user',
        'content',
        'rating',
        'like',
    ]
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    list_filter = [
        'movie',
        'user',
        'rating',
    ]
    search_fields = [
        'movie',
        'user',
    ]