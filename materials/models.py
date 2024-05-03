from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}



class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='название курса')
    preview = models.ImageField(upload_to='materials/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='название урока')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='materials/', verbose_name='превью', **NULLABLE)
    video = models.URLField(max_length=300, verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
