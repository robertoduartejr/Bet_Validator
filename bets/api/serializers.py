from rest_framework import serializers
from bets.models import Jogos

class JogosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogos
        fields = ('mandante', 'visitante','liga','goals_last5','approved','approve_details','game_date')
