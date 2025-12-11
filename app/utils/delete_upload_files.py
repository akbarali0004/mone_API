import os
import shutil
from datetime import date, timedelta
from settings import settings

UPLOAD_DIR = settings.UPLOAD_DIR

def delete_upload_files():
    folder = os.path.join(settings.UPLOAD_DIR, str(date.today()-timedelta(days=7)))

    # Xavfsizlik tekshiruvi
    if not folder or folder.strip() == "" or folder in ["/", "\\"]:
        print("Xato: xavfli UPLOAD_DIR yo'li!")
        return

    if not os.path.exists(folder):
        print(f"{folder} mavjud emas")
        return

    try:
        shutil.rmtree(folder)
        print(f"{folder} papkasi muvaffaqiyatli o'chirildi")
    except Exception as e:
        print(f"Papka o'chirilmadi: {folder}, xato -> {e}")
