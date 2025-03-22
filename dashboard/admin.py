from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserData


class UserDataInline(admin.StackedInline):
    model = UserData
    can_delete = False
    verbose_name_plural = 'Profil użytkownika'
    fk_name = 'user'


class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserDataInline,)

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_trainer', 'is_active', 'active_until', 'trainer')
    search_fields = ('user__username', 'user__email', 'trainer__username')
    list_filter = ('is_trainer', 'is_active')
