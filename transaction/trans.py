from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Transaction
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
import re



class Checkout(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self,request,*args,**kwargs):
        trans_id = kwargs.get('trans_id')
        trans = get_object_or_404(Transaction, pk=trans_id)
        return render(request,"checkout.html",{"trans":trans})
    
   

    def post(self, request, *args, **kwargs):
        trans_id = kwargs.get('trans_id')
        trans = get_object_or_404(Transaction, pk=trans_id)

        # prevent double payment
        if trans.fine_paid:
            messages.info(request, "Fine already paid.")
            return redirect('transactions')

        card_name = request.POST.get('card_name', '').strip()
        card_number = request.POST.get('card_number', '').strip()
        expiration = request.POST.get('expiration', '').strip()
        cvv = request.POST.get('cvv', '').strip()


        # mask card number
        last4 = card_number[-4:]

        # mark fine paid
        trans.fine_paid = True
        trans.save()

        # ✅ Send email confirmation
        subject = "Library Fine Payment Confirmation"
        message = (
            f"Your fine payment was successful.\n\n"
            f"Loan ID: {trans.id}\n"
            f"Card Holder: {card_name}\n"
            f"Card Ending: **** **** **** {last4}\n\n"
            f"Thank you."
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [trans.member.user.email],  # sending to member email
            fail_silently=False,
        )

        messages.success(request, "Fine Paid Successfully")
        return redirect('transactions')


