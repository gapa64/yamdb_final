from django.contrib.auth import get_user_model
from django.db import models

from .validators import score_validator, year_validator

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(db_index=True,
                            max_length=256,
                            verbose_name='Название')
    year = models.IntegerField(
        validators=[year_validator],
        verbose_name='Год',
    )
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   verbose_name='Жанр')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Критик')
    pub_date = models.DateTimeField(verbose_name='Дата создания',
                                    auto_now_add=True)
    score = models.IntegerField(validators=[score_validator],
                                verbose_name='Оценка публикации')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              help_text='Введите название произведения',
                              verbose_name='Произведение')
    text = models.TextField(verbose_name='Текст отзыва',
                            help_text='Введите текст отзыва')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_reviewer')
        ]
        ordering = ('-id',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.title}_{self.author}'


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Коментатор')
    pub_date = models.DateTimeField(verbose_name='Дата создания',
                                    auto_now_add=True)
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Отзыв')

    text = models.TextField(verbose_name='Текст коментария',
                            help_text='Введите текст коментария')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
