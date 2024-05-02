from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import PublishedModel
from core.constants import MAX_LENGTH


User = get_user_model()


class Post(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок',
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория',
    )
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:profile', kwargs={'username': self.author})


class Category(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        help_text='Обязательное поле',
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        help_text='Обязательное поле',
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField('Текст')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор публикации',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )

    class Meta:
        verbose_name = 'коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.author}'
