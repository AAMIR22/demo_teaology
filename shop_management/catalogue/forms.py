from django import forms
from .models import CartItem, Customer, Cart

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['discount']
