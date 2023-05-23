from django.db import models
from users.models import User
from movies.models import Movie
from django.urls import reverse


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movies")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    content = models.TextField("내용")
    created_at = models.DateTimeField("리뷰생성일", auto_now_add=True)
    updated_at = models.DateTimeField("리뷰변경일", auto_now=True)
    like = models.ManyToManyField(User, related_name="likes")

    def get_absolute_url(self):
        return reverse('review_detail_view', kwargs={"review_id": self.id})
    
    def __str__(self):
        return str(self.content)
    