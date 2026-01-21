from django.shortcuts import render,redirect
from .models import Book
from django.contrib import messages

# Create your views here.

def add_book(request):

    if request.method == 'POST':
        data  = request.POST
        title = data.get('title')
        author = data.get('author').lower()
        isbn = data.get('isbn')
        published_date = data.get('published_date')
        available_copies = data.get('available_copies')
        photo = request.FILES.get('photo')
        category = data.get('category').lower()

        if Book.objects.filter(isbn=isbn).exists():
            messages.error(request,"Book with this ISBN already exists")
            return redirect('addbook')

        elif int(available_copies) <= 0:
            messages.error(request,"Book copies should be greater than 0")
            return redirect('addbook')
        
        book = Book.objects.create(
            title = title,
            author = author,
            isbn = isbn,
            published_date = published_date,
            available_copies = available_copies,
            photo = photo,
            category = category
        )
        book.save()

        messages.success(request,"Book added successfully")
        return redirect('addbook')

    return render(request,'add.html')


def update_book(request,id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found")
        return redirect("updatebook", id=id)

    if request.method == "POST":
        data = request.POST
        available_copies = data.get('available_copies')
        photo = request.FILES.get('photo')

        if int(available_copies) < 0:
            messages.error(request, "Available copies cannot be negative")
            return redirect("updatebook", id=id)

        book.available_copies = available_copies
        if photo:
            book.photo = photo
        book.save()

        messages.success(request, "Book updated successfully")
        return redirect("updatebook", id=id)

    return render(request, 'updatebook.html', {'book': book})


def allbook(request):
    if request.session.get('role') != 'admin':
        messages.error(request, "Only admin can access this feature")
        return redirect('login')

    books = Book.objects.all().order_by('title')

    if request.method == 'POST':
        search = request.POST.get('search', '').strip()

        if search:
            books = Book.objects.filter(
                title__icontains=search
            ) | Book.objects.filter(
                author__icontains=search
            )

            if not books.exists():
                messages.error(request, "User does not exist")

    return render(request, 'listbook.html', {'books': books})