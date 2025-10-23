from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import ExpenseForm
from .models import expense
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

import csv
from django.http import HttpResponse


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    expenses = expense.objects.filter(user=request.user).order_by('-date')


    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

  
    current_month = now().month
    monthly_total = expenses.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

  
    return render(request, 'expenses/home.html', {
        'expenses': expenses,
        'total': total,
        'monthly_total': monthly_total
    })



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
