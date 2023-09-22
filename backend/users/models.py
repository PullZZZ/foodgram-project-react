from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    first_name = models.CharField('Имя',
                                  max_length=150,
                                  blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)
    email = models.EmailField('Адрес электронной почты',
                              unique=True,
                              blank=False,)

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


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribeds'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'subscribed'],
                                    name='unique_subscribe'),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('subscribed')),
                name='self_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.subscriber.username}: {self.subscribed.username}'
