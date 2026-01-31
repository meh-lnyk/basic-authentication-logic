from django.urls import path
from .views import RegistrationView, LoginView, ProfileView, LogoutView, SoftDeleteView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete-account/', SoftDeleteView.as_view(), name='soft-delete'),
]
