from django.db import models
from datetime import date
# Create your models here.
from django.utils import timezone

class Jogos(models.Model):
    mandante = models.CharField(max_length=100)
    visitante = models.CharField(max_length=100)
    liga = models.CharField(max_length=100)
    goals_last5 = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    approve_details = models.CharField(max_length=300)
    game_date = models.DateTimeField(default=timezone.now)
    consolidado = models.JSONField(null=True)

    def __str__(self):
        return f'{self.mandante} vS {self.visitante}'
