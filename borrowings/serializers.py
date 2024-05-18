import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction

from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        Borrowing.validate_dates(
            datetime.date.today(),
            data["expected_return_date"],
            data["actual_return_date"],
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


class BorrowingCreateSerializer(BorrowingSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]
            Borrowing.validate_inventory(
                validated_data["book"],
                ValidationError
            )
            book.inventory -= 1
            book.save()
            return Borrowing.objects.create(**validated_data)

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date",
                  "actual_return_date", "book")
