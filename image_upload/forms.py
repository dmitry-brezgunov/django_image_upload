from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import Image
from .utils import valid_url_mimetype


class UploadImageForm(forms.ModelForm):
    '''Форма добавления изображения на основе модели Image'''
    class Meta:
        model = Image
        fields = ('url', 'original_image', )

    def clean_url(self):
        '''Валидация поля url для проверки корректности ссылки'''
        url = self.cleaned_data.get("url")
        if url and not valid_url_mimetype(url):
            raise ValidationError(
             "Неверное расширение файла. "
             "Ссылка должна оканчиваться расширением изображения "
             "(например .jpg).")
        return url

    def clean(self):
        '''Валидация формы для проверки что только одно из полей заполнено'''
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")
        local = cleaned_data.get("original_image")

        if (url and local) or (not url and not local):
            raise ValidationError("Заполните корректно одно из полей")

        return cleaned_data


class ChangeSizeForm(forms.Form):
    '''Форма для изменения размера изображения'''
    width = forms.IntegerField(
        required=False, label="Ширина", validators=[MinValueValidator(1)])
    height = forms.IntegerField(
        required=False, label="Высота", validators=[MinValueValidator(1)])

    def clean(self):
        '''Валидация формы для проверки, что хотя бы одно поле заполнено'''
        cleaned_data = self.cleaned_data
        width = cleaned_data.get("width")
        height = cleaned_data.get("height")

        if not width and not height:
            raise ValidationError("Заполните хотя бы одно поле")

        return cleaned_data
