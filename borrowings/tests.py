import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from books.models import Book
from books.serializers import BookSerializer
from books.tests import sample_book
from borrowings.models import Borrowing


def sample_borrowing():
    borrow_date = datetime.date.today()
    return {
        "borrow_date": str(borrow_date),
        "expected_return_date": str(
            borrow_date + datetime.timedelta(days=2)
        ),
        "actual_return_date": "",
        "book": 1,
        "user": 1
    }


def get_borrowing_list_url():
    return reverse("borrowings:borrowing-list")


class BorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        book_data = sample_book()
        book_data["inventory"] = 0
        book_data["title"] = "Inventory Is Empty"
        book = BookSerializer(data=book_data)
        book.is_valid()
        book.save()

        book_data["inventory"] = 2
        book_data["title"] = "Inventory Not Empty"
        book = BookSerializer(data=book_data)
        book.is_valid()
        book.save()

    def test_post_borrow_date_greater_than_actual_or_expected(self):
        borrowing = sample_borrowing()
        borrowing["expected_return_date"] = "2024-04-04"
        res = self.client.post(
            get_borrowing_list_url(), data=borrowing
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_post_borrow_with_book_inventory_0(self):
        borrowing = sample_borrowing()
        borrowing["book"] = Book.objects.get(title="Inventory Is Empty").id
        res = self.client.post(
            get_borrowing_list_url(), data=borrowing
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_book_inventory_when_borrowing_created(self):
        borrowing = sample_borrowing()
        book = Book.objects.get(
            title="Inventory Not Empty"
        )
        borrowing["book"] = book.id
        res = self.client.post(
            get_borrowing_list_url(), data=borrowing
        )
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(1, Book.objects.get(id=book.id).inventory)

    def test_post_borrowing_user(self):
        borrowing = sample_borrowing()
        borrowing["book"] = Book.objects.get(title="Inventory Not Empty").id
        res = self.client.post(
            get_borrowing_list_url(), data=borrowing
        )
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(
            self.user.id,
            Borrowing.objects.get(id=res.data["id"]).user_id
        )
