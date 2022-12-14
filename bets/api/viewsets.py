from rest_framework import viewsets
from bets.api import serializers
from bets import models
import betvalidators
import time

class JogosViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.JogosSerializer
    queryset = models.Jogos.objects.all()
    http_method_names = ['get'] #pra aparecer apenas o get

    def callscraping(self):
        betvalidators.betvalidator()