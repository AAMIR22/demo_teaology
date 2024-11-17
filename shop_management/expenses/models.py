from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()
    contact_number = models.CharField(max_length=15)
    created_date = models.DateTimeField(default=timezone.now)  # Auto creation date

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    salary_type = models.CharField(max_length=10, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contact_number = models.CharField(max_length=15)
    hire_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)  # Auto creation date

    def __str__(self):
        return self.name

class Purchase(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_date = models.DateTimeField(default=timezone.now)  # Auto creation date

class SalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_from = models.DateField()
    paid_to = models.DateField()
    date = models.DateField()
    created_date = models.DateTimeField(default=timezone.now)  # Auto creation date

class ElectricityBill(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_status = models.BooleanField(default=False)
    date_from = models.DateField()
    date_to = models.DateField()
    created_date = models.DateTimeField(default=timezone.now)  # Auto creation date

class RentPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_from = models.DateField()
    date_to = models.DateField()
    paid_status = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)  # Auto creation date

class MarketingExpense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_date = models.DateTimeField(default=timezone.now)  # Auto creation date

class EquipmentExpense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_date = models.DateTimeField(default=timezone.now)  # Auto creation date
