import mimetypes

from PIL import Image

VALID_IMAGE_MIMETYPES = [
    "image"
]


def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
    '''Проверка того, что ссылка является изображением'''
    mimetype, _ = mimetypes.guess_type(url)
    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False


def image_resize(image_object, width, height):
    '''Функция для изменения размера изображения
    Все изменения производятся от оригинального изображения,
    чтобы избежать потери качества. Изображение с измененным
    размером при этом перезаписывается, чтобы не хранить
    множество копий всех предыдущих размеров'''
    image_file = image_object.original_image
    image = Image.open(image_file)

    # Если один из параметров не был указан
    # берется размер оригинального изображения
    if width is None:
        width = image_object.original_image.width
    if height is None:
        height = image_object.original_image.height

    size = (width, height)
    image.thumbnail(size, Image.BILINEAR)
    image.save(image_object.resized_image.path, quality=75)
