from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'name', 'address', 'phone']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')

        # Create the User 
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create the Customer profile and link it to the User
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
