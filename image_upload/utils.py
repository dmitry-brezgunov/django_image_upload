import mimetypes
import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image

from .models import Image as MyImage

VALID_IMAGE_MIMETYPES = [
    "image"
]


def valid_url_mimetype(
     url: str, mimetype_list: list = VALID_IMAGE_MIMETYPES) -> bool:
    '''Проверка того, что ссылка является изображением'''
    mimetype, _ = mimetypes.guess_type(url)
    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False


def image_resize(image_object: MyImage, width: int, height: int):
    '''Функция для изменения размера изображения
    Все изменения производятся от оригинального изображения,
    чтобы избежать потери качества. Создается новое изображение
    с измененным размером.'''
    img_io = BytesIO()
    image_file = image_object.original_image
    old_image = image_object.resized_image.path
    image = Image.open(image_file)

    # Если один из параметров не был указан
    # берется размер оригинального изображения
    if width is None:
        width = image_object.resized_image.width
    if height is None:
        height = image_object.resized_image.height

    size = (width, height)
    image.thumbnail(size, Image.BILINEAR)
    os.remove(old_image)
    image.save(img_io, format="JPEG", quality=100)
    img_content = ContentFile(img_io.getvalue(), image_object.filename)

    # Изначально сделал так, что старая версия resized_image перезаписывалась,
    # но возникли проблемы с кешем, изображение кешировалась в браузере
    # и не обновлялось.
    image_object.resized_image = img_content
    image_object.save()
    img_io.close()
