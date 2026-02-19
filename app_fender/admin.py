from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, 
    Category, 
    Product, 
    ProductVariant, 
    Cart, 
    CartItem, 
    Order, 
    OrderItem
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1 
    fields = ('color', 'model_number', 'price', 'stock', 'image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'product', 'color', 'price', 'stock', 'model_number')
    list_filter = ('product__category', 'product')
    search_fields = ('product__name', 'color', 'model_number')
    autocomplete_fields = ('product',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0 
    fields = ('product_variant', 'quantity', 'get_total_item_price')
    readonly_fields = ('get_total_item_price',)
    autocomplete_fields = ('product_variant',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'session_key', 'created_at', 'get_total_price')
    readonly_fields = ('created_at', 'get_total_price', 'user', 'session_key')
    search_fields = ('user__email', 'session_key')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product_variant', 'quantity')
    autocomplete_fields = ('cart', 'product_variant')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product_variant', 'quantity', 'price')
    readonly_fields = ('product_variant', 'quantity', 'price')
    can_delete = False 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('id', 'user__email')
    readonly_fields = ('user', 'created_at', 'total_amount')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variant', 'quantity', 'price')
    readonly_fields = ('order', 'product_variant', 'quantity', 'price')
    autocomplete_fields = ('order', 'product_variant')
