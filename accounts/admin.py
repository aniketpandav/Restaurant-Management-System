from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from restaurant_project.admin_site import admin_site

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_role(self, obj):
        if obj.is_superuser:
            return 'Superadmin'
        elif obj.is_staff:
            return 'Staff'
        return 'Customer'
    get_role.short_description = 'Role'

admin_site.register(User, CustomUserAdmin)
