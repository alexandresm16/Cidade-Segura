from django.db import models
from occurrences.models import Occurrence
from accounts.models import User
from django.db.models import Sum, F, Case, When, FloatField


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
        constraints = [
            models.UniqueConstraint(
                fields=['occurrence', 'user'],
                name='unique_vote_per_user_per_occurrence'
            )
        ]

    def credibility_score(self):
        return self.votes.aggregate(
            score=Sum(
                Case(
                    When(vote='confirm', then=F('weight')),
                    When(vote='deny', then=-F('weight')),
                    default=0,
                    output_field=FloatField()
                )
            )
        )['score'] or 0

    def update_status_by_votes(self):
        score = self.credibility_score()

        if score >= 2:
            self.status = 'approved'
        elif score <= -3:
            self.status = 'rejected'
        else:
            self.status = 'pending'

        self.save(update_fields=['status'])
