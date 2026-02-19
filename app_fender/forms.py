
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Order, Category, Product, ProductVariant
from django.forms.models import inlineformset_factory

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password1", "password2")

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'shipping_full_name',
            'shipping_address_line1',
            'shipping_address_line2',
            'shipping_city',
            'shipping_state',
            'shipping_postal_code',
            'shipping_country',
            'shipping_phone'
        ]
        labels = {
            'shipping_full_name': 'Full Name',
            'shipping_address_line1': 'Address Line 1',
            'shipping_address_line2': 'Address Line 2 (Optional)',
            'shipping_city': 'City',
            'shipping_state': 'State / Province',
            'shipping_postal_code': 'Postal Code',
            'shipping_country': 'Country',
            'shipping_phone': 'Phone Number'
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'image',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ('color', 'model_number', 'price', 'stock', 'image', 'secondary_image', 'youtube_link')
        widgets = {
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'youtube_link': forms.URLInput(attrs={'class': 'form-control'}),
        }

ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant, form=ProductVariantForm,
    extra=1, can_delete=True
)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'status',
            'is_paid',
            'shipping_full_name',
            'shipping_address_line1',
            'shipping_address_line2',
            'shipping_city',
            'shipping_state',
            'shipping_postal_code',
            'shipping_country',
            'shipping_phone',
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shipping_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_state': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_country': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomUserEditForm(forms.ModelForm):
    password_hash = forms.CharField(
        label='Password Hash (Read-Only)',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['password_hash'] = self.instance.password
        self.fields.update({'password_hash': self.fields.pop('password_hash')})
