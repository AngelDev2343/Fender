from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'app_fender'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('shop/', views.product_list_view, name='product_list'),
    path('categories/', views.category_list_view, name='category_list'),
    path('product/<slug:product_slug>/', views.product_detail_view, name='product_detail'),
    path('search/', views.search_view, name='search'),

    path('support/', TemplateView.as_view(template_name='support.html'), name='support'),
    path('custom/', TemplateView.as_view(template_name='custom.html'), name='custom'),

    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='app_fender:login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),

    path('admin-panel/', views.admin_panel_view, name='admin_panel'),

    # Users
    path('admin-panel/users/', views.admin_user_list, name='admin_user_list'),
    path('admin-panel/users/create/', views.admin_user_create, name='admin_user_create'),
    path('admin-panel/users/<int:user_id>/view/', views.admin_user_view, name='admin_user_view'),
    path('admin-panel/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin-panel/users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),

    # Categories
    path('admin-panel/categories/', views.admin_category_list, name='admin_category_list'),
    path('admin-panel/categories/create/', views.admin_category_create, name='admin_category_create'),
    path('admin-panel/categories/<int:category_id>/view/', views.admin_category_view, name='admin_category_view'),
    path('admin-panel/categories/<int:category_id>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path('admin-panel/categories/<int:category_id>/delete/', views.admin_category_delete, name='admin_category_delete'),

    # Products
    path('admin-panel/products/', views.admin_product_list, name='admin_product_list'),
    path('admin-panel/products/create/', views.admin_product_create, name='admin_product_create'),
    path('admin-panel/products/<int:product_id>/view/', views.admin_product_view, name='admin_product_view'),
    path('admin-panel/products/<int:product_id>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('admin-panel/products/<int:product_id>/delete/', views.admin_product_delete, name='admin_product_delete'),

    # Variants
    path('admin-panel/variants/<int:variant_id>/view/', views.admin_variant_view, name='admin_variant_view'),
    path('admin-panel/variants/<int:variant_id>/edit/', views.admin_variant_edit, name='admin_variant_edit'),

    # Orders
    path('admin-panel/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin-panel/orders/create/', views.admin_order_create, name='admin_order_create'),
    path('admin-panel/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-panel/orders/<int:order_id>/edit/', views.admin_order_edit, name='admin_order_edit'),
    path('admin-panel/orders/<int:order_id>/delete/', views.admin_order_delete, name='admin_order_delete'),

    # Cart
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('cart/add/<int:variant_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/remove-one/<int:item_id>/', views.remove_one_from_cart_view, name='remove_one_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<int:order_id>/confirmation/', views.order_confirmation_view, name='order_confirmation'),
]
