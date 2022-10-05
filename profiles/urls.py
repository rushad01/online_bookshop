from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'profiles'
urlpatterns = [
    path('register/', views.RegistrationFormView, name='register'),
    path('profile/', views.ProfileView, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html'), name="login"),
]
