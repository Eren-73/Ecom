from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # -------------------
    # Signup
    # -------------------
    path('signup/vendor/', views.vendor_signup, name='vendor_signup'),
    path('signup/customer/', views.customer_signup, name='customer_signup'),

    # -------------------
    # Login / Logout
    # -------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # -------------------
    # Dashboards
    # -------------------
    path('vendor/dashboard/', views.dashboard_vendor, name='dashboard_vendor'),
    path('customer/dashboard/', views.dashboard_customer, name='dashboard_customer'),

    path('vendor/order/<int:order_item_id>/status/', views.change_order_status, name='change_order_status'),
    path('order/<int:order_id>/update/', views.update_order_status, name='update_order_status'),

    path('customer/order/<int:order_id>/', views.order_detail_customer, name='order_detail_customer'),

    # urls.py (accounts)
    path('vendor/sales_by_product/<str:product_id>/', views.sales_by_product, name='sales_by_product'),

    path('vendor/sales/csv/', views.vendor_sales_csv, name='vendor_sales_csv'),
    
    path('vendor/<int:vendor_id>/boutique/', views.boutique_vendeur, name='boutique_vendeur'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
