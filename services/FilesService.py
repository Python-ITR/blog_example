import hashlib
import mimetypes
from os import path
from flask import current_app
from werkzeug import FileStorage


class FilesService:
    @staticmethod
    def save_file(fs: FileStorage):
        """
        Функция сохраняет файл на диск
        Для формирования имени файла используется hash-function md5
        Делается это для избежания дублирования файлов
        Из функции возвращается путь до файла
        """
        hasher = hashlib.new("md5")
        hasher.update(fs.stream.read())
        filename = hasher.hexdigest()
        fs.stream.seek(0)
        extension = mimetypes.guess_extension(fs.mimetype)
        if not extension:
            _, extension = path.splitext(fs.name)
        filename = f"{filename}{extension}"
        fs.save(FilesService.get_path(filename))
        return filename

    @staticmethod
    def get_media_url(filepath: str) -> str:
        """Получить относительный URL до файла"""
        return path.join("/media", filepath)

    @staticmethod
    def get_path(filepath: str) -> str:
        """Получить путь до папки на диске, куда будет сохраняться файл"""
        return path.join(current_app.config.get("MEDIA_DIR"), filepath)

    
