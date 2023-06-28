from django.contrib import admin

from accounts.models import User, OtpCode


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(OtpCode)
class OtpAdmin(admin.ModelAdmin):
    pass
