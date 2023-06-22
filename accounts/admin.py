from django.contrib import admin

from accounts.models import User, OtpCode


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(OtpCode)
class OtpAdmin(admin.ModelAdmin):
    pass
