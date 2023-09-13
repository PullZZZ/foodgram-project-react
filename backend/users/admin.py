from django.contrib import admin
from .models import Subscribe


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'subscriber',
        'subscribed'
    )
    search_fields = ('subscriber', 'subscribed')


admin.site.register(Subscribe, SubscribeAdmin)
