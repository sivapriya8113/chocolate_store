from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Chocolate, Carts, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','first_name','last_name')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email','password','first_name','last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data.get('first_name',''),
            last_name = validated_data.get('last_name',''),
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs['email'],password = attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password')
        attrs['user']=user
        return attrs

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        refresh = RefreshToken.for_user(instance)
        response_data['access_token'] = str(refresh.access_token)
        response_data['refresh_token'] = str(refresh)
        response_data['user_id'] = instance.id
        return response_data


class ChocoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chocolate
        # fields = '__all__'
        fields = ('id', 'category', 'description', 'price', 'image_url', 'choco_available')


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    date = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    quantity = serializers.CharField(read_only=True)

    class Meta:
        model = Carts
        fields = ["id", "product", "user", "date", "status", "quantity"]

    def create(self, validated_data):
        user = self.context.get('user')
        product = self.context.get('product')
        return product.carts_set.create(**validated_data, user=user)
