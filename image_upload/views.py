import os

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache

from .forms import ChangeSizeForm, UploadImageForm
from .models import Image
from .utils import image_resize


def index(request):
    '''Главная страница со списком изображений'''
    image_list = Image.objects.all()
    return render(request, "index.html", {"images": image_list})


def upload_image(request):
    '''Страница добавления изображения'''
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            name = os.path.basename(image.original_image.name)
            # При первой загрузке изображения дублируем в поле resized_image
            # оригинальное изображение
            image.resized_image.save(name, image.original_image)
            return redirect("detail", image_id=image.id)
    else:
        form = UploadImageForm()
    return render(request, "upload.html", {"form": form})


@never_cache
def image_detail(request, image_id):
    '''Страница просмотра изображения и изменения его размера'''
    image = get_object_or_404(Image, id=image_id)
    if request.method == "POST":
        form = ChangeSizeForm(request.POST)
        if form.is_valid():
            width = form.cleaned_data["width"]
            height = form.cleaned_data["height"]
            image_resize(image, width, height)
            return redirect("detail", image_id=image.id)
    else:
        form = ChangeSizeForm()
    return render(request, "image.html", {"image": image, "form": form})
