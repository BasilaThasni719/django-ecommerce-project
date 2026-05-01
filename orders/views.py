from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Order, OrderedItem
from products.models import Product
from customers.models import Customer

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import OrderSerializer


# ---------------------------------
# Helper
# ---------------------------------
def get_customer(user):
    return Customer.objects.filter(user=user).first()


# ---------------------------------
# Web Views
# ---------------------------------
@login_required(login_url='account')
def show_cart(request):
    customer = get_customer(request.user)

    if not customer:
        messages.error(request, "No customer profile found.")
        return redirect('home')

    cart_obj = Order.objects.filter(
        owner=customer,
        order_status=Order.CART_STAGE
    ).first()

    return render(request, 'cart.html', {'cart': cart_obj})


@login_required(login_url='account')
def remove_item_from_cart(request, pk):
    customer = get_customer(request.user)

    if not customer:
        messages.error(request, "No customer profile found.")
        return redirect('home')

    try:
        item = OrderedItem.objects.get(
            pk=pk,
            owner__owner=customer,
            owner__order_status=Order.CART_STAGE
        )
        item.delete()
    except OrderedItem.DoesNotExist:
        messages.error(request, "Item not found.")

    return redirect('cart')


@login_required(login_url='account')
def checkout_cart(request):
    customer = get_customer(request.user)

    if not customer:
        messages.error(request, "No customer profile found.")
        return redirect('home')

    if request.method == "POST":
        try:
            total = float(request.POST.get('total'))

            order_obj = Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )

            if not order_obj.added_items.exists():
                messages.error(request, "Cart is empty.")
                return redirect('cart')

            if total <= 0:
                messages.error(request, "Invalid total.")
                return redirect('cart')

            order_obj.order_status = Order.ORDER_CONFIRMED
            order_obj.total_price = total
            order_obj.save()

            messages.success(
                request,
                "Your order is confirmed. Item will be delivered within 2 days."
            )

        except Order.DoesNotExist:
            messages.error(request, "No items in cart.")

        except Exception:
            messages.error(request, "Unable to process order.")

    return redirect('orders')


@login_required(login_url='account')
def show_orders(request):
    customer = get_customer(request.user)

    if not customer:
        messages.error(request, "No customer profile found.")
        return redirect('home')

    all_orders = Order.objects.filter(
        owner=customer
    ).exclude(order_status=Order.CART_STAGE)

    return render(request, 'orders.html', {'orders': all_orders})


@login_required(login_url='account')
def add_to_cart(request):
    customer = get_customer(request.user)

    if not customer:
        messages.error(request, "No customer profile found.")
        return redirect('home')

    if request.method == "POST":
        try:
            quantity = int(request.POST.get('quantity'))
            product_id = request.POST.get('product_id')

            product = Product.objects.get(pk=product_id)

            cart_obj, created = Order.objects.get_or_create(
                owner=customer,
                order_status=Order.CART_STAGE
            )

            ordered_item, created = OrderedItem.objects.get_or_create(
                Product=product,
                owner=cart_obj
            )

            if created:
                ordered_item.quantity = quantity
            else:
                ordered_item.quantity += quantity

            ordered_item.save()

        except Product.DoesNotExist:
            messages.error(request, "Product not found.")

    return redirect('cart')


# ---------------------------------
# API ViewSet
# ---------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = get_customer(self.request.user)

        if not customer:
            return Order.objects.none()

        return Order.objects.filter(
            owner=customer
        ).exclude(order_status=Order.CART_STAGE)

    @action(detail=False, methods=['get'])
    def cart(self, request):
        customer = get_customer(request.user)

        if not customer:
            return Response(
                {'error': 'No customer profile found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        serializer = self.get_serializer(cart_obj)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add_to_cart')
    def add_to_cart_api(self, request):
        customer = get_customer(request.user)

        if not customer:
            return Response(
                {'error': 'No customer profile found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity'))

            product = Product.objects.get(pk=product_id)

            cart_obj, created = Order.objects.get_or_create(
                owner=customer,
                order_status=Order.CART_STAGE
            )

            ordered_item, created = OrderedItem.objects.get_or_create(
                Product=product,
                owner=cart_obj
            )

            if created:
                ordered_item.quantity = quantity
            else:
                ordered_item.quantity += quantity

            ordered_item.save()

            return Response({'message': 'Item added successfully'})

        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request):
        print("checkout called")
        customer = get_customer(request.user)

        if not customer:
            return Response(
                {'error': 'No customer profile found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            total = float(request.data.get('total'))

            order = Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )

            order.total_price = total
            order.order_status = Order.ORDER_CONFIRMED
            order.save()

            return Response({'message': 'Order confirmed successfully.'})

        except Order.DoesNotExist:
            return Response(
                {'error': 'No cart found.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['delete'], url_path='remove')
    def remove_item(self, request, pk=None):
        customer = get_customer(request.user)

        if not customer:
            return Response(
                {'error': 'No customer profile found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = OrderedItem.objects.get(
                id=pk,
                owner__owner=customer,
                owner__order_status=Order.CART_STAGE
            )

            item.delete()

            return Response(
                {'message': 'Item removed successfully.'},
                status=status.HTTP_204_NO_CONTENT
            )

        except OrderedItem.DoesNotExist:
            return Response(
                {'error': 'Item not found.'},
                status=status.HTTP_404_NOT_FOUND
            )