from django.db import models
from django.core.exceptions import ValidationError


def validate_title(value):
    forbidden_chars = '!@#$%^&*_=+'
    for char in value:
        if char in forbidden_chars:
            raise ValidationError(f'Символ "{char}" запрещен. Пишите название словами')

def validate_capital_start(value):
    if value and not value[0].isupper():
        raise ValidationError('Заголовок должен начинаться с большой буквы')

def validate_non_negative(value):
    if value < 0:
        raise ValidationError('Цена должна быть БОЛЬШЕ нуля')


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='Тэг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']


class Bb(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
        validators = [validate_title, validate_capital_start]
    )

    content = models.TextField(verbose_name='Описание')

    price = models.FloatField(
        verbose_name='Цена',
        validators = [validate_non_negative]
    )

    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    image = models.ImageField(upload_to='bbs/', blank=True, null=True, verbose_name='Фото')
    rubric = models.ForeignKey(Rubric, null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Тэги')

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']


class BbExtra(models.Model):
    bb = models.OneToOneField(Bb, on_delete=models.CASCADE, primary_key=True, verbose_name='Объявление')
    is_broken = models.BooleanField(default=False, verbose_name='Требует ремонта?')
    contact_email = models.EmailField(blank=True, verbose_name='Email для связи')

    class Meta:
        verbose_name = 'Дополнительно'
        verbose_name_plural = 'Дополнительные параметры'















