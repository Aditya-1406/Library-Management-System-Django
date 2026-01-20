from django.shortcuts import redirect
from django.contrib import messages

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("member_id"):
            messages.error(request, "Please login first")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("member_id"):
            messages.error(request, "Please login first")
            return redirect("login")
        if request.session.get("role") != "admin":
            messages.error(request, "Admin access required")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper
