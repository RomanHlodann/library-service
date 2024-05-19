from celery import shared_task

from borrowings.telegram_actions import send_notification


@shared_task
def send_notification_of_borrow_creation_telegram_bot(message: str):
    send_notification(message)
