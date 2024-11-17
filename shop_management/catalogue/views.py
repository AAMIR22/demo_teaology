
from django.http import  HttpResponseRedirect
from django.urls import reverse
from .models import  CartItem

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Cart, Sale
from .forms import CartItemForm, CustomerForm, DiscountForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'product_list.html', {'category': category, 'products': products})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    else:
        cart = Cart.objects.get(id=cart_id)

    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.cart = cart
            cart_item.save()
            return redirect('catalogue:category_list')
    else:
        form = CartItemForm(initial={'product': product})

    return render(request, 'add_to_cart.html', {'form': form, 'product': product})


def view_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            categories = Category.objects.all()
            return render(request, 'category_list.html', {'categories': categories})

        if request.method == 'POST':
            discount_form = DiscountForm(request.POST, instance=cart)
            if discount_form.is_valid():
                discount_form.save()
                return redirect('catalogue:view_cart')
        else:
            discount_form = DiscountForm(instance=cart)
        cart = get_object_or_404(Cart, id=cart_id)
        return render(request, 'view_cart.html', {'cart': cart,'discount_form': discount_form})
    else:
        categories = Category.objects.all()
        return render(request, 'category_list.html', {'categories': categories})


def checkout(request):
    cart_id = request.session.get('cart_id')
    cart = get_object_or_404(Cart, id=cart_id)
    items= CartItem.objects.filter(cart=cart)
    if not Sale.objects.filter(cart=cart).exists():
        if request.method == 'POST':
            customer_form = CustomerForm(request.POST)
            if customer_form.is_valid():
                customer = customer_form.save()
                cart.customer = customer
                cart.save()
        sale = Sale.objects.create(cart=cart, total_price=cart.total_price())
        del request.session['cart_id']  # Clear the session cart ID after checkout
        return render(request, 'summary.html', {'sale': sale,'item':items})
    else:
        return render(request, 'summary.html', {'sale': Sale.objects.get(cart=cart)})


def download_sales_data(request):
    sales = Sale.objects.all()
    data = []

    for sale in sales:
        for item in sale.cart.items.all():
            data.append({
                'Customer Name': sale.cart.customer.name if sale.cart.customer else 'Anonymous',
                'Customer Email': sale.cart.customer.email if sale.cart.customer else 'N/A',
                'Order ID': sale.cart.id,
                'Product Name': item.product.name,
                'Category': item.product.category,
                'Price per Unit': item.product.price,
                'Quantity Sold': item.quantity,
                'Total Sales': item.quantity * item.product.price,
                'Discount': sale.cart.discount,
                'Net Total': sale.total_price,
                'Date': sale.date.replace(tzinfo=None),
            })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_data.xlsx'
    df.to_excel(response, index=False)

    return response



def sales_details(request):
    sales = Sale.objects.all()
    return render(request, 'sales_details.html', {'sales': sales})

def edit_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, instance=sale.cart.customer)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('catalogue:sales_details')
    else:
        customer_form = CustomerForm(instance=sale.cart.customer)
    return render(request, 'edit_sale.html', {'sale': sale, 'customer_form': customer_form})



def sale_details_view(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    cart_items = sale.cart.items.all()
    discount_form = DiscountForm(instance=sale.cart)
    return render(request, 'sale_details.html', {'sale': sale, 'cart_items': cart_items, 'discount_form': discount_form})

def edit_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            # Recalculate total price after editing cart item
            cart_item.cart.save()
            sale = Sale.objects.get(cart=cart_item.cart)
            sale.save()
            return HttpResponseRedirect(reverse('catalogue:sale_details_view', args=[cart_item.cart.sale.id]))
    else:
        form = CartItemForm(instance=cart_item)
    return render(request, 'edit_cart_item.html', {'form': form, 'cart_item': cart_item})

def edit_discount(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        discount_form = DiscountForm(request.POST, instance=sale.cart)
        if discount_form.is_valid():
            discount_form.save()
            # Recalculate total price after updating discount
            sale.total_price = sale.cart.total_price()
            sale.save()
            return redirect('catalogue:sale_details_view', sale_id=sale.id)
    else:
        discount_form = DiscountForm(instance=sale.cart)
    return render(request, 'edit_discount.html', {'sale': sale, 'discount_form': discount_form})



