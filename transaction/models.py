from django.db import models
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
from django.db import transaction


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
        # Atomic transaction to avoid race condition
        with transaction.atomic():
            if not self.pk:  # new transaction
                # Lock book row for update (prevents negative copies)
                book = type(self.book).objects.select_for_update().get(pk=self.book.pk)

                if book.available_copies <= 0:
                    raise ValueError("No copies available for this book.")

                book.available_copies -= 1
                book.save()
                self.book = book

            self.fine_amount = self.calculate_fine()
            super().save(*args, **kwargs)

    def return_book(self):
        if not self.returned_at:
            with transaction.atomic():
                self.returned_at = timezone.now()
                self.fine_amount = self.calculate_fine()

                book = type(self.book).objects.select_for_update().get(pk=self.book.pk)
                book.available_copies += 1
                book.save()

                super().save()

    def __str__(self):
        return f"{self.member.user.username} borrowed {self.book.title}"

    class Meta:
        ordering = ("-id",)
        indexes = [
            models.Index(fields=["-id"]),
        ]
