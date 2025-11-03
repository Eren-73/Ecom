"""
URL configuration for ecommerce_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views 
<<<<<<< HEAD
=======
from django.conf import settings
from django.conf.urls.static import static
>>>>>>> feature/produits

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('accounts/', include('accounts.urls')),
<<<<<<< HEAD
=======
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
>>>>>>> feature/produits


    # Redirection automatique vers le dashboard
    path('dashboard/', views.redirect_dashboard, name='redirect_dashboard'),


    
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
   


    # Redirections selon rôle
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('vendeur/', views.vendeur_dashboard, name='vendeur_dashboard'),
<<<<<<< HEAD
]
=======

   

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> feature/produits
