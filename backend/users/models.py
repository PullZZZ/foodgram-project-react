from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
User._meta.get_field('email')._unique = True


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'subscribed'],
                                    name='unique_subscribe'),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('subscribed')),
                name='self_subscribe'
            )
        ]
