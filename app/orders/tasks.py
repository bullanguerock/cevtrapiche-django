from celery import shared_task
import random
from .models import Order, OrderItem
from .FlowApi import get_status

@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y

def liberate_inventory(order):
    try:
        orderitems = OrderItem.objects.filter(order=order)
        for objects in orderitems:
            former_inventory = objects.product.inventory
            quantity = objects.quantity
            new_inventory = former_inventory + quantity

            #save
            objects.product.inventory = new_inventory
            objects.product.save(update_fields=['inventory'])

            return print('iventory liberated succefully')

    except:
        return print('liberate_inventory error')


@shared_task(name="pending_orders")
def pending_orders_handler():
    try:
        pending = Order.objects.filter(status='pendiente')
    except Order.DoesNotExist:
        return None
    
    if pending:
        count = 0
        total = 0
        for item in pending:
            former_status = item.status
            token_check = item.flow_token
            status = get_status(token_check)['status']
            print(status)
            if (status != 1 and former_status!=status):
                #Pagada
                if (status == 2):
                    item.status = 'pagada'
                    item.save(update_fields=['status'])
                #Reachazada
                elif (status == 3):
                    item.status = 'rechazada'
                    item.save(update_fields=['status'])

                    #liberate inventory
                    liberate_inventory(item)              

                elif (status == 4):
                    item.status = 'anulada'
                    item.save(update_fields=['status'])

                    #liberate inventory
                    liberate_inventory(item)                               
                
                count+=1
            total+=1
        return print(str(count)+' ordenes pendientes de ' + str(total) +' han sido actualizadas')

    else:
        return print('No hay ordenes pendientes')   

