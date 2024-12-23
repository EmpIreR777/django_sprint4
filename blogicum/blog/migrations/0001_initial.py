# Generated by Django 3.2.16 on 2024-04-10 12:44

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Обязательное поле', max_length=256, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Слаг')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и Время:')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Обязательное поле', max_length=256, verbose_name='Название')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и Время:')),
            ],
            options={
                'verbose_name': 'Местоположение',
                'verbose_name_plural': 'Местоположения',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Обязательное поле', max_length=256, verbose_name='Название')),
                ('text', models.TextField(verbose_name='Описание')),
                ('pub_date', models.DateTimeField(verbose_name='Дата и Время:')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и Время:')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='blog.category', verbose_name='Категории')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location', to='blog.location', verbose_name='Локация')),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Публикации',
            },
        ),
    ]
