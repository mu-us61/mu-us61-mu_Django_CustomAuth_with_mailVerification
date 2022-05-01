from django.contrib import admin
from app_auth import models

# Register your models here.

from django.contrib.auth.admin import UserAdmin


admin.site.register(models.CustomUser, UserAdmin)
