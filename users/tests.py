import json
from datetime import datetime

from rest_framework.test import APITestCase, APIClient

from materials.models import Course, Lesson
from users.models import User, Payments
from django.urls import reverse
from rest_framework import status


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        response = self.client.get(
            reverse('users:user_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': self.user.pk, 'email': 'test@test.com', 'avatar': None, 'phone': None, 'city': None}]
        )

    def test_create_users(self):
        data = {
            "email": '1@ya.ru',
            "password": "123456"
        }
        response = self.client.post(reverse('users:user_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {'id': self.user.pk + 1, 'email': '1@ya.ru', 'avatar': None, 'phone': None, 'city': None,
                          'password': '123456', 'payments': []})

    def test_retrieve_users(self):
        response = self.client.get(
            reverse('users:user_detail', kwargs={'pk': self.user.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(response.json(),
                         {'id': self.user.pk, 'email': 'test@test.com', 'avatar': None, 'phone': None, 'city': None,
                          'password': '12345', 'payments': []})

    def test_update_users(self):
        data = {
            "email": '12@ya.ru',
            "password": "1234567"
        }
        response = self.client.patch(
            reverse('users:user_update', kwargs={'pk': self.user.pk}),

            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.user.pk, 'email': '12@ya.ru', 'avatar': None, 'phone': None, 'city': None,
             'password': '1234567', 'payments': []}
        )

    def test_delete_users(self):
        response = self.client.delete(
            reverse('users:user_delete', kwargs={'pk': self.user.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class PaymentsTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test', owner=self.user)
        self.lesson = Lesson.objects.create(name='test', course=self.course,
                                            video='https://www.youtube.com/123',
                                            owner=self.user)
        self.payments = Payments.objects.create(user=self.user, pay_sum=1000)

    def test_list_payments(self):
        response = self.client.get(
            '/payments/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': self.payments.id, 'pay_date': self.payments.pay_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
              'pay_sum': 1000, 'pay_transfer': True, 'user': self.user.id,
              'paid_course': None, 'paid_lesson': None}]
        )

    def test_create_payments(self):
        data = {
            "user": self.user.pk,
            "paid_course": self.course.pk,
            'pay_date': datetime.now,
            'pay_sum': 2000,
            'pay_transfer': False
        }
        response = self.client.post('/payments/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {'id': self.payments.id + 1,
                          'pay_date': response.json()['pay_date'],
                          'pay_sum': 2000, 'pay_transfer': False, 'user': self.user.pk,
                          'paid_course': self.course.pk, 'paid_lesson': None})

    def test_retrieve_payments(self):
        response = self.client.get(f'/payments/{self.payments.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(response.json(),
                         {'id': self.payments.id,
                          'pay_date': self.payments.pay_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                          'pay_sum': 1000, 'pay_transfer': True, 'user': self.user.id,
                          'paid_course': None, 'paid_lesson': None})

    def test_update_payments(self):
        data = {
            "paid_lesson": self.lesson.pk,
            'pay_sum': 2500
        }
        response = self.client.patch(f'/payments/{self.payments.id}/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.payments.id,
             'pay_date': response.json()['pay_date'],
             'pay_sum': 2500, 'pay_transfer': True, 'user': self.user.id,
             'paid_course': None, 'paid_lesson': self.lesson.pk}
        )

    def test_delete_payments(self):
        response = self.client.delete(f'/payments/{self.payments.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
