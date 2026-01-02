from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum, F, Case, When, FloatField

User = get_user_model()

# Create your models here.
class Occurrence(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Em validação'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]

    CRIME_TYPE_CHOICES = [
        ('theft', 'Furto'),
        ('robbery', 'Roubo'),
        ('assault', 'Agressão'),
        ('gunshot', 'Disparo de arma'),
        ('car', 'Acidente de trânsito'),
        ('fire', 'incêndio'),
        ('other', 'Outro'),
    ]

    reporter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='occurrences'
    )
    crime_type = models.CharField(max_length=20, choices=CRIME_TYPE_CHOICES)
    description = models.TextField(max_length=300, blank=True)
    reference = models.TextField(max_length=250, blank=True)
    logradouro = models.CharField('Logradouro', max_length=100, null=False, blank=False)
    bairro = models.CharField('Bairro', max_length=50, null=False, blank=False)
    cidade = models.CharField('Cidade', max_length=50, null=False, blank=False)
    uf = models.CharField('UF', max_length=20, null=False, blank=False)
    cep = models.CharField('CEP', max_length=9, null=False, blank=False)
    link = models.TextField(max_length=300, blank=True)

    latitude = models.DecimalField(
        'Latitude',
        max_digits=9,
        decimal_places=6,
        help_text='Latitude em graus decimais'
    )
    longitude = models.DecimalField(
        'Longitude',
        max_digits=9,
        decimal_places=6,
        help_text='Longitude em graus decimais'
    )


    occurred_at = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Denuncia'
        verbose_name_plural = 'Denuncias'
        ordering = ['-occurred_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['crime_type']),
            models.Index(fields=['cidade', 'bairro']),
            models.Index(fields=['occurred_at']),
        ]

    def __str__(self):
        return f'{self.get_crime_type_display()} - {self.bairro} - {self.cidade}/{self.uf}'

    def credibility_score(self):
        result = self.votes.aggregate(
            score=Sum(
                Case(
                    When(vote='confirm', then=F('weight')),
                    When(vote='deny', then=-F('weight')),
                    default=0,
                    output_field=FloatField()
                )
            )
        )
        return result['score'] or 0


    def update_status_by_votes(self):
        score = self.credibility_score()

        status_anterior = self.status  # salva status antigo

        if score >= 2:
            self.status = 'approved'
        elif score <= -3:
            self.status = 'rejected'
        else:
            self.status = 'pending'

        self.save(update_fields=['status'])

        # Atualiza UserProfile apenas se o status mudou para approved ou rejected
        if self.status != status_anterior and self.status in ['approved', 'rejected']:
            if hasattr(self.reporter, 'profile'):
                self.reporter.profile.update_after_occurrence(self.status)