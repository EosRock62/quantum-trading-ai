from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .self_improve import hourly_self_eval

scheduler = BackgroundScheduler(timezone="UTC")

def _job():
    # In der Starter-Version nur Logging; später echte Metriken/Bewertungen
    hourly_self_eval()

def start_scheduler():
    try:
        scheduler.add_job(_job, "interval", hours=1, id="self_eval", next_run_time=None)
        scheduler.start()
        print(f"[Scheduler] gestartet @ {datetime.utcnow().isoformat()}Z")
    except Exception as e:
        print(f"[Scheduler] Fehler: {e}")
