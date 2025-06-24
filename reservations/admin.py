from django.contrib import admin
from .models import Reservation, Table
from restaurant_project.admin_site import admin_site

@admin.register(Reservation, site=admin_site)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reservation_date', 'reservation_time', 'number_of_guests', 'status', 'table')
    list_filter = ('status', 'reservation_date', 'table')
    search_fields = ('user__username', 'user__email', 'special_request')
    ordering = ('-reservation_date', '-reservation_time')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['delete_selected']
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Table, site=admin_site)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'is_available')
    list_filter = ('is_available', 'capacity')
    search_fields = ('table_number',)
    ordering = ('table_number',)
    list_editable = ('is_available',)
    actions = ['delete_selected']
