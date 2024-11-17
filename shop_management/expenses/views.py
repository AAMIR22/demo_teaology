from django.shortcuts import render, redirect
from .models import Purchase, SalaryPayment, ElectricityBill, RentPayment, MarketingExpense, EquipmentExpense, Employee, Vendor

def index(request):
    return render(request, 'expenses/expense_list.html')

def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'expenses/purchase_list.html', {'purchases': purchases})

def salary_list(request):
    salaries = SalaryPayment.objects.all()
    return render(request, 'expenses/salary_list.html', {'salaries': salaries})

def electricity_list(request):
    bills = ElectricityBill.objects.all()
    return render(request, 'expenses/electricity_list.html', {'bills': bills})

def rent_list(request):
    rents = RentPayment.objects.all()
    return render(request, 'expenses/rent_list.html', {'rents': rents})

def marketing_list(request):
    expenses = MarketingExpense.objects.all()
    return render(request, 'expenses/marketing_list.html', {'expenses': expenses})

def equipment_list(request):
    expenses = EquipmentExpense.objects.all()
    return render(request, 'expenses/equipment_list.html', {'expenses': expenses})

def employee_register(request):
    employees = Employee.objects.all()
    return render(request, 'expenses/employee_register.html', {'employees': employees})

# Add views for adding, editing, and deleting records directly in the templates
def add_purchase(request):
    if request.method == 'POST':
        vendor = Vendor.objects.get(id=request.POST['vendor'])
        item = request.POST['item']
        amount = request.POST['amount']
        date = request.POST['date']
        Purchase.objects.create(vendor=vendor, item=item, amount=amount, date=date)
        return redirect('expenses:purchase_list')
    vendors = Vendor.objects.all()
    return render(request, 'expenses/add_purchase.html', {'vendors': vendors})

# Define similar add, edit, and delete views for other models

import pandas as pd
import sqlite3
from django.http import HttpResponse

def export_expenses_to_excel(request):
    db_path = 'db.sqlite3'
    queries = {
        "Vendor": "SELECT id, name, contact_info, contact_number FROM expenses_vendor",
        "Employee": "SELECT id, name, position, salary_type, salary_amount, advance_payment FROM expenses_employee",
        "Purchase": """
            SELECT p.id, v.name AS vendor_name, p.item, p.amount, p.date
            FROM expenses_purchase p
            JOIN expenses_vendor v ON p.vendor_id = v.id
        """,
        "SalaryPayment": """
            SELECT sp.id, e.name AS employee_name, sp.amount, sp.paid_from, sp.paid_to, sp.date
            FROM expenses_salarypayment sp
            JOIN expenses_employee e ON sp.employee_id = e.id
        """,
        "ElectricityBill": "SELECT id, amount, due_date, paid_status, date_from, date_to FROM expenses_electricitybill",
        "RentPayment": "SELECT id, amount, date_from, date_to, paid_status FROM expenses_rentpayment",
        "MarketingExpense": "SELECT id, description, amount, date FROM expenses_marketingexpense",
        "EquipmentExpense": "SELECT id, description, amount, date FROM expenses_equipmentexpense"
    }

    data = {}
    conn = sqlite3.connect(db_path)
    for sheet_name, query in queries.items():
        df = pd.read_sql_query(query, conn)
        data[sheet_name] = df
    conn.close()

    # Create a Pandas Excel writer using BytesIO as the buffer
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Set the response to download the file
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=expenses_report.xlsx'
    return response


import pandas as pd
import sqlite3
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from io import BytesIO
import datetime


@require_http_methods(["GET", "POST"])
def export_expenses_to_exceldate(request):
    db_path = 'db.sqlite3'
    queries = {
        "Vendor": "SELECT id, name, contact_info, contact_number FROM expenses_vendor",
        "Employee": "SELECT id, name, position, salary_type, salary_amount, advance_payment FROM expenses_employee",
        "Purchase": """
            SELECT p.id, v.name AS vendor_name, p.item, p.amount, p.date
            FROM expenses_purchase p
            JOIN expenses_vendor v ON p.vendor_id = v.id
            WHERE p.date BETWEEN ? AND ?
        """,
        "SalaryPayment": """
            SELECT sp.id, e.name AS employee_name, sp.amount, sp.paid_from, sp.paid_to,  sp.date
            FROM expenses_salarypayment sp
            JOIN expenses_employee e ON sp.employee_id = e.id
            WHERE sp.date BETWEEN ? AND ?
        """,
        "ElectricityBill": "SELECT id, amount, due_date, paid_status, date_from, date_to FROM expenses_electricitybill WHERE date_from BETWEEN ? AND ?",
        "RentPayment": "SELECT id, amount, date_from, date_to, paid_status FROM expenses_rentpayment WHERE date_from BETWEEN ? AND ?",
        "MarketingExpense": "SELECT id, description, amount, date FROM expenses_marketingexpense WHERE date BETWEEN ? AND ?",
        "EquipmentExpense": "SELECT id, description, amount, date FROM expenses_equipmentexpense WHERE date BETWEEN ? AND ?"
    }

    # Default date range
    start_date = request.POST.get('start_date', '2000-01-01')
    end_date = request.POST.get('end_date', datetime.date.today().strftime('%Y-%m-%d'))

    data = {}
    conn = sqlite3.connect(db_path)
    for sheet_name, query in queries.items():
        if '?' in query:
            df = pd.read_sql_query(query, conn, params=[start_date, end_date])
        else:
            df = pd.read_sql_query(query, conn)

        if 'amount' in df.columns:
            total_row = pd.DataFrame(df[['amount']].sum()).T
            total_row.insert(0, 'id', 'Total')
            df = pd.concat([df, total_row], ignore_index=True)

        data[sheet_name] = df
    conn.close()

    # Create a Pandas Excel writer using BytesIO as the buffer
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Set the response to download the file
    response = HttpResponse(output.getvalue(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=expenses_report_{start_date}_to_{end_date}.xlsx'
    return response

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('expenses:expense_list')
        else:
            return HttpResponse("Invalid login details")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('expenses:expense_list')
