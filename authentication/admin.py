from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('photo_url',)
    list_display = ('__str__', 'uid', 'email', 'phone_number',)
    search_fields = ('uid', 'email', 'name',)
    list_filter = ('department', 'year_of_joining',)
    raw_id_fields = ('user',)
