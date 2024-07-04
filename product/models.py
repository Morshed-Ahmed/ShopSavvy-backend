from django.db import models
from user.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)
    min_quantity = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_type = models.CharField(max_length=10, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')], default='percentage')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    image_url = models.URLField(blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name