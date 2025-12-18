from apscheduler.schedulers.background import BackgroundScheduler
from database import get_db
from crud import activate_tasks, delete_task_proofs
from .delete_upload_files import delete_upload_files

# Scheduler yaratish
scheduler = BackgroundScheduler()


def daily_jobs():
    with get_db() as db:
        activate_tasks(db)
        delete_task_proofs(db)
    delete_upload_files()


# Har kuni 00:00 da ishga tushirish
scheduler.add_job(func=daily_jobs, trigger='cron', hour=0, minute=0)

scheduler.start()
