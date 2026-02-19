from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.db import transaction
from django.contrib import messages

from .models import Product, ProductVariant, Category, Cart, CartItem, CustomUser, Order, OrderItem
from .forms import (CustomUserCreationForm, ShippingAddressForm, CustomUserEditForm,
                   CategoryForm, ProductForm, ProductVariantForm, OrderForm, ProductVariantFormSet)

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            user__isnull=True
        )
    return cart

def home_view(request):
    featured_products = Product.objects.all()[:5]
    context = {
        'products': featured_products
    }
    return render(request, 'index.html', context)

def product_list_view(request):
    query = request.GET.get('query')
    category_slug = request.GET.get('category')
    products = Product.objects.all()
    selected_category = None

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        ).distinct()

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    context = {
        'products': products,
        'selected_category': selected_category,
        'query': query,
    }

    if category_slug:
        template_name = 'categoria1.html'
    else:
        template_name = 'shop.html'

    return render(request, template_name, context)

def category_list_view(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'categoria.html', context)

def product_detail_view(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    all_variants = ProductVariant.objects.filter(product=product).order_by('color')

    if not all_variants.exists():
        return render(request, 'buy.html', {'product': product, 'variants': []})

    selected_variant_id = request.GET.get('variant_id')

    if selected_variant_id:
        try:
            main_variant = all_variants.get(id=selected_variant_id)
        except ProductVariant.DoesNotExist:
            main_variant = all_variants.first()
    else:
        main_variant = all_variants.first()

    context = {
        'product': product,
        'main_variant': main_variant,
        'all_variants': all_variants
    }
    return render(request, 'buy.html', context)

def search_view(request):
    query = request.GET.get('search')
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'products': products
    }
    return render(request, 'shop.html', context)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('app_fender:profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'profile.html', context)

def is_superuser(user):
    return user.is_superuser

def is_superuser(user):
    return user.is_superuser

def is_staff_or_superuser(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_panel_view(request):
    total_users = CustomUser.objects.count()
    total_categories = Category.objects.count()
    total_products = Product.objects.count()
    total_variants = ProductVariant.objects.count()
    total_orders = Order.objects.count()

    context = {
        'total_users': total_users,
        'total_categories': total_categories,
        'total_products': total_products,
        'total_variants': total_variants,
        'total_orders': total_orders,
    }
    return render(request, 'admin_panel.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    context = {'users': users}
    return render(request, 'admin/user_list.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('app_fender:admin_user_list')
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'action': 'Create'}
    return render(request, 'admin/user_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_user_view(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)
    context = {'user_obj': user_obj}
    return render(request, 'admin/user_view.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_user_edit(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('app_fender:admin_user_list')
    else:
        form = CustomUserEditForm(instance=user_obj)

    context = {'form': form, 'action': 'Edit', 'user': user_obj}
    return render(request, 'admin/user_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_user_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('app_fender:admin_user_list')

    context = {'user': user}
    return render(request, 'admin/user_confirm_delete.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_category_list(request):
    categories = Category.objects.all().order_by('name')
    context = {'categories': categories}
    return render(request, 'admin/category_list.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('app_fender:admin_category_list')
    else:
        form = CategoryForm()

    context = {'form': form, 'action': 'Create'}
    return render(request, 'admin/category_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = {'category': category}
    return render(request, 'admin/category_view.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('app_fender:admin_category_list')
    else:
        form = CategoryForm(instance=category)

    context = {'form': form, 'action': 'Edit', 'category': category}
    return render(request, 'admin/category_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('app_fender:admin_category_list')

    context = {'category': category}
    return render(request, 'admin/category_confirm_delete.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
@transaction.atomic
def admin_product_create(request):
    initial_data = {}
    if 'category' in request.GET:
        initial_data['category'] = request.GET.get('category')

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        variant_formset = ProductVariantFormSet(request.POST, request.FILES)

        if product_form.is_valid() and variant_formset.is_valid():
            product = product_form.save()
            variant_formset.instance = product
            variant_formset.save()
            messages.success(request, 'Product and variants created successfully!')
            return redirect('app_fender:admin_product_list')
    else:
        product_form = ProductForm(initial=initial_data)
        variant_formset = ProductVariantFormSet(instance=Product())

    context = {
        'product_form': product_form,
        'variant_formset': variant_formset,
        'action': 'Create'
    }
    return render(request, 'admin/product_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'admin/product_view.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
@transaction.atomic
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        variant_formset = ProductVariantFormSet(request.POST, request.FILES, instance=product)

        if product_form.is_valid() and variant_formset.is_valid():
            product = product_form.save()
            variant_formset.save()
            messages.success(request, 'Product and variants updated successfully!')
            return redirect('app_fender:admin_product_list')
    else:
        product_form = ProductForm(instance=product)
        variant_formset = ProductVariantFormSet(instance=product)

    context = {
        'product_form': product_form,
        'variant_formset': variant_formset,
        'action': 'Edit',
        'product': product
    }
    return render(request, 'admin/product_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_product_list(request):
    products = Product.objects.select_related('category').all()

    category_id = request.GET.get('category')
    selected_category = None

    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            products = products.filter(category=selected_category)
        except Category.DoesNotExist:
            pass

    products = products.order_by('name')
    context = {
        'products': products,
        'selected_category': selected_category
    }
    return render(request, 'admin/product_list.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('app_fender:admin_product_list')

    context = {'product': product}
    return render(request, 'admin/product_confirm_delete.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_variant_list(request):
    variants = ProductVariant.objects.select_related('product').all().order_by('product__name', 'color')
    context = {'variants': variants}
    return render(request, 'admin/variant_list.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_variant_create(request):
    if request.method == 'POST':
        form = ProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product variant created successfully!')
            return redirect('app_fender:admin_variant_list')
    else:
        form = ProductVariantForm()

    context = {'form': form, 'action': 'Create'}
    return render(request, 'admin/variant_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_variant_view(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    context = {'variant': variant}
    return render(request, 'admin/variant_view.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_variant_edit(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if request.method == 'POST':
        form = ProductVariantForm(request.POST, request.FILES, instance=variant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product variant updated successfully!')
            return redirect('app_fender:admin_variant_list')
    else:
        form = ProductVariantForm(instance=variant)

    context = {'form': form, 'action': 'Edit', 'variant': variant}
    return render(request, 'admin/variant_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_variant_delete(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if request.method == 'POST':
        variant.delete()
        messages.success(request, 'Product variant deleted successfully!')
        return redirect('app_fender:admin_variant_list')

    context = {'variant': variant}
    return render(request, 'admin/variant_confirm_delete.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_order_list(request):
    orders = Order.objects.select_related('user').all().order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'admin/order_list.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.select_related('product_variant__product').all()

    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'admin/order_detail.html', context)

def cart_detail_view(request):
    cart = _get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.get_total_item_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

def add_to_cart_view(request, variant_id):
    quantity = 1
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

    variant = get_object_or_404(ProductVariant, id=variant_id)

    if quantity < 1:
        return redirect('app_fender:product_detail', product_slug=variant.product.slug)

    cart = _get_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_variant=variant,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('app_fender:cart_detail')

def remove_from_cart_view(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('app_fender:cart_detail')

def remove_one_from_cart_view(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('app_fender:cart_detail')

@login_required
def checkout_view(request):
    cart = _get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('app_fender:cart_detail')

    total_price = sum(item.get_total_item_price() for item in cart_items)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_amount = total_price
                    order.is_paid = True
                    order.save()

                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product_variant=item.product_variant,
                            quantity=item.quantity,
                            price=item.product_variant.price
                        )

                        item.product_variant.stock -= item.quantity
                        item.product_variant.save()

                    cart_items.delete()

                    return redirect('app_fender:order_confirmation', order_id=order.id)

            except Exception as e:
                print(f"Error during checkout: {e}")

    else:
        initial_data = {
            'shipping_full_name': f"{request.user.first_name} {request.user.last_name}",
        }
        form = ShippingAddressForm(initial=initial_data)

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'checkout.html', context)

@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()

    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'order_confirmation.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            try:
                order.user = CustomUser.objects.get(id=request.user.id)
            except CustomUser.DoesNotExist:
                messages.error(request, 'Error: No user found to assign the order. Please ensure a user exists.')
                return render(request, 'admin/order_form.html', {'form': form, 'action': 'Create'})

            order.total_amount = 0.00
            order.save()
            messages.success(request, f'Order {order.id} created successfully! (Must manually add OrderItems)')
            return redirect('app_fender:admin_order_list')
    else:
        form = OrderForm()

    context = {'form': form, 'action': 'Create'}
    return render(request, 'admin/order_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Order {order.id} updated successfully!')
            return redirect('app_fender:admin_order_list')
    else:
        form = OrderForm(instance=order)

    context = {'form': form, 'action': 'Edit', 'order': order}
    return render(request, 'admin/order_form.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.delete()
        messages.success(request, f'Order {order.id} deleted successfully!')
        return redirect('app_fender:admin_order_list')

    context = {'order': order}
    return render(request, 'admin/order_confirm_delete.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'admin/order_list.html', context)

@login_required
@user_passes_test(is_staff_or_superuser)
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    context = {'order': order, 'order_items': order_items}
    return render(request, 'admin/order_detail.html', context)
