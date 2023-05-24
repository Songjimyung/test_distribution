from django.db import models
from users.models import User
from movies.models import Movie
from django.urls import reverse


class Review(models.Model):
    RATING_CHOICES = (
        (0.0, 0.0), 
        (0.5, 0.5), 
        (1.0, 1.0), 
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0),
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movies")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    content = models.TextField("내용", null=True)
    rating = models.FloatField("평점", choices=RATING_CHOICES)
    created_at = models.DateTimeField("리뷰생성일", auto_now_add=True)
    updated_at = models.DateTimeField("리뷰변경일", auto_now=True)
    like = models.ManyToManyField(User, related_name="likes", blank=True)

    def get_absolute_url(self):
        return reverse('review_detail_view', kwargs={"review_id": self.id})
    
    def __str__(self):
        return str(self.content)
    