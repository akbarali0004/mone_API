from apscheduler.schedulers.background import BackgroundScheduler
from zoneinfo import ZoneInfo
from database import get_db
from crud import activate_tasks, delete_task_proofs
from .delete_upload_files import delete_upload_files

# Scheduler yaratish
scheduler = BackgroundScheduler(timezone=ZoneInfo("Asia/Tashkent"))


def daily_jobs():
    db = next(get_db())
    try:
        activate_tasks(db)
        delete_task_proofs(db)
    finally:
        db.close()

    delete_upload_files()


# Har kuni 00:00 da ishga tushirish
scheduler.add_job(func=daily_jobs, trigger='cron', hour=16, minute=38)

if not scheduler.running:
    scheduler.start()
