from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Subscribe, User


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'subscriber',
        'subscribed'
    )
    search_fields = ('subscriber', 'subscribed')


class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('subscribers_count',
                                                 'recipes_count')
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2'
                ),
            },
        ),
    )

    def subscribers_count(self, user):
        return user.subscribeds.count()

    def recipes_count(self, user):
        return user.recipes.count()


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
