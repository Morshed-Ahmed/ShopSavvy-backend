from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from .serializers import CategorySerializer,SubcategorySerializer,BrandSerializer,UnitSerializer,ProductSerializer
from .models import Category,Subcategory,Brand, Unit, Product

from rest_framework import serializers
from rest_framework import viewsets, permissions, filters
import django_filters



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

