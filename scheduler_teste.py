from apscheduler.schedulers.background import BackgroundScheduler
from bets.api.viewsets import JogosViewSet
import betvalidators
import time

def callscraping(self):
    betvalidators.betvalidator()
    for i in range(20):
        print(i)
        time.sleep(1)


scheduler = BackgroundScheduler()
jogos = JogosViewSet()
scheduler.add_job(jogos.callscraping, "interval", minutes=5, id="jogos_001", replace_existing=True)
scheduler.start()