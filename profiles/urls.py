from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'profiles'
urlpatterns = [
    path('register/', views.RegistrationFormView, name='register'),
    path('profile/', views.ProfileView, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='profiles/logout.html'), name='logout'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('product/<str:book_name>',
         views.productDetail, name='product-detail'),
]
