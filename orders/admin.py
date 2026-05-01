from django.contrib import admin
from .models import OrderedItem, Order

class OrderAdmin(admin.ModelAdmin):
    list_filter = [
        "owner",
        "order_status",
    ]

    search_field = (
        "owner",
        "id",
    )

admin.site.register(Order,OrderAdmin)
