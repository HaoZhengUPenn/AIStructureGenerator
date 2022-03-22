from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import GHRequest

@admin.register(GHRequest)
class GHAdmin(admin.ModelAdmin):
    ordering = ('-updated_at',)
    list_display = ['code','gh_num','succeed','updated_at']
    