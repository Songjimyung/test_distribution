from django.db import models
from users.models import User
from movies.models import Movie
from django.urls import reverse


class Review(models.Model):
    RATING_CHOICES = (
        (0, 0), 
        (1, 1), 
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movies")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    content = models.TextField("내용", null=True)
    rating = models.IntegerField("평점", choices=RATING_CHOICES)
    created_at = models.DateTimeField("리뷰생성일", auto_now_add=True)
    updated_at = models.DateTimeField("리뷰변경일", auto_now=True)
    like = models.ManyToManyField(User, related_name="likes", blank=True)
    
    def get_absolute_url(self):
        if self.id:
            return reverse('review_detail_view', kwargs={"movie_id": self.movie.id, "review_id": self.id})
        else:
            return reverse('review_view', kwargs={"movie_id": self.movie.id})

    def __str__(self):
        return str(self.content)
    