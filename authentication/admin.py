from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(UserProfile)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('__str__', 'uid', 'email',)
    search_fields=('uid',)
    list_filter=('department', 'year_of_joining',)
    raw_id_fields=('user',)
