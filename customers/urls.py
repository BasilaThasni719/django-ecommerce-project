from django.urls import path, include
from . import views


# DRF
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')

urlpatterns = [
    # HTML template views
    path('account/', views.show_account, name='account'),
    path('logout', views.sign_out, name='logout'),

    # API routes
    path('api/', include(router.urls))
]

