from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
User._meta.get_field('email')._unique = True


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
