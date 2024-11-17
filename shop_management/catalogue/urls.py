from django.urls import path
from . import views
app_name="catalogue"
urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.product_list, name='product_list'),
    path('product/<int:product_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'), path('checkout/', views.checkout, name='checkout'),
    path('download_sales_data/', views.download_sales_data, name='download_sales_data'),
    path('sales_details/', views.sales_details, name='sales_details'),
    path('sales_details/edit/<int:sale_id>/', views.edit_sale, name='edit_sale'),
    path('sales_details/<int:sale_id>/', views.sale_details_view, name='sale_details_view'),
    path('edit_cart_item/<int:cart_item_id>/', views.edit_cart_item, name='edit_cart_item'),
    path('edit_cart_item/<int:cart_item_id>/', views.edit_cart_item, name='edit_cart_item'),
    path('edit_discount/<int:sale_id>/', views.edit_discount, name='edit_discount'),
]
