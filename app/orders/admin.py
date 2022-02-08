from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields] #if field.name != "id"]
admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem)