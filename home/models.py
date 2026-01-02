from django.db import models
from django.core.exceptions import ValidationError

class CidadeSegura(models.Model):
    telefone = models.CharField(max_length=20, blank=True, null=True)
    whatsApp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    descricao = models.TextField()
    alerta = models.TextField()
    anuncio = models.TextField()
    link_whatsapp = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Cidade Segura'
        verbose_name_plural = 'Cidade Segura'

    def save(self, *args, **kwargs):
        if not self.pk and CidadeSegura.objects.exists():
            raise ValidationError('Só é permitido criar uma única instância da Cidade Segura.')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email



class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=100)
    humidity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"