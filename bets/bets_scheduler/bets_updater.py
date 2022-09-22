from apscheduler.schedulers.background import BackgroundScheduler
from bets.api.viewsets import JogosViewSet

def start():
    scheduler = BackgroundScheduler()
    jogos = JogosViewSet()
    scheduler.add_job(jogos.callscraping, "interval", minutes=1, id="jogos_001", replace_existing=True)
    scheduler.start()