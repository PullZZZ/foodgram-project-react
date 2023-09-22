from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    first_name = models.CharField('Имя',
                                  max_length=settings.USERSFIELD_MAX_LEN,
                                  blank=False)
    last_name = models.CharField('Фамилия',
                                 max_length=settings.USERSFIELD_MAX_LEN,
                                 blank=False)
    email = models.EmailField('Адрес электронной почты',
                              unique=True,
                              blank=False,
                              max_length=settings.EMAIL_MAX_LEN)

    class Meta:
        db_table = 'auth_user'
        constraints = [
            models.UniqueConstraint(
                Lower('username'),
                name='unique_username'
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id', )

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписчик'
    )
    subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribeds',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscribed'],
                name='unique_subscribe'
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('subscribed')),
                name='self_subscribe',
                violation_error_message='Нельзя подписаться на самого себя'
            ),
        ]

    def __str__(self):
        return f'{self.subscriber.username}: {self.subscribed.username}'
