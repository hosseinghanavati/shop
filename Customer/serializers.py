from rest_framework import serializers

from Core.models import User
from .models import Customer, Address


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.phone')

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['id']


class UserPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id']


class AddressPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'owner', 'province']
        read_only_fields = ['id', 'owner']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['id', 'owner']

