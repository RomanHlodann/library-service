from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book


def sample_book():
    return {
        "title": "Test",
        "author": "Test",
        "cover": "soft",
        "inventory": 0,
        "daily_fee": 2.49
    }


def book_list_url():
    return reverse("library:book-list")


class BookModelTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_cover_choices(self):
        cover_field = Book._meta.get_field("cover")
        cover_choices = cover_field.choices

        expected_choices = [
            ("hard", "Hard"),
            ("soft", "Soft")
        ]

        self.assertEqual(cover_choices, expected_choices)

    def test_title_uniqueness(self):
        book = sample_book()
        self.client.post(book_list_url(), data=book)
        res = self.client.post(book_list_url(), data=book)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_post_book_negative_inventory(self):
        book = sample_book()
        book["inventory"] = -1
        res = self.client.post(book_list_url(), data=book)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

    def test_post_book_negative_fee(self):
        book = sample_book()
        book["daily_fee"] = -1.49
        res = self.client.post(book_list_url(), data=book)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)


class BookViewUnauthorizedTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_access_to_book_list(self):
        res = self.client.get(book_list_url())
        self.assertEqual(status.HTTP_200_OK, res.status_code)

    def test_post_book(self):
        book = sample_book()
        res = self.client.post(book_list_url(), data=book)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, res.status_code)


class BookViewAuthorizedTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_post_book(self):
        book = sample_book()
        res = self.client.post(post_book_url(), data=book)
        self.assertEqual(status.HTTP_403_FORBIDDEN, res.status_code)


class BookViewAdminTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_post_book(self):
        book = sample_book()
        res = self.client.post(post_book_url(), data=book)
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
