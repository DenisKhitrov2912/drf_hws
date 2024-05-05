from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set", many=True, read_only=True)

    def get_subscription(self, course):
        owner = self.context['request'].user
        subscription = Subscription.objects.filter(course=course.id, user=owner.id)
        if subscription:
            return True
        return False

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'owner', 'preview', 'description', 'lesson_count', 'lesson', 'subscription']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
