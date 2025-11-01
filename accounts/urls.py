from django.urls import path
from . import views

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

    # -------------------
    # Redirection vers le bon dashboard
    # -------------------
    path('dashboard/', views.redirect_dashboard, name='dashboard'),
]
