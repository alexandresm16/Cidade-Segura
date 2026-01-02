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

    def update_after_occurrence(self, occurrence_status):
        """
        Atualiza os contadores e a reputação do usuário com base no status da ocorrência.
        :param occurrence_status: string: 'approved', 'rejected' ou 'pending'
        """
        if occurrence_status == 'approved':
            self.reports_approved += 1
        elif occurrence_status == 'rejected':
            self.reports_rejected += 1
        # 'pending' não altera contadores

        # Atualiza a reputação
        # Exemplo simples: reputação = 1 + approved - rejected
        # Você pode adaptar a fórmula conforme quiser
        self.reputation_score = 1 + self.reports_approved/4 - self.reports_rejected/2

        self.save(update_fields=['reports_approved', 'reports_rejected', 'reputation_score'])