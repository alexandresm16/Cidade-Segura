from django.db import models
from occurrences.models import Occurrence
from accounts.models import User


# Create your models here.
class OccurrenceVote(models.Model):
    VOTE_CHOICES = [
        ('confirm', 'Confirmo'),
        ('deny', 'Não procede'),
        ('unsure', 'Informação insuficiente'),
    ]

    occurrence = models.ForeignKey(
        Occurrence, on_delete=models.CASCADE, related_name='votes'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)
    weight = models.FloatField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('occurrence', 'user')
