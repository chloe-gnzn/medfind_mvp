from django.contrib import admin

from .models import Favorite, Medicine, MedicineCategory, SearchHistory, User

admin.site.register(MedicineCategory)
admin.site.register(SearchHistory)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine_id', 'medicine_name', 'generic_name', 'form', 'strength', 'category')
    list_filter = ('category',)
    search_fields = ('medicine_name', 'generic_name')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('favorite_id', 'user', 'favorite_type', 'medicine', 'pharmacy', 'created_at')
    list_filter = ('favorite_type',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'phone_number', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    exclude = ('password_hash',)

    def has_add_permission(self, request):
        return False  # create accounts via the app / create_admin so passwords are hashed
