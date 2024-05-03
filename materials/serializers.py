from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set", many=True, read_only=True)

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'owner', 'preview', 'description', 'lesson_count', 'lesson']
