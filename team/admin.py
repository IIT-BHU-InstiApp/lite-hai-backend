from django.contrib import admin
from .models import Role, TeamMember

admin.site.register(Role)

@admin.register(TeamMember)
class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('github_image_url',)
    list_display = ('__str__', 'role', 'github_username')
    list_filter = ('role',)
