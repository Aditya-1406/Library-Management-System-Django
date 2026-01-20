from django.shortcuts import render,redirect
from .models import Member
from django.contrib import messages
from .decorators import login_required_custom,admin_required
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

@login_required_custom
def logout(request):
    request.session.flush()
    return redirect('login')

@login_required_custom
def update(request):
    mem_id = request.session.get("member_id")

    try:
        mem = Member.objects.get(id=mem_id)
    except Exception as e:
        return redirect('login')
    
    if request.method == 'POST':
            data = request.POST

            name = data.get('name')
            contact = data.get('contact')
            email = data.get('email')

            mem.name = name
            mem.contact = contact 
            mem.email = email
            mem.save()
            messages.success(request,"Profile Updated Successfully")
            return redirect('login')
        
    return render(request,'update.html',{'mem':mem})
    
@admin_required
def delete(request):


   role = request.session.get('role')
   if role != 'admin':
       messages.error(request,"Only admin can access this feature")
       return redirect('login')
   if request.method == 'POST':
        data = request.POST
        user_id = data.get('name')
        email = data.get('email')

        if user_id:
            try:
                user = Member.objects.get(id=user_id)
                user.delete()
                messages.success(request,"User Deleted Successfully")
                return redirect('login')
            except Member.DoesNotExist:
                messages.error(request,"User with this ID does not exits")
                return redirect('login')

        elif email:
            try:
                user = Member.objects.get(email=email)
                user.delete()
                messages.success(request,"User Deleted Successfully")
                return redirect('login')
            except Member.DoesNotExist:
                messages.error(request,"User with this ID does not exits")
                return redirect('login')    

   

   return render(request,'delete.html')
   
@admin_required
def alluser(request):
    if request.session.get('role') != 'admin':
        messages.error(request, "Only admin can access this feature")
        return redirect('login')

    users = Member.objects.all().order_by('role')

    if request.method == 'POST':
        search = request.POST.get('search', '').strip()

        if search:
            users = Member.objects.filter(
                email__icontains=search
            ) | Member.objects.filter(
                name__icontains=search
            )

            if not users.exists():
                messages.error(request, "User does not exist")

    return render(request, 'alluser.html', {'users': users})

def updaterole(request,id):
    if request.session.get('role')!= 'admin':
        messages.error(request,"Only admin can access this feature")
        return redirect('login')
    
    try:
        mem= Member.objects.get(id=id)
    except Member.DoesNotExist:
        messages.error(request,"User does not exists")
        return redirect('alluser')
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        contact = data.get('contact')
        role = data.get('role')
        mem.role = role
        mem.name = name
        mem.contact = contact
        mem.save()
        request.session.role = role
        request.session.name = name 

        messages.success(request,"User Role Updated Successfully")
        return redirect('alluser')
    return render(request,'updaterole.html',{'mem':mem})