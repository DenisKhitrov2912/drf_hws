# Generated by Django 5.0.4 on 2024-05-03 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_payments_options_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default='True', verbose_name='активность'),
        ),
    ]