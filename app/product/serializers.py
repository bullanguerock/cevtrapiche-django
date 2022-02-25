from rest_framework import serializers

from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    try:
        get_image = serializers.SerializerMethodField('image_url')
        get_thumbnail = serializers.SerializerMethodField('thumbnail_url')
    except:
        get_image = ''
        get_thumbnail = ''

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail",
            "inventory"
        )
    def image_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        else:
            return ''

    def thumbnail_url(self, obj):
        request = self.context.get("request")

        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        else:
            if obj.image and request:
                obj.thumbnail = obj.make_thumbnail(obj.image)
                obj.save()

                return request.build_absolute_uri(obj.thumbnail.url)
            else:
                return ''

        

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )


