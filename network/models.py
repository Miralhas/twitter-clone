from django.db import models
from django.urls import reverse

from accounts.models import User

# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="tweets_liked")

    def __str__(self):
        return f"{self.pk}"
    
    def get_absolute_path(self):
        return reverse("network:tweet_detail", args=(self.user.username, self.pk))

    class Meta:
        ordering = ["-date"]


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content[:25]}"


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, null=True)
    following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user} -> {self.following_user}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_user'], name='unique_followers')
        ]