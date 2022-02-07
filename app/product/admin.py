from django.contrib import admin

# Register your models here.

from .models import Category, Product

admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields] #if field.name != "id"]
admin.site.register(Product, ProductAdmin)