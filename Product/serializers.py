from rest_framework import serializers

from .models import Product, Category, Discount, Brand


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):

    # product = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = Category
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


