from django.contrib import admin
from .models import Order, OrderItem, OrderItemTopping
from restaurant_project.admin_site import admin_site

@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'is_paid')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__username', 'user__email', 'id')
    ordering = ('-created_at',)
    list_editable = ('status', 'is_paid')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['delete_selected']
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'quantity', 'get_total_price')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'menu_item__name')
    ordering = ('-order__created_at',)
    actions = ['delete_selected']
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

@admin.register(OrderItemTopping)
class OrderItemToppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_item', 'topping')
    list_filter = ('topping',)
    search_fields = ('order_item__menu_item__name', 'topping__name')
    ordering = ('order_item__order__created_at',)
    actions = ['delete_selected']
