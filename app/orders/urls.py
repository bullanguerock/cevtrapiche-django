from django.urls import path
from orders import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('getstatus/', views.getStatus, name='getStatus'),
    path('orders/', views.OrdersList.as_view(), name='orders')


]