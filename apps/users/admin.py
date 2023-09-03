from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'date_joined')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)