from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "hard"
        SOFT = "soft"

    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    cover = models.CharField(
        max_length=10, choices=CoverChoices
    )
    inventory = models.IntegerField(
        validators=(MinValueValidator(0),)
    )
    daily_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=(MinValueValidator(0),)
    )

    def __str__(self) -> str:
        return self.title
