from apscheduler.schedulers.background import BackgroundScheduler
from bets.api.viewsets import JogosViewSet


scheduler = BackgroundScheduler()
jogos = JogosViewSet()
scheduler.add_job(jogos.callscraping2, "interval", minutes=3, id="jogos_002", replace_existing=True)
scheduler.start()