from rest_framework import serializers

from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):

    products = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Category
        fields = '__all__'



