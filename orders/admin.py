from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'total_amount', 'created_at')
    search_fields = ('order_number', 'customer__username')
    list_filter = ('status',)
    inlines = [OrderItemInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'total_items', 'created_at')
    search_fields = ('user__username',)
