from rest_framework import serializers
from .models import Order, OrderedItem

class OrderedItemSerializer(serializers.ModelSerializer):
     class Meta:
        model = OrderedItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    added_items = OrderedItemSerializer(many=True, read_only=True) # to automatically serialize all related OrderedItem s linked to the Order.

    class Meta:
        model = Order
        fields = '__all__'

