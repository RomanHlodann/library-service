from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        Borrowing.validate_dates(
            attrs["borrow_date"],
            attrs["expected_return_date"],
            attrs["actual_return_date"],
            ValidationError
        )
        return data

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date",
                  "actual_return_date", "book", "user")


class BorrowingListSerializer(BorrowingSerializer):
    book_title = serializers.CharField(source="book.title")

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date",
                  "actual_return_date", "book_title", "user")


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer()
