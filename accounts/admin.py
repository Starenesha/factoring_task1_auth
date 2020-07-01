from django.contrib import admin

# Register your models here.
from accounts.models import User, Depart


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Depart)
class DepartAdmin(admin.ModelAdmin):
    pass
