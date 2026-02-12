from django.db import models
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings


def get_default_due_date():
    return timezone.now() + timedelta(days=14)


class Transaction(models.Model):
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)

    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=get_default_due_date)
    returned_at = models.DateTimeField(null=True, blank=True)

    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"))
    fine_paid = models.BooleanField(default=False)

    def calculate_fine(self):
        """Calculate fine even if book not returned yet"""
        end_date = self.returned_at or timezone.now()

        if end_date > self.due_date:
            days_overdue = (end_date.date() - self.due_date.date()).days
            fine_per_day = Decimal("10.00")
            return Decimal(days_overdue) * fine_per_day

        return Decimal("0.00")

    def save(self, *args, **kwargs):
        with transaction.atomic():

            # get old returned_at value (before update)
            old_returned_at = None
            if self.pk:
                old_returned_at = Transaction.objects.get(pk=self.pk).returned_at

            # 🔻 BORROW LOGIC (when transaction is created)
            is_new = self.pk is None
            if is_new:
                if self.book.available_copies <= 0:
                    raise ValueError("No copies available for this book.")
                self.book.available_copies -= 1
                self.book.save()

            # 🔺 RETURN LOGIC (when admin sets returned_at)
            is_returned_now = False
            if old_returned_at is None and self.returned_at is not None:
                self.book.available_copies += 1
                self.book.save()
                is_returned_now = True

            # update fine
            self.fine_amount = self.calculate_fine()

            super().save(*args, **kwargs)

            # ✅ EMAIL WHEN BOOK IS ISSUED
            if is_new:
                subject = "📚 Book Issued - Library Notification"
                due_date_str = self.due_date.strftime("%d %b %Y")

                message = f"""
Hi {self.member.user.username},

Your book has been successfully issued 🎉

📖 Book Name: {self.book.title}
📅 Due Date: {due_date_str}

⚠️ Fine Warning:
A fine of ₹10 per day will be charged if the book is returned late.

Please return the book on time.

Library Management System 📚
                """

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [self.member.user.email],
                    fail_silently=False,
                )

            # ✅ EMAIL WHEN BOOK IS RETURNED
            if is_returned_now:
                subject = "✅ Book Returned - Library Notification"
                fine = self.fine_amount

                message = f"""
Hi {self.member.user.username},

Your book has been successfully returned ✅

📖 Book Name: {self.book.title}
💰 Fine Amount: ₹{fine}

"""

                if fine > 0:
                    message += f"""
⚠️ You have been charged a fine of ₹{fine}.
Please pay the fine to the library.
"""
                else:
                    message += """
🎉 No fine charged! Thank you for returning the book on time.
"""

                message += """

Library Management System 📚
                """

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [self.member.user.email],
                    fail_silently=False,
                )

    def __str__(self):
        return f"{self.member.user.username} borrowed {self.book.title}"

    class Meta:
        ordering = ("-id",)
        indexes = [
            models.Index(fields=["-id"]),
        ]
