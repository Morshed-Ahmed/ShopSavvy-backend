from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from .serializers import CategorySerializer,SubcategorySerializer,BrandSerializer,UnitSerializer,ProductSerializer
from .models import Category,Subcategory,Brand, Unit, Product


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]





from rest_framework import serializers

   
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         user = self.request.user
#         if not user.is_authenticated:
#             return Product.objects.all()
#         if user.is_superuser or user.role == 'admin':
#             return Product.objects.all()
#         elif user.role == 'seller':
#             return Product.objects.filter(user=user)
#         else:
#             return Product.objects.none()

#     def perform_create(self, serializer):
#         if not self.request.user.is_authenticated:
#             raise serializers.ValidationError('Authentication required to create a product.')
#         serializer.save(user=self.request.user)

#     @action(detail=True, methods=['post'])
#     def change_status(self, request, pk=None):
#         product = self.get_object()
#         new_status = request.data.get('status')

#         if new_status not in ['active', 'inactive']:
#             return Response({'error': 'Invalid status'}, status=400)

#         product.status = new_status
#         product.save()
#         return Response({'status': product.status})

#     @action(detail=False, methods=['get'])
#     def seller_products(self, request):
#         if not request.user.is_authenticated:
#             return Response({'error': 'Authentication required'}, status=403)
        
#         seller_products = Product.objects.filter(user=request.user)
#         serializer = ProductSerializer(seller_products, many=True)
#         return Response(serializer.data)



from rest_framework import viewsets, permissions, filters


import django_filters


class ProductFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)

    class Meta:
        model = Product
        fields = ['status']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku', 'brand__name', 'unit__name']
    ordering_fields = ['price', 'name', 'status']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.all()
        
        if not user.is_authenticated:
            return queryset
        
        if user.is_superuser or user.role == 'admin':
            queryset = Product.objects.all()
        elif user.role == 'seller':
            queryset = Product.objects.filter(user=user)
        else:
            queryset = Product.objects.none()
        
        return queryset

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError('Authentication required to create a product.')
        serializer.save(user=self.request.user)




    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response({'error': 'Authentication required to delete a product.'}, status=403)
        
        if user.is_superuser or user.role == 'admin' or (user.role == 'seller' and instance.user == user):
            self.perform_destroy(instance)
            return Response(status=204)
        else:
            return Response({'error': 'You do not have permission to delete this product.'}, status=403)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        if not user.is_authenticated:
            return Response({'error': 'Authentication required to update a product.'}, status=403)
        
        if user.is_superuser or user.role == 'admin' or (user.role == 'seller' and instance.user == user):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'error': 'You do not have permission to update this product.'}, status=403)



    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        product = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['active', 'inactive']:
            return Response({'error': 'Invalid status'}, status=400)

        product.status = new_status
        product.save()
        return Response({'status': product.status})

    @action(detail=False, methods=['get'])
    def seller_products(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=403)
        
        seller_products = Product.objects.filter(user=request.user)
        serializer = ProductSerializer(seller_products, many=True)
        return Response(serializer.data)


# from rest_framework import viewsets, filters, permissions
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from django_filters import rest_framework as django_filters
# from .models import Product
# from .serializers import ProductSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, django_filters.DjangoFilterBackend]
#     filterset_class = ProductFilter
#     search_fields = ['name', 'description', 'sku', 'brand__name', 'unit__name']
#     ordering_fields = ['price', 'name', 'status']
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         user = self.request.user
        
#         if not user.is_authenticated:
#             return Product.objects.none()  # Return empty queryset for unauthenticated users
        
#         if user.is_superuser or user.role == 'admin':
#             return Product.objects.all()  # Admin can see all products
#         elif user.role == 'seller':
#             if not user.has_perm('product.view_product'):  # Assuming permission 'view_product_list' is defined
#                 return Product.objects.none()  # Seller without permission sees no products
#             else:
#                 return Product.objects.filter(user=user)  # Seller with permission sees own products
#         else:
#             return Product.objects.none()  # Other roles see no products

#     def perform_create(self, serializer):
#         if not self.request.user.is_authenticated:
#             raise serializers.ValidationError('Authentication required to create a product.')
#         serializer.save(user=self.request.user)

#     @action(detail=True, methods=['post'])
#     def change_status(self, request, pk=None):
#         product = self.get_object()
#         new_status = request.data.get('status')

#         if new_status not in ['active', 'inactive']:
#             return Response({'error': 'Invalid status'}, status=400)

#         product.status = new_status
#         product.save()
#         return Response({'status': product.status})

#     @action(detail=False, methods=['get'])
#     def seller_products(self, request):
#         if not request.user.is_authenticated:
#             return Response({'error': 'Authentication required'}, status=403)
        
#         seller_products = Product.objects.filter(user=request.user)
#         serializer = ProductSerializer(seller_products, many=True)
#         return Response(serializer.data)


# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.shortcuts import get_object_or_404
# from .models import User
# from django.contrib.auth.models import Permission

# @api_view(['POST'])
# @permission_classes([permissions.IsAdminUser])  # Ensure only admin can grant permission
# def grant_permission(request, seller_id):
#     seller = get_object_or_404(User, pk=seller_id)
#     permission = Permission.objects.get(codename='product.view_product')  # Fetch the correct permission object
#     seller.user_permissions.add(permission)  # Grant the permission to the seller
#     return Response({'message': 'Permission granted successfully.'}, status=status.HTTP_200_OK)

