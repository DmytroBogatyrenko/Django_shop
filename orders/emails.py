import logging

from django.conf import settings
from django.core.mail import BadHeaderError, EmailMultiAlternatives, mail_admins
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _send_order_email(order, subject, template_base):
    context = {'order': order, 'items': order.items.all()}

    text_content = render_to_string(f'{template_base}.txt', context)
    html_content = render_to_string(f'{template_base}.html', context)

    recipient = order.user.email if order.user else getattr(order, 'email', None)
    if not recipient:
        logger.warning('Для замовлення %s немає email — лист не надіслано', order.order_number)
        return False

    message = EmailMultiAlternatives(
        subject,
        text_content,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
        [recipient],
    )
    message.attach_alternative(html_content, 'text/html')

    try:
        message.send(fail_silently=False)
    except BadHeaderError:
        logger.error('Некоректний заголовок листа для замовлення %s', order.order_number)
        return False
    except Exception as e:
        logger.error('Помилка при надсиланні листа: %s', e)
        return False

    return True


def send_order_confirmation_email(order):
    subject = f'Замовлення #{order.order_number} підтверджено'
    return _send_order_email(order, subject, 'orders/emails/order_confirmation')


def send_payment_received_email(order):
    subject = f'Оплату за замовлення #{order.order_number} отримано'
    return _send_order_email(order, subject, 'orders/emails/payment_received')


def notify_admins_about_order(order):
    try:
        guest_email = getattr(order.shipping_address, 'email', None) if hasattr(order, 'shipping_address') else None
        user_info = f"{order.user.username} ({order.user.email})" if order.user else f"Гість ({guest_email})"
        mail_admins(
            subject=f'Нове замовлення {order.order_number}',
            message=(
                f'Користувач: {user_info}\n'
                f'Сума: {order.total_price} грн\n'
                f'Спосіб оплати: {order.get_payment_method_display()}\n'
                f'Позицій: {order.items.count()}\n'
            ),
            fail_silently=True,
        )
    except Exception as e:
        logger.error('Помилка надсилання сповіщення адмінам: %s', e)
