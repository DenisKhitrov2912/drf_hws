from rest_framework.test import APITestCase, APIClient
from users.models import User
from materials.models import Lesson, Course, Subscription
from django.urls import reverse
from rest_framework import status


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test', owner=self.user)
        self.lesson = Lesson.objects.create(name='test', course=self.course,
                                            video='https://www.youtube.com/123',
                                            owner=self.user)

    def test_list_lessons(self):
        response = self.client.get(
            reverse('materials:lessons'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None,
             'results': [{'id': self.lesson.id, 'course': self.course.pk, 'name': self.lesson.name,
                          'description': None, 'preview': None, 'video': 'https://www.youtube.com/123',
                          'owner': self.user.pk}]}
        )

    def test_create_lesson(self):
        data = {
            "name": self.lesson.name,
            "course": self.course.id,
            "video": "https://www.youtube.com/123",
        }
        response = self.client.post(reverse('materials:lesson_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {'id': self.lesson.pk + 1, 'course': self.course.pk, 'name': self.lesson.name,
                          'description': None, 'preview': None, 'video': 'https://www.youtube.com/123',
                          'owner': self.user.pk})

    def test_retrieve_lesson(self):
        response = self.client.get(
            reverse('materials:lesson', kwargs={'pk': self.lesson.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(response.json(),
                         {'id': self.lesson.id, 'course': self.course.pk, 'name': self.lesson.name,
                          'description': None, 'preview': None, 'video': 'https://www.youtube.com/123',
                          'owner': self.user.pk})

    def test_update_lesson(self):
        data = {
            "name": "test",
            "course": self.course.pk,
            "video": "https://www.youtube.com/1234",
            "owner": self.user.pk,
        }
        response = self.client.patch(
            reverse('materials:lesson_update', kwargs={'pk': self.lesson.pk}),

            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'course': self.course.pk, 'name': 'test', "video": 'https://www.youtube.com/1234',
             'owner': self.user.pk, 'description': None, 'preview': None}
        )

    def test_delete_lesson(self):
        response = self.client.delete(
            reverse('materials:lesson_delete', kwargs={'pk': self.lesson.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_validator(self):
        data = {
            "name": "test",
            "course": self.course.pk,
            "video": "https://www.test.com/54321"
        }
        response = self.client.post(reverse('materials:lesson_create'), data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'video': ['Incorrect YouTube URL']}
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="test", owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

    def test_create_subscription(self):
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }

        response = self.client.post(reverse('materials:subs_create'), data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        (self.assertEqual(
            response.json(),
            {'message': 'подписка удалена'}
        ))


class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test', owner=self.user)
        self.lesson = Lesson.objects.create(name='test', course=self.course,
                                            video='https://www.youtube.com/123',
                                            owner=self.user)

    def test_list_course(self):
        response = self.client.get(
            '/courses/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None,
             'results': [{'id': self.course.pk,
                          'lesson': [{'course': self.course.id,
                                      'description': None,
                                      'id': self.lesson.id,
                                      'name': 'test',
                                      'owner': self.user.id,
                                      'preview': None,
                                      'video': 'https://www.youtube.com/123'}],
                          'lesson_count': 1,
                          'name': self.course.name,
                          'description': None, 'owner': self.user.pk, 'preview': None, 'subscription': False}]}
        )

    def test_create_course(self):
        data = {
            "name": self.course.name
        }
        response = self.client.post('/courses/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {'id': self.course.pk + 1,
                          'lesson': [],
                          'lesson_count': 0,
                          'name': self.course.name,
                          'description': None, 'owner': self.user.pk, 'preview': None, 'subscription': False})

    def test_retrieve_course(self):
        response = self.client.get(f'/courses/{self.course.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(response.json(),
                         {'id': self.course.pk,
                          'lesson': [{'course': self.course.id,
                                      'description': None,
                                      'id': self.lesson.id,
                                      'name': 'test',
                                      'owner': self.user.id,
                                      'preview': None,
                                      'video': 'https://www.youtube.com/123'}],
                          'lesson_count': 1,
                          'name': self.course.name,
                          'description': None, 'owner': self.user.pk, 'preview': None, 'subscription': False})

    def test_update_course(self):
        data = {
            "name": "test_new",
            "owner": self.user.pk,
        }
        response = self.client.patch(f'/courses/{self.course.id}/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.course.pk,
             'lesson': [{'course': self.course.id,
                         'description': None,
                         'id': self.lesson.id,
                         'name': 'test',
                         'owner': self.user.id,
                         'preview': None,
                         'video': 'https://www.youtube.com/123'}],
             'lesson_count': 1,
             'name': 'test_new',
             'description': None, 'owner': self.user.pk, 'preview': None, 'subscription': False})

    def test_delete_course(self):
        response = self.client.delete(f'/courses/{self.course.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
