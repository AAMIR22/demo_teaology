# admin.py
from django.contrib import admin
from .models import Customer, Category, Product, Cart, CartItem, Sale

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

class SaleAdmin(admin.ModelAdmin):
    list_display = ('cart', 'total_price', 'date')
    search_fields = ('cart__customer__name',)

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Sale, SaleAdmin)
