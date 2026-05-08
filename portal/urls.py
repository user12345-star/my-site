from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('sale/', views.sale, name='sale'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category, name='category'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('order/', views.order, name='order'),
    path('done/', views.done, name='done'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]
