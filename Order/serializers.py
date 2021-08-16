from rest_framework import serializers

from Order.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True, read_only=True)


    class Meta:
        model = Order
        fields = '__all__'

