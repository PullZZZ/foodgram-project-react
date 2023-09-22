# Generated by Django 4.2.4 on 2023-09-22 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_options'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscribe',
            name='unique_subscribe',
        ),
        migrations.RemoveConstraint(
            model_name='subscribe',
            name='self_subscribe',
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='subscribed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribeds', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('subscriber', 'subscribed'), name='unique_subscribe', violation_error_message='Подписка уже оформлена'),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.CheckConstraint(check=models.Q(('subscriber', models.F('subscribed')), _negated=True), name='self_subscribe', violation_error_message='Нельзя подписаться на самого себя'),
        ),
    ]