from django.test import Client, TestCase

from .models import Image


class UploadImageTest(TestCase):
    '''Тестирование загрузки изображения'''
    def setUp(self):
        self.client = Client()

    def test_img_upload_local(self):
        '''Тестирования загрузки локального файла'''
        with open("test-img.jpg", "rb") as fp:
            self.client.post("/upload-image/", {"original_image": fp})

        obj = Image.objects.all()[0]

        response = self.client.get(f'/image/{obj.id}/')
        self.assertContains(
            response, f'<img src="{obj.resized_image.url}"',
            status_code=200)

        response = self.client.get('/')
        self.assertContains(
            response, f'<a href="/image/{obj.id}/"', status_code=200)

    def test_img_upload_url(self):
        '''Тестирование загрузки с url'''
        url = "https://upload.wikimedia.org/wikipedia/ru/9/90/Gris_game.jpg"
        self.client.post("/upload-image/", {"url": url})

        obj = Image.objects.all()[0]

        response = self.client.get(f'/image/{obj.id}/')
        self.assertContains(
            response, f'<img src="{obj.resized_image.url}"',
            status_code=200)

        response = self.client.get('/')
        self.assertContains(
            response, f'<a href="/image/{obj.id}/"', status_code=200)

    def test_form_validation(self):
        '''Тестирование валидации формы загрузки'''
        url = "https://upload.wikimedia.org/wikipedia/ru/9/90/Gris_game.jpg"
        with open("test-img.jpg", "rb") as fp:
            response = self.client.post(
                "/upload-image/", {"original_image": fp, "url": url})

        self.assertFormError(
            response, "form", None, "Заполните корректно одно из полей")

        url = "https://upload.wikimedia.org/wikipedia/ru/9/90/Gris_game"
        response = self.client.post("/upload-image/", {"url": url})
        self.assertFormError(
            response, "form", "url", "Проверьте работоспособность ссылки")

        url = "https://github.com/dmitry-brezgunov/"
        response = self.client.post("/upload-image/", {"url": url})
        self.assertFormError(
            response, "form", "url", "Неверное расширение файла. Ссылка должна"
            " оканчиваться расширением изображения (например .jpg).")


class ResizeImageTest(TestCase):
    '''Тестирование изменения размера изображения'''
    def setUp(self):
        self.client = Client()
        with open("test-img.jpg", "rb") as fp:
            self.client.post("/upload-image/", {"original_image": fp})

        self.img = Image.objects.all()[0]

    def test_image_resize_width(self):
        self.client.post(f"/image/{self.img.id}/", {"width": 500})
        response = self.client.get(f"/image/{self.img.id}/")
        new_img = Image.objects.get(id=self.img.id)

        self.assertContains(
            response, f'<img src="{new_img.resized_image.url}"',
            status_code=200)
        self.assertEqual(new_img.resized_image.width, 500)

    def test_image_resize_height(self):
        self.client.post(f"/image/{self.img.id}/", {"height": 500})
        response = self.client.get(f"/image/{self.img.id}/")
        new_img = Image.objects.get(id=self.img.id)

        self.assertContains(
            response, f'<img src="{new_img.resized_image.url}"',
            status_code=200)

        self.assertEqual(new_img.resized_image.height, 500)

    def test_resize_form(self):
        response = self.client.post(f"/image/{self.img.id}/", {})
        self.assertFormError(
            response, "form", None, "Заполните хотя бы одно поле")
