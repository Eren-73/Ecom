from django.contrib import admin
from .models import VendorProfile, CustomerProfile
from django.contrib.auth.models import User

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'phone', 'city', 'is_verified', 'created_at')
    search_fields = ('business_name', 'user__username', 'city')
    list_filter = ('is_verified', 'city')

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'created_at')
    search_fields = ('user__username', 'city')
