from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
import json

from member.models import Member
from books.models import Book
from .models import Transaction


@method_decorator(staff_member_required, name='dispatch')
class DashboardView(View):

    def get(self, request):
        total_members = Member.objects.count()
        total_books = Book.objects.count()
        issued_books = Transaction.objects.filter(returned_at__isnull=True).count()
        returned_books = Transaction.objects.filter(returned_at__isnull=False).count()

        # 📊 Monthly transactions
        trans = Transaction.objects.annotate(
            month=TruncMonth('borrowed_at')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')

        labels = []
        trans_data = []
        fine_data = []

        for t in trans:
            labels.append(t['month'].strftime("%b %Y"))
            trans_data.append(t['count'])

            # total fine per month
            fine_sum = Transaction.objects.filter(
                borrowed_at__month=t['month'].month,
                borrowed_at__year=t['month'].year
            ).aggregate(total=Sum('fine_amount'))['total'] or 0

            fine_data.append(float(fine_sum))

        context = {
            'total_members': total_members,
            'total_books': total_books,
            'issued_books': issued_books,
            'returned_books': returned_books,

            'labels': json.dumps(labels),
            'trans_data': json.dumps(trans_data),
            'fine_data': json.dumps(fine_data),
            'status_data': json.dumps([issued_books, returned_books]),
        }

        return render(request, "admin/dashboard.html", context)
