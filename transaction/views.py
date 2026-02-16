from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Transaction
from django.db.models import Q


class TransactionView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        member = request.user.member

        transactions = Transaction.objects.filter(
            member=member
        ).select_related('book')

        # Pagination
        paginator = Paginator(transactions, 10)
        page_number = request.GET.get('page')
        transactions = paginator.get_page(page_number)

        return render(request, 'transaction.html', {
            "transactions": transactions
        })

    def post(self, request):
        member = request.user.member

        transactions = Transaction.objects.filter(
            member=member
        ).select_related('book')

        search = request.POST.get('search', '')

        if search:
            transactions = transactions.filter(
                Q(book__title__icontains=search)
            | Q(id=search))

        if transactions.count() == 0:
            messages.error(request, 'No Records found')
            return redirect('transactions')  

        # Pagination after search
        paginator = Paginator(transactions, 10)
        page_number = request.GET.get('page')
        transactions = paginator.get_page(page_number)

        return render(request, 'transaction.html', {
            "transactions": transactions
        })
