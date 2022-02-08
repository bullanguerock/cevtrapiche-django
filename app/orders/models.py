from django.contrib.auth.models import User
from django.db import models

from product.models import Product

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('stale', 'Stale'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
    ('pagada', 'Pagada'),
    ('pendiente', 'Pendiente'),
    ('rechazada', 'Rechazada'),
    ('anulada', 'Anulada'),
)

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
    paid_amount = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    flow_token = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.first_name 
    
    def mark_paid(self, custom_amount=None):
        if custom_amount!= None:
            self.paid_amount = custom_amount
        self.status = 'paid'
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id