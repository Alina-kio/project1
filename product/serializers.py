from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'price', 'default_delivery_price', 'default_delivery_time']
        # fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'



class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemsSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    product = ProductSerializer()
    class Meta:
        model = CartItems
        # fields = '__all__'
        fields = ['cart', 'product', 'quantity', 'price']



class OrderSerializer(serializers.ModelSerializer):
    cart_items = CartItemsSerializer(many=True, write_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cart_items')
        order = Order.objects.create(**validated_data)

        for cart_item_data in cart_items_data:
            CartItems.objects.create(order=order, **cart_item_data)

        return order


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItems
        fields = '__all__'

