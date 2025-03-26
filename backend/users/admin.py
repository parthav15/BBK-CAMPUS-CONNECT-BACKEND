from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from users.models import CustomUser

class UserAdmin(BaseUserAdmin):
    list_display = ("first_name", "last_name", "phone_number", "email", "campus", "is_active", "is_staff", "is_deleted", "profile_picture_preview")
    list_editable = ("phone_number", "is_active", "is_deleted")
    list_filter = ("is_active", "is_staff", "is_deleted", "date_joined", "campus")
    search_fields = ("first_name", "last_name", "phone_number", "email")
    readonly_fields = ("date_joined", "last_login", "profile_picture_preview")
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_deleted', 'is_superuser', 'campus', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login')
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')

    actions = ["make_inactive", "make_staff", "delete_users"]
    ordering = ("first_name", "last_name")
    list_per_page = 50

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);" />',
                obj.profile_picture.url
            )
        return format_html('<span style="color: #777;">No Image</span>')
    profile_picture_preview.short_description = "Profile Picture"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) marked as inactive.")
    make_inactive.short_description = "Mark selected users as inactive"

    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f"{updated} user(s) marked as staff.")
    make_staff.short_description = "Mark selected users as staff"

    def delete_users(self, request, queryset):
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f"{updated} user(s) soft deleted.")
    delete_users.short_description = "Soft delete selected users"

admin.site.register(CustomUser, UserAdmin)