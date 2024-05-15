import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from materials.tasks import sending_mail
from users.permissions import IsUserAdmDRF, IsUserOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Администраторы DRF').exists():
            return Course.objects.all()
        elif self.request.user.is_anonymous:
            return None
        else:
            return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsUserAdmDRF | IsUserOwner]
        else:
            permission_classes = [IsAuthenticated, IsUserOwner | IsAdminUser]
        return [permission() for permission in permission_classes]

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    # def partial_update(self, request, *args, **kwargs):
    #     user = self.request.user
    #     course_id = self.get_object().id
    #     course_item = get_object_or_404(Course, pk=course_id)
    #     subs_item = Subscription.objects.filter(
    #         user=user, course=course_item
    #     )
    #
    #     if subs_item.exists():
    #         sending_mail.delay()
    #     return super().partial_update(request, *args, **kwargs)
    #
    # def update(self, request, *args, **kwargs):
    #     user = self.request.user
    #     course_id = self.get_object().id
    #     course_item = get_object_or_404(Course, pk=course_id)
    #     subs_item = Subscription.objects.filter(
    #         user=user, course=course_item
    #     )
    #
    #     if subs_item.exists():
    #         sending_mail.delay()
    #     return super().update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        date = instance.last_update
        instance.last_update = datetime.datetime.now()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        sending_mail.delay(instance.id, date)
        return Response(serializer.data)

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsUserOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Администраторы DRF').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    def get(self, request):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonDetailAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsUserAdmDRF | IsUserOwner]
    pagination_class = MaterialsPagination


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsUserAdmDRF | IsUserOwner]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        date = instance.last_update
        instance.last_update = datetime.datetime.now()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        sending_mail.delay(instance.id, date)
        return Response(serializer.data)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | IsUserOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsUserOwner]
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(operation_description="Add or remove the subscription on a course")
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(
            user=user, course=course_item
        )

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'

        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})
