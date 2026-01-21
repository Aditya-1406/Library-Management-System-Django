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