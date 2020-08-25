from django.urls import path

from .views import image_detail, index, upload_image

urlpatterns = [
    path('', index, name='index'),
    path('upload-image/', upload_image, name='upload'),
    path('image/<int:image_id>/', image_detail, name='detail'),
]
