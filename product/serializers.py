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

# class ProductSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     subcategory = SubcategorySerializer()
#     brand = BrandSerializer()
#     unit = UnitSerializer()
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'category', 'subcategory', 'brand', 'unit', 'sku', 'min_quantity', 'quantity',
#                   'description', 'tax', 'discount_type', 'price', 'status', 'image_url', 'user']

# class ProductSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     subcategory = SubcategorySerializer()
#     brand = BrandSerializer()
#     unit = UnitSerializer()
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'category', 'subcategory', 'brand', 'unit', 'sku', 'min_quantity', 'quantity',
#                   'description', 'tax', 'discount_type', 'price', 'status', 'image_url', 'user']

#     def create(self, validated_data):
#         category_data = validated_data.pop('category')
#         subcategory_data = validated_data.pop('subcategory')
#         brand_data = validated_data.pop('brand')
#         unit_data = validated_data.pop('unit')

#         category, created = Category.objects.get_or_create(**category_data)
#         subcategory, created = Subcategory.objects.get_or_create(name=subcategory_data['name'], category=category)
#         brand, created = Brand.objects.get_or_create(**brand_data)
#         unit, created = Unit.objects.get_or_create(**unit_data)

#         user = self.context['request'].user
#         if not user.is_authenticated:
#             raise serializers.ValidationError('Authentication required to create a product.')

#         validated_data.pop('user', None)  # Remove user if present in validated_data

#         product = Product.objects.create(category=category, subcategory=subcategory, brand=brand, unit=unit, user=user, **validated_data)
#         return product

#     def update(self, instance, validated_data):
#         category_data = validated_data.pop('category', None)
#         subcategory_data = validated_data.pop('subcategory', None)
#         brand_data = validated_data.pop('brand', None)
#         unit_data = validated_data.pop('unit', None)

#         if category_data:
#             for attr, value in category_data.items():
#                 setattr(instance.category, attr, value)
#             instance.category.save()

#         if subcategory_data:
#             for attr, value in subcategory_data.items():
#                 setattr(instance.subcategory, attr, value)
#             instance.subcategory.save()

#         if brand_data:
#             for attr, value in brand_data.items():
#                 setattr(instance.brand, attr, value)
#             instance.brand.save()

#         if unit_data:
#             for attr, value in unit_data.items():
#                 setattr(instance.unit, attr, value)
#             instance.unit.save()

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         return instance



# VALID CODE 

# class ProductSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all())
#     brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
#     unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'category', 'subcategory', 'brand', 'unit', 'sku', 'min_quantity', 'quantity',
#                   'description', 'tax', 'discount_type', 'price', 'status', 'image_url', 'user']

#     def create(self, validated_data):
#         user = self.context['request'].user
#         if not user.is_authenticated:
#             raise serializers.ValidationError('Authentication required to create a product.')
        
#         validated_data['user'] = user
#         product = Product.objects.create(**validated_data)
#         return product

#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance



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