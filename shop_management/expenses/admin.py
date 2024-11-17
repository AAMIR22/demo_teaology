from django.contrib import admin
from .models import Employee, Purchase, SalaryPayment, ElectricityBill, RentPayment, MarketingExpense, EquipmentExpense, \
    Vendor

admin.site.register(Vendor)
admin.site.register(Employee)
admin.site.register(Purchase)
admin.site.register(SalaryPayment)
admin.site.register(ElectricityBill)
admin.site.register(RentPayment)
admin.site.register(MarketingExpense)
admin.site.register(EquipmentExpense)
