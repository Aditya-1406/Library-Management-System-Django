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
from member.views import signup,login,logout,update,delete,alluser,updaterole
from django.conf import settings
from django.conf.urls.static import static
from book.views import add_book

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',signup,name='signup'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('update/',update,name='update'),
    path('delete/',delete,name='delete'),
    path('alluser/',alluser,name='alluser'),
    path('updaterole/<int:id>/',updaterole,name='updaterole'),
    path('addbook/',add_book,name='addbook')
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)