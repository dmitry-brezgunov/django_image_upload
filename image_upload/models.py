import os
from urllib.request import urlretrieve

from django.core.files import File
from django.db import models


class Image(models.Model):
    '''Модель изображения, хранящегося в базе.
    original_image - поле с изображением оригинального размера
    url - ссылка на изображение, если оно загруженно со стороннего ресурса
    resized_image - поле с измененным изображением'''
    original_image = models.ImageField(
        upload_to="images/", verbose_name='Файл', blank=True)
    url = models.URLField(verbose_name='Ссылка', blank=True)
    resized_image = models.ImageField(upload_to="images/resized")

    @property
    def filename(self):
        '''Метод для вывода имени файла. Используется в шаблонах'''
        return os.path.basename(self.original_image.url)

    def get_remote_image(self):
        '''Метод для загрузки изображения с url
        Срабатывает только если поле url заполнено
        и изображение отсутствует локально'''
        if self.url and not self.original_image:
            result = urlretrieve(self.url)
            self.original_image.save(os.path.basename(self.url),
                                     File(open(result[0], 'rb')))
            self.save()

    def save(self, *args, **kwargs):
        '''Переопределение стандартного сохранения
        для скачивания файла с url'''
        self.get_remote_image()
        super().save(*args, **kwargs)
