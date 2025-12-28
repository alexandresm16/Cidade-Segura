# accounts/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    reputation_score = models.FloatField(default=1)
    reports_approved = models.PositiveIntegerField(default=0)
    reports_rejected = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
