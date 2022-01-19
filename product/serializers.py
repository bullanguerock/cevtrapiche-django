from urllib import request
from rest_framework import serializers

from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):

    get_image = serializers.SerializerMethodField()

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
    def get_image_uri(self, obj):
        request = self.context.get('request')
        get_image = obj.image.url
        return request.build_absolute_uri(get_image)

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