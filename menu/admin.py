from django.contrib import admin
from .models import Category, MenuItem
from restaurant_project.admin_site import admin_site

@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_per_page = 20
    actions = ['delete_selected']

@admin.register(MenuItem, site=admin_site)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_vegetarian', 'is_spicy', 'is_available', 'is_featured')
    list_filter = ('category', 'is_vegetarian', 'is_spicy', 'is_available', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('is_available', 'is_featured')
    ordering = ('category', 'name')
    list_per_page = 20
    actions = ['delete_selected']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'category', 'image')
        }),
        ('Item Properties', {
            'fields': ('is_vegetarian', 'is_spicy', 'is_available', 'is_featured')
        }),
    )
