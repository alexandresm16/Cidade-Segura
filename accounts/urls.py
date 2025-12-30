# accounts/urls.py
from django.urls import path
from .views import RegisterView, ActivateAccountView, UserLoginView, LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate-account'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
