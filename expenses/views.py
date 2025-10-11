from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import ExpenseForm
from .models import expense
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

import csv
from django.http import HttpResponse


# Create your views here.

# login_required
def home(request):
    # Redirect to login if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Replace 'login' with your login URL name

    # Get all expenses for the logged-in user
    expenses = expense.objects.filter(user=request.user).order_by('-date')

    # Calculate total amount spent
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Total spent in the current month
    current_month = now().month
    monthly_total = expenses.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

    # Render the home page with all values
    return render(request, 'expenses/home.html', {
        'expenses': expenses,
        'total': total,
        'monthly_total': monthly_total
    })

# def home(request):
#     # ORM
#     expenses= Expense.objects.filter(user=request.user).order_by('-date')
#     return render(request, 'expenses/home.html', {'expenses':expenses})


#      # Calculate total amount spent
#     total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

#     # Total spent in current month
#     current_month = now().month
#     monthly_total = expenses.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

#     return render(request, 'expenses/home.html', {
#         'expenses': expenses,
#         'total': total,
#         'monthly_total': monthly_total
#     })
#Login  required

# def add_expense(request):
#     if request.method== 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             expense = form.save(commit=False)
#             expense.user = request.user

#             expense.save()
#             return redirect('home')
        
#     else:
#         form= ExpenseForm()
#     return render(request,'expenses/add_expense.html' ,{'form':form} )

def add_expense(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        description = request.POST.get('description')
        date = request.POST.get('date')
        expense.objects.create(
            
            user=request.user,
            amount=amount,
            category=category,
            description=description,
            date=date
        )
        return redirect('home')
    return render(request, 'expenses/add_expense.html')

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=expenses.csv'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Amount', 'Description'])

    expenses = expense.objects.filter(user=request.user)
    for exp in expenses:
        writer.writerow([exp.date, exp.category, exp.amount, exp.description])

    return response