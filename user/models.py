# from django.db import models
# from django.contrib.auth.models import AbstractUser

# # Create your models here.
# class User(AbstractUser):
#     ROLES = (
#         ('admin', 'Admin'),
#         ('seller', 'Seller'),
#     )
#     role = models.CharField(max_length=10, choices=ROLES, default='seller')

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='user_groups',
#         blank=True,
#         help_text=('The groups this user belongs to. A user will get all permissions '
#                    'granted to each of their groups.'),
#         verbose_name=('groups'),
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='user_permissions',
#         blank=True,
#         help_text=('Specific permissions for this user.'),
#         verbose_name=('user permissions'),
#     )

#     def save(self, *args, **kwargs):
#         if self.is_superuser:
#             self.role = 'admin'
#         super().save(*args, **kwargs)

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLES, blank=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)


