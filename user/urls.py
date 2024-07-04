from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RegisterView,CustomAuthToken, ProfileView, LogoutView,UserListView

router = DefaultRouter()
router.register(r'users', UserListView)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]