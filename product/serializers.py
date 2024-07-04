from rest_framework import serializers
from .models import Category,Subcategory,Brand,Unit,Product
from user.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']



class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'subcategory', 'brand', 'unit', 'sku', 'min_quantity', 'quantity',
                  'description', 'tax', 'discount_type', 'price', 'status', 'image_url', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError('Authentication required to create a product.')
        
        validated_data['user'] = user
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        # Ensure user field is not updated
        validated_data.pop('user', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance