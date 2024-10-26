

from django.urls import path
from my_app import views
urlpatterns = [
  
   path('', views.product_list, name='product_list'),

path('purchase',views.purchase,name="purchase"),
path('checkout/',views.checkout,name='checkout'),

 
  

path('cart/', views.view_cart, name='view_cart'),
path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
 path('pay', views.pay, name='pay'),
    path('stk', views.stk, name="stk")
]


# path('',views.index,name="index"),