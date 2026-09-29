from django.contrib import admin

from .models import ActivityLog, Admin as MedFindAdmin


@admin.register(MedFindAdmin)
class MedFindAdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'email', 'first_name', 'last_name', 'role', 'created_at')
    exclude = ('password_hash',)

    def has_add_permission(self, request):
        return False  # create accounts via the app / create_admin so passwords are hashed


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'actor_type', 'actor_id', 'action', 'created_at')
    list_filter = ('actor_type', 'action')
    search_fields = ('description', 'action')
