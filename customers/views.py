from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Customer

# DRF imports
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import CustomerSerializer

def sign_out(request):
    logout(request)
    return redirect('home')


def show_account(request):
    context={}

    if request.POST and 'register' in request.POST:
        context['register']=True
        try:
            username=request.POST.get('username')
            name=request.POST.get('name')
            password=request.POST.get('password')
            email=request.POST.get('email')
            address=request.POST.get('address')
            phone=request.POST.get('phone')

            if not all([username, name, password, email, address, phone]):
                raise ValueError("Missing required fields.")
                
            #creates user account
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email,
                
            )

            #create customer account
            customer=Customer.objects.create(
                    name=username,
                    user=user,
                    phone=phone,
                    address=address,
                    
            )

            success_message = "User registered successfully!!"
            messages.success(request, success_message)  # ✅ correct

            

        except Exception as e:
            print("Registration Error:", e)  # for console debug
            messages.error(request, "Duplicate username or invalid inputs!")


    if request.POST and 'login' in request.POST:

        context['register']=False
        
        print(request.POST)
        username=request.POST.get('username')

        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'invalid credentials')

        
            
    return render(request, 'account.html', context)


# DRF ViewSet
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
