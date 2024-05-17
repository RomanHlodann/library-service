from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    @staticmethod
    def validate_dates(
            borrow_date,
            expected_return_date,
            actual_return_date,
            error_to_raise):
        if borrow_date < expected_return_date:
            raise error_to_raise(
                "Borrow date cannot be after expected"
                f"{borrow_date} < {expected_return_date}"
            )
        if actual_return_date and borrow_date < actual_return_date:
            raise error_to_raise(
                "Borrow date cannot be after actual"
                f"{borrow_date} < {actual_return_date}"
            )

    def clean(self):
        Borrowing.validate_dates(
            self.borrow_date,
            self.expected_return_date,
            self.actual_return_date,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return f"{self.book} at {self.borrow_date}"