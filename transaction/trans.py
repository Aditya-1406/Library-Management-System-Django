from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Transaction
from django.db.models import Q




class Checkout(View):

    def get(self,request,*args,**kwargs):
        trans_id = kwargs.get('trans_id')
        trans = get_object_or_404(Transaction, pk=trans_id)
        return render(request,"checkout.html",{"trans":trans})