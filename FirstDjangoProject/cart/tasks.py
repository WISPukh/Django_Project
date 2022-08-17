from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from main.models import Order


@shared_task
def order_created(order_id):
    order = Order.objects.get(pk=order_id)
    subject = f'Order № {order_id}'
    message = f"Your order content is:\n" \
              f"Price: {order.total_price}\n" \
              f"Total quantity: {order.quantity}"
    mail_sent = send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [order.customer_id.email]
    )

    return mail_sent
