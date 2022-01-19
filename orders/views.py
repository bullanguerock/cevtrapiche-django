
from urllib import response
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer

from .FlowApi import get_status, flow_payment


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    data = request.data
    serializer = OrderSerializer(data=data)
    

    if serializer.is_valid():
        print('serializer valid')       
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
        
        try:                  
            serializer.save(user=request.user, paid_amount=paid_amount)

            order = serializer.data['id']
            data_dict = flow_payment(paid_amount, order)
            print(data_dict) 
            
            print(data_dict['redirect_url'])

            return Response(data_dict['redirect_url'], status=status.HTTP_201_CREATED)
        except Exception:
            print('exception posiblemente numero de orden repetida')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
    print('serializer invalid')

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def confirmation(request):
    try:
        data = request.data
        #print(data)
        
        token = data['token'] 
        response = get_status(token)
        status_data = response
        print(status_data, token)

        params = {
            'status': status_data,
            'token': token
        }
        
        return redirect('https://cevtrapiche-django.herokuapp.com/cart/confirmation?token='+f'{token}'+'&status='+f'{status_data}')
    except Exception:
        print('exception status post')
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def getStatus(request):    
    result = request.data      
    try:
        status_order = get_status(result['token'])
        print('status order', status_order)
        data = {
            'status_order': status_order
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception:
        print('exception status get')
        return Response(status=status.HTTP_400_BAD_REQUEST)