from django.urls import path
from .import views

app_name = 'payment'
urlpatterns = [
    path('payment',views.payment,name='payment'),
    path('payment-status', views.payment_status, name='payment-status'),


 
    
]
