from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from django.shortcuts import get_object_or_404, redirect
from my_app.models import Product,CartItem
from math import ceil
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings

from django.contrib.auth.decorators import login_required



from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . credentials import MpesaAccessToken, LipanaMpesaPpassword

from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


from django.shortcuts import render
from django.http import JsonResponse
from .utility import lipa_na_mpesa_online
# from .models import Payment
# from my_app import keys
from django.views.decorators.csrf import csrf_exempt

# def index(request):
  
  
  
  
  
#   # current_user=request.user
#   # print(current_user)
#   # allProds=[]
#   # catprods=Product.objects.values('category','id')
#   # cats={item['category'] for item in catprods}
#   # for cat in cats:
#   #   prod=Product.objects.filter(category=cat)
#   #   n=len(prod)
#   #   nSlides=n//4+ ceil((n/4)-(n//4))
#   #   allProds.append([prod,range(1,nSlides),nSlides])
#   # params={'allProds':allProds}
    

#   #   # return HttpResponse ('welcometo my shop')


#     products=Product.objects.all()
#     return render(request,'index.html',{'products':products})






def product_list(request):
    products=Product.objects.all()
    return render(request,'index.html',{'products':products})
















@login_required
def add_to_cart(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    
    cart_item.quantity+=1
    cart_item.save()
    
    
    
    
    return redirect('view_cart')
  
  
  
  
def view_cart(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total_price=sum(item.product.price*item.quantity for item in cart_items)
    return render(request,"cart.html",{'cart_items':cart_items,'total_price':total_price})





def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f'Reduced {cart_item.product.name} quantity in your cart.')
    else:
        cart_item.delete()
        messages.success(request, f'Removed {cart_item.product.name} from your cart.')
    
    return redirect('view_cart')




def purchase(request):
  allprods=[]
  catprods=Product.objects.values('category','id')
  cats={item['category']for item in catprods}
  for cat in cats:
    prod= Product.objects.filter(category=cat)
    n=len(prod)
    nSlides=n//4+ceil((n/4))-(n//4)
    allprods.append([prod,range(1,nSlides),nSlides])


  params={'allprods':allprods}
  return render(request,'purchase.html',params)





def checkout(request):
  if not request.user.is_authenticated:
    messages.warning(request,"login & try again")
    return redirect('/arkauth/login')

  return render(request,"checkout.html")

def initiate_payment(request):
    phone_number = request.POST.get('phone_number')
    amount = request.POST.get('amount')

    if not phone_number or not amount:
        return JsonResponse({'status': 'error', 'message': 'Missing parameters'})

    response = lipa_na_mpesa_online(phone_number, amount)
    return JsonResponse(response)
  
  
  
 
def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token}) 
  
  

def pay(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "samuel chege ",
            "TransactionDesc": "Web Development Charges"
        }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse("success")


def stk(request):
    return render(request, 'pay.html', {'navbar':'stk'})