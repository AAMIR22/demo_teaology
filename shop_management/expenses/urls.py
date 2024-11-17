from django.contrib import admin
from django.urls import path
from expenses import views
app_name="expenses"
urlpatterns = [
    path('', views.index, name='expense_list'),
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('salaries/', views.salary_list, name='salary_list'),
    path('electricity/', views.electricity_list, name='electricity_list'),
    path('rent/', views.rent_list, name='rent_list'),
    path('marketing/', views.marketing_list, name='marketing_list'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('employees/', views.employee_register, name='employee_register'),
    path('purchases/add/', views.add_purchase, name='add_purchase'),
    path('export-expenses/', views.export_expenses_to_excel, name='export_expenses'),
    path('export-expenses1/', views.export_expenses_to_exceldate, name='export_expensesdate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
