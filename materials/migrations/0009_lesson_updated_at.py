# Generated by Django 5.0.4 on 2024-05-15 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0008_alter_subscription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='дата и время обновления'),
        ),
    ]
