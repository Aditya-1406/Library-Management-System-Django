from django.shortcuts import render, redirect,get_object_or_404
from .models import Book
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction 
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
# Create your views here.

class ListBook(View):

    # Optimized query (joins author in single query)
    def get(self,request):
        books_qs = Book.objects.select_related('author').all()

        # Pagination (12 books per page)
        paginator = Paginator(books_qs, 12)
        page_number = request.GET.get('page')
        books = paginator.get_page(page_number)

        return render(request, 'list_book.html', {"books": books})

class AllBook(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        books_qs = Book.objects.select_related('author').all()

        paginator = Paginator(books_qs, 12)
        page_number = request.GET.get('page')
        books = paginator.get_page(page_number)

        return render(request, 'all_books.html', {"books": books})

    def post(self, request):
        search = request.POST.get('search', '')

        books_qs = Book.objects.select_related('author').filter(
            Q(title__icontains=search) |
            Q(author__name__icontains=search)
        )

        if not books_qs.exists():
            messages.error(request, 'No books found matching your search')
            return redirect('books')

        paginator = Paginator(books_qs, 12)
        page_number = request.GET.get('page')
        books = paginator.get_page(page_number)

        return render(request, 'all_books.html', {"books": books})    


class BorrowBook(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self,request,*args, **kwargs):
        book_id = kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        # Check if copies available
        if book.available_copies <= 0:
            messages.error(request, "No copies available for this book.")
            return redirect('books')

        # Get member object
        member = request.user.member  # assuming OneToOne relation

        # Prevent duplicate borrowing (optional but recommended)
        already_borrowed = Transaction.objects.filter(
            member=member,
            book=book,
            returned_at__isnull=True
        ).exists()

        if already_borrowed:
            messages.warning(request, "You already borrowed this book.")
            return redirect('books')

        # Create transaction
        transaction = Transaction.objects.create(
            member=member,
            book=book
        )
        messages.success(request, f"You successfully borrowed '{book.title}'!")
        return redirect('books')