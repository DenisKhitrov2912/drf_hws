from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    is_active = models.BooleanField(default='True', verbose_name='активность')
    last_login = models.DateTimeField(auto_now=True, verbose_name="Последний вход", **NULLABLE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    pay_date = models.DateTimeField(auto_now=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    pay_sum = models.PositiveIntegerField(verbose_name='сумма оплаты')
    pay_transfer = models.BooleanField(default=True, verbose_name='оплата переводом')
    session_id = models.CharField(max_length=250, **NULLABLE, verbose_name="id сессии")
    payment_link = models.URLField(max_length=500, **NULLABLE, verbose_name="Ссылка на оплату")
    payment_status = models.TextField(**NULLABLE, verbose_name="статус оплаты")

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
