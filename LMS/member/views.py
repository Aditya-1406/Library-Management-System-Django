from django.shortcuts import render,redirect
from .models import Member
from django.contrib import messages
# Create your views here.


def signup(request):
    
    if request.method == "POST":
        data = request.POST

        name = data.get('name')
        contact = data.get('contact')
        email = data.get('email')
        password = data.get('password')

        user = Member.objects.filter(email = email)
        if user.exists():
            messages.warning(request,"User with this mail id already exists")
            return redirect('signup')
        
        user = Member.objects.create(
            name = name,
            contact = contact,
            email = email,
        )

        user.set_password(password)
        user.save()
        messages.success(request,"Signup Successful 😊")
        return redirect('login')

    return render(request,'Signup.html')

def login(request):

    if request.method == "POST":
        data = request.POST
        email = data.get('email')
        password = data.get('password')

        
        try:
            user = Member.objects.get(email=email)
        except Member.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")
        
        if user.verify_password(password):
            request.session["member_id"] = user.id
            request.session["role"] = user.role
            request.session["name"] = user.name
            messages.success(request, "Login successful!")
            return redirect("login")

        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")


    
    return render(request,'login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

