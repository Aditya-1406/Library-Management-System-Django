from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Member
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def signup(request):
    if request.method == 'POST':
        data = request.POST

        first_name = data.get('first_name')
        username = data.get('username')
        email = data.get('email')
        contact = data.get('contact')
        password = data.get('password')

        
        if (len(password) < 8) or (not any(char.isdigit() for char in password)) or (not any(char.isalpha() for char in password)):
            messages.error(request, 'Password must be at least 8 characters long and contain both letters and numbers.')
            return redirect('signup')

        user = User.objects.filter(email=email)
        if user.exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')
        
        user = User.objects.create(
            first_name= first_name,
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        member = Member.objects.create(
            user = user,
            contact = contact
        )

        member.save()
        messages.success(request,'User Created Successfully')
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')


        try:
            # Find the user by email, then authenticate with their username
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

        user = authenticate(request, username=u.username, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

        login(request, user)

        # Optional role check
        try:
            role = user.member.role
        except Member.DoesNotExist:
            role = 'member'

        if role == 'superuser' and user.is_staff:
            return redirect('admin:index')

        messages.success(request, 'Login successful.')
        return redirect('login')


    return render(request,'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')