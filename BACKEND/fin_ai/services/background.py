import threading
import time
from datetime import datetime
from fin_ai.database import SessionLocal
from fin_ai.models.models import PaperTrade
from fin_ai.routes.trading import settle_trade_by_id

CHECK_INTERVAL_SECONDS = 60  # check every 60 seconds (adjust as needed)


def _worker_loop(stop_event):
    while not stop_event.is_set():
        try:
            now = datetime.utcnow()
            db = SessionLocal()
            try:
                due_trades = db.query(PaperTrade).filter(PaperTrade.settled == False, PaperTrade.target_date <= now).all()
                for t in due_trades:
                    try:
                        settled = settle_trade_by_id(t.id)
                        if settled:
                            print(f"[background] Settled trade {t.id} for user {t.user_id}")
                    except Exception as e:
                        print(f"[background] Error settling trade {t.id}: {e}")
            finally:
                db.close()
        except Exception as e:
            print(f"[background] Worker error: {e}")
        # sleep until next check
        stop_event.wait(CHECK_INTERVAL_SECONDS)


class BackgroundWorker:
    def __init__(self):
        self._stop = threading.Event()
        self._thread = threading.Thread(target=_worker_loop, args=(self._stop,), daemon=True)

    def start(self):
        if not self._thread.is_alive():
            self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=5)


_bg_worker = None

def start_background_worker():
    global _bg_worker
    if _bg_worker is None:
        _bg_worker = BackgroundWorker()
        _bg_worker.start()


def stop_background_worker():
    global _bg_worker
    if _bg_worker is not None:
        _bg_worker.stop()
        _bg_worker = None
