from django.shortcuts import render
from . models import Product
from django.core.paginator import Paginator

#for creating apis for product page
from rest_framework import viewsets
from .serializers import ProductSerializer

# Create your views here.
def index(request):
    featured_products=Product.objects.order_by('priority')[:4]
    latest_products=Product.objects.order_by('id')[:4]
    context={
        'featured_products':featured_products,
        'latest_products':latest_products
    }
    return render(request,'index.html', context)

def list_products(request):
    """_summary_
    returns product list page
    Args:
        request (_type_): _description_
    Returns:
        _type_: _description_
    """
    page=1
    if request.GET:
        page=request.GET.get('page',1)

    product_list=Product.objects.order_by('priority')
    product_paginator=Paginator(product_list, 6)
    product_list=product_paginator.get_page(page)
    context={'products':product_list}
    return render(request,'products.html',context)

def detail_products(request,pk):
    product=Product.objects.get(pk=pk)
    context={'product':product}
    return render(request,'product_detail.html', context)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(delete_status=Product.LIVE).order_by('priority')
    serializer_class = ProductSerializer