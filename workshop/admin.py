from django.contrib import admin
from .models import Council, Club, Tag, WorkshopResource, Workshop

@admin.register(Council)
class CouncilAdmin(admin.ModelAdmin):
    def get_gensec(self, obj):
        """
        Get the General Secretary of a Council
        """
        if obj.gensec is None:
            return None
        return obj.gensec.name

    def get_joint_gensec(self, obj):
        """
        Get the Joint General Secretary of a Council
        """
        return ',\n'.join([o.name for o in obj.joint_gensec.all()])

    list_display = ('__str__', 'name', 'get_gensec', 'get_joint_gensec',)
    search_fields = ('name', 'gensec__name', 'joint_gensec__name',)

    get_gensec.short_description = 'General Secretary'
    get_joint_gensec.short_description = 'Joint General Secretary'


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    def get_secy(self, obj):
        """
        Get the Secretary of a Club
        """
        if obj.secy is None:
            return None
        return obj.secy.name

    def get_joint_secy(self, obj):
        """
        Get the Joint Secretary of a Club
        """
        return ',\n'.join([o.name for o in obj.joint_secy.all()])

    def get_subscribed_users(self, obj):
        """
        Get the count of subscribed users for a Club
        """
        return obj.subscribed_users.count()

    list_display = (
        '__str__', 'name', 'council', 'get_secy', 'get_joint_secy', 'get_subscribed_users')
    search_fields = ('name', 'secy__name', 'joint_secy__name',)
    list_filter = ('council',)

    get_secy.short_description = 'Secretary'
    get_joint_secy.short_description = 'Joint Secretary'
    get_subscribed_users.short_description = 'Subscribed Users'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'club')
    search_fields = ('tag_name',)
    list_filter = ('club',)


@admin.register(WorkshopResource)
class WorkshopResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    search_fields = ('name',)


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    def get_contacts(self, obj):
        """
        Get the contacts for a workshop
        """
        return ',\n'.join([o.name for o in obj.contacts.all()])

    def get_tags(self, obj):
        """
        Get the tags for a workshop
        """
        return ',\n'.join([o.tag_name for o in obj.tags.all()])

    def get_interested_users(self, obj):
        """
        Get the count of interested users for a workshop
        """
        return obj.interested_users.count()

    list_display = (
        '__str__', 'title', 'club', 'date', 'time',
        'get_interested_users', 'get_contacts', 'get_tags')
    search_fields = ('title', 'contacts__name', 'tags__tag_name')
    list_filter = ('club',)

    get_interested_users.short_description = 'Interested Users'
    get_contacts.short_description = 'Contacts'
    get_tags.short_description = 'Tags'
