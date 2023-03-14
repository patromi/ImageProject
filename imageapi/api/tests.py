import io
from datetime import datetime, timedelta

import pytz
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import ImageUser as User
from core.models import Images
from PIL import Image as img


def create_test_img():
    image = img.new('RGB', (1000, 1000), color='red')
    image_file = io.BytesIO()
    image.save(image_file, 'png')
    return image_file.getvalue()


UPLOAD_URL_NAMES = (
    'small_upload',
    'medium_upload',
    'original_upload',
    'custom_upload',

)

BASIC_USER_URlS = (
    'small_upload',

)

PREMIUM_AND_ENTERPRISE_USER_URlS = (
    'small_upload',
    'medium_upload',
    'original_upload',

)


class APITest(APITestCase):
    def setUp(self) -> None:
        url = reverse('token_obtain_pair')
        u = User.objects.create_user(email='root@gmail.com', password='pass', plan='ROOT')
        u.is_active = True
        u.save()
        token = self.client.post(url, {'email': 'root@gmail.com', 'password': 'pass'}, format='json')
        self.assertEqual(token.status_code, status.HTTP_200_OK)
        self.root_token = token.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.root_token}')

        self.basic_user = User.objects.create_user(email='basic@gmail.com', password='pass', plan='BASIC')
        self.basic_user.is_active = True
        self.basic_user.save()
        self.basic_user_token = self.client.post(url, {'email': 'basic@gmail.com', 'password': 'pass'}, format='json')
        self.assertEqual(self.basic_user_token.status_code, status.HTTP_200_OK)

        self.premium_user = User.objects.create_user(email='premium@gmail.com', password='pass', plan='PREMIUM')
        self.premium_user.is_active = True
        self.premium_user.save()
        self.premium_user_token = self.client.post(url, {'email': 'premium@gmail.com', 'password': 'pass'},
                                                   format='json')
        self.assertEqual(self.premium_user_token.status_code, status.HTTP_200_OK)

        self.enterprise_user = User.objects.create_user(email='enter@gmail.com', password='pass', plan='ENTERPRISE')
        self.enterprise_user.is_active = True
        self.enterprise_user.save()
        self.enterprise_user_token = self.client.post(url, {'email': 'enter@gmail.com', 'password': 'pass'},
                                                      format='json')
        self.assertEqual(self.premium_user_token.status_code, status.HTTP_200_OK)
        self.token_list = [token.data["access"], self.basic_user_token.data["access"],
                           self.premium_user_token.data["access"], self.enterprise_user_token.data["access"]]

    def test_upload_small_image_with_valid_data(self):
        for token in self.token_list:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
            img = SimpleUploadedFile('image.png', create_test_img())
            data = {'title': 'Test Image', 'image': img}
            response = self.client.post(reverse('small_upload'), data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {'status': 'Uploaded'})

    def test_upload_normal_image_with_valid_data(self):
        img = SimpleUploadedFile('image.png', create_test_img())
        data = {'title': 'Test Image', 'image': img}
        response = self.client.post(reverse('medium_upload'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'status': 'Uploaded'})

    def test_upload_original_image_with_valid_data(self):
        img = SimpleUploadedFile('image.png', create_test_img())
        data = {'title': 'Test Image', 'image': img}
        response = self.client.post(reverse('original_upload'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'status': 'Uploaded'})

    def test_upload_custom_image_with_valid_data_and_different_resolution(self):
        img = SimpleUploadedFile('image.png', create_test_img())
        data = {'title': 'Test Image', 'image': img, 'height': '535', 'width': '332'}
        response = self.client.post(reverse('custom_upload'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'status': 'Uploaded'})

    def test_basic_user_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.basic_user_token.data["access"]}')
        for url in UPLOAD_URL_NAMES:
            img = SimpleUploadedFile('image.png', create_test_img())
            data = {'title': 'Test Image', 'image': img}
            response = self.client.post(reverse(url), data)
            if url in BASIC_USER_URlS:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data, {'status': 'Uploaded'})
            else:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_premium_user_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.premium_user_token.data["access"]}')
        for url in UPLOAD_URL_NAMES:
            img = SimpleUploadedFile('image.png', create_test_img())
            data = {'title': 'Test Image', 'image': img}
            response = self.client.post(reverse(url), data)
            if url in PREMIUM_AND_ENTERPRISE_USER_URlS:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data, {'status': 'Uploaded'})
            else:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_enterprise_user_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.enterprise_user_token.data["access"]}')
        for url in UPLOAD_URL_NAMES:
            img = SimpleUploadedFile('image.png', create_test_img())
            data = {'title': 'Test Image', 'image': img, 'expired_time': 400}
            response = self.client.post(reverse(url), data)
            if url in PREMIUM_AND_ENTERPRISE_USER_URlS:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data, {'status': 'Uploaded'})
            else:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_root_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.root_token}')
        for url in UPLOAD_URL_NAMES:
            img = SimpleUploadedFile('image.png', create_test_img())
            data = {'title': 'Test Image', 'image': img, 'expired_time': 400, 'height': 340, 'width': 400}
            response = self.client.post(reverse(url), data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {'status': 'Uploaded'})


    def test_upload_image_with_valid_data_and_invalid_expired_time(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.root_token}')
        img = SimpleUploadedFile('image.png', create_test_img())
        data = {'title': 'Test Image', 'image': img, 'expired_time': 'testdata'}
        for url in UPLOAD_URL_NAMES:
            response = self.client.post(reverse(url), data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_image_with_invalid_data_and_expired_time(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.enterprise_user_token.data["access"]}')
        img = SimpleUploadedFile('image.png', create_test_img())
        data = {'title': 'Test Image', 'image': img, 'height': '535w', 'width': '332w', 'expired_time': 300}
        response = self.client.post(reverse('custom_upload'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_image_with_invalid_img_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.root_token}')
        for url in UPLOAD_URL_NAMES:
            data = {'title': 'Test Image', 'image': 'img','expired_time': 300}
            response = self.client.post(reverse(url), data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_view(self):
        for token in self.token_list:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
            response = self.client.get(reverse('img_listview'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expired_link(self):

        img = SimpleUploadedFile('image.png', create_test_img())
        data = {'id':'8aa366d5-5d9f-4c3b-884a-2e6679d88ba8',"title":"TestTitle","image":img,'expired_at': datetime.now(pytz.timezone('UTC')) - timedelta(seconds=10),'uploaded_by':self.enterprise_user,'resolution':'200x200'}
        Images.objects.create(**data)
        response = self.client.get(reverse('img_view',kwargs={'id':"8aa366d5-5d9f-4c3b-884a-2e6679d88ba8"}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_expired_link(self):
        img = SimpleUploadedFile('image.png', create_test_img())
        data = {'id': '8aa366d5-5d9f-4c3b-884a-2e6679d88ba9', "title": "TestTitle", "image": img,
                'expired_at': datetime.now(pytz.timezone('UTC')) + timedelta(seconds=20),
                'uploaded_by': self.enterprise_user, 'resolution': '200x200'}
        Images.objects.create(**data)
        response = self.client.get(reverse('img_view', kwargs={'id': "8aa366d5-5d9f-4c3b-884a-2e6679d88ba9"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

