import os
import uuid

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_pet_photos(files: list[FileStorage]) -> list[str]:
    urls = []
    upload_dir = os.path.join(current_app.root_path, "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    for file in files:
        if not file or not file.filename:
            continue
        if not allowed_file(file.filename):
            continue
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > current_app.config["MAX_PHOTO_SIZE"]:
            continue
        ext = secure_filename(file.filename).rsplit(".", 1)[-1].lower()
        name = f"{uuid.uuid4().hex}.{ext}"
        path = os.path.join(upload_dir, name)
        file.save(path)
        urls.append(f"uploads/{name}")
    return urls
