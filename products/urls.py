"""
URL configuration for myproject project.

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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views
from .views import ProductViewSet

# Router for DRF ViewSet
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

# URL patterns for both HTML views and API
urlpatterns = [
    # Website UI routes (HTML pages)
    path('', views.index, name='home'),
    path('product_list', views.list_products, name='list_product'),
    path('product_details/<pk>', views.detail_products, name='detail_product'),

    # API routes (automatically handled by router)
    path('api/', include(router.urls)),
]

