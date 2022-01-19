from urllib import request
from rest_framework import serializers

from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):

    get_image = serializers.SerializerMethodField('image_url')

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail"
        )
        def image_url(self, obj):
            request = self.context.get("request")
            return request.build_absolute_uri(obj.image.url)

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )