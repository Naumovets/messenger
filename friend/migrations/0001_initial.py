# Generated by Django 4.2.1 on 2023-05-05 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user1_friend', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь 1')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user2_friend', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь 2')),
            ],
        ),
    ]