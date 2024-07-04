from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register ViewSets
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'subcategories', views.SubcategoryViewSet)
router.register(r'brands', views.BrandViewSet)
router.register(r'units', views.UnitViewSet)
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('products/change-status/<int:pk>/', views.ProductViewSet.as_view({'post': 'change_status'}), name='product-change-status'),
    path('products/seller-products/', views.ProductViewSet.as_view({'get': 'seller_products'}), name='seller-products'),
]

