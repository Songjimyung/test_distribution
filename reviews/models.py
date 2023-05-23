from django.db import models
from users.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    content = models.TextField("내용")
    created_at = models.DateTimeField("리뷰생성일", auto_now_add=True)
    updated_at = models.DateTimeField("리뷰변경일", auto_now=True)
    like = models.ManyToManyField(User, related_name="likes")

    def __str__(self):
        return str(self.content)
    