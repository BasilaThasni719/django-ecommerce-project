from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

# DRF ViewSet
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

# Register API ViewSet
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    # HTML/template-based views
    path('cart/', views.show_cart, name='cart'),
    path('orders', views.show_orders, name='orders'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<pk>', views.remove_item_from_cart, name='remove_item'),
    path('checkout', views.checkout_cart, name='checkout'),

    # DRF API endpoints
    path('api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)