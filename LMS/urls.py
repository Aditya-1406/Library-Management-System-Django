"""
URL configuration for LMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from member.views import Signup,LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static
from books.views import ListBook,AllBook,BorrowBook
from transaction.views import TransactionView
from transaction.admin_dashboard import DashboardView
from transaction.trans import  Checkout


urlpatterns = [
    path('',ListBook.as_view(),name='home'),
    path('admin/dashboard/',DashboardView.as_view(),name='admin_dashboard'),
    path('books/',AllBook.as_view(),name='books'),
    path('transactions/',TransactionView.as_view(),name='transactions'),
    path('borrow/<int:book_id>/',BorrowBook.as_view(), name='borrow_book'),
    path('admin/', admin.site.urls),
    path('signup/', Signup.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('checkout/<int:trans_id>/',Checkout.as_view(),name='pay'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

