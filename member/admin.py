from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Member


# Register Member model
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "contact", "role", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("user__username", "user__email", "contact")
    ordering = ("-created_at",)


# Custom User Admin for Jazzmin tabs/carousel/horizontal_tabs
class CustomUserAdmin(BaseUserAdmin):
    
    fieldsets = (
        ("Authentication", {"fields": ("username", "password")}),  # legend string required
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("date_joined",)}),
    )


# Unregister the default User admin
admin.site.unregister(User)

# Register customized UserAdmin
admin.site.register(User, CustomUserAdmin)