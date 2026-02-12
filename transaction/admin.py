from django.contrib import admin
from .models import Transaction
# Register your models here.
from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json





class TransAdmin(admin.ModelAdmin):
    list_display = ("id", "member", "book", "borrowed_at", "due_date","returned_at","fine_amount","fine_paid")
    list_filter = ("due_date", "fine_amount")
    search_fields = ("id","member__user__username", "book__title", "borrowed_at")
    ordering = ("-id",)


admin.site.register(Transaction,TransAdmin)