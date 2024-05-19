from django.db.models.signals import post_save
from django.dispatch import receiver
from borrowings.models import Borrowing
from borrowings.tasks import send_notification_of_borrow_creation_telegram_bot


@receiver(post_save, sender=Borrowing)
def notify_borrowing_created(sender, instance, created, **kwargs):
    if created:
        send_notification_of_borrow_creation_telegram_bot.delay(
            f"Created borrowing:\n"
            f"id: {instance.id}\n"
            f"Borrow date: {instance.borrow_date}\n"
            f"Expected return date {instance.expected_return_date}"
            f"Book: {instance.book.title}\n"
            f"New book inventory: {instance.book.inventory}\n"
            f"By {instance.user.email}"
        )
