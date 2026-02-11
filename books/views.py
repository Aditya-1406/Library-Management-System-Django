from django.shortcuts import render, redirect,get_object_or_404
from .models import Book
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction 
# Create your views here.

def list_book(request):

    # Optimized query (joins author in single query)
    books_qs = Book.objects.select_related('author').all()

    # Pagination (12 books per page)
    paginator = Paginator(books_qs, 12)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    return render(request, 'list_book.html', {"books": books})

@login_required(login_url='login')
def all_books(request):
    books = Book.objects.select_related('author').all()

    if request.method == 'POST':
        search = request.POST.get('search','')
        books = books.filter(title__icontains=search) | books.filter(author__name__icontains=search)

        if books.count()==0:
            books = Book.objects.select_related('author').all()
            messages.error(request, 'No books found matching your search')
            redirect('books')


    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    return render(request, 'all_books.html', {"books": books})


@login_required(login_url='login')
def borrow_book(request, book_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to borrow a book.")
        return redirect('login')  # change to your login URL

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
    transaction.save()
    messages.success(request, f"You successfully borrowed '{book.title}'!")
    return redirect('books')