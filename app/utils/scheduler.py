from apscheduler.schedulers.background import BackgroundScheduler
from database import get_db
from crud import activate_tasks
from .delete_upload_files import delete_upload_files

# Scheduler yaratish
scheduler = BackgroundScheduler()

# Har kuni 00:00 da ishga tushirish
scheduler.add_job(func=lambda: activate_tasks(next(get_db())), trigger='cron', hour=0, minute=0)
scheduler.add_job(func=lambda: delete_upload_files(), trigger='cron', hour=0, minute=0)

# Har dushanba 00:00 ishga tushirish
scheduler.add_job(func=lambda: activate_tasks(next(get_db())), trigger='cron', day_of_week='mon', hour=0, minute=0)

# Har oy 1-kuni 00:00 ishga tushirish
scheduler.add_job(func=lambda: activate_tasks(next(get_db())), trigger='cron', day=1, hour=0, minute=0)

scheduler.start()
