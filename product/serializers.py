from urllib import request
from rest_framework import serializers

from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):

    get_image = serializers.SerializerMethodField('image_url')
    get_thumbnail = serializers.SerializerMethodField('thumbnail_url')


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

    def thumbnail_url(self, obj):
        request = self.context.get("request")

        if obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        else:
            if obj.image:
                obj.thumbnail = obj.make_thumbnail(obj.image)
                obj.save()

                return request.build_absolute_uri(obj.thumbnail.url)
            else:
                return ''

        

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )