from django.shortcuts import render,redirect
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def transaction_view(request):
    member = request.user.member
    transactions = Transaction.objects.filter(member=member).select_related('book')

    if request.method == 'POST':
        search = request.POST.get('search','')
        transactions = transactions.filter(book__title__icontains=search) | transactions.filter(id=search)

        if transactions.count()==0:
            messages.error(request, 'No Records found')
            redirect('books')


    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    return render(request, 'transaction.html', {"transactions": transactions})
