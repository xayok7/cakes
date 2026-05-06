import os
import datetime
from abc import ABC, abstractmethod
from django.core.mail import send_mail
from django.conf import settings

class Observer(ABC):
    @abstractmethod
    def update(self, order):
        pass

class OrderNotifier:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def notify(self, order):
        for obs in self._observers:
            obs.update(order)

class EmailNotificationObserver(Observer):
    def update(self, order):
        subject = f"Обновление по заказу #{order.id}"
        message = (
            f"Здравствуйте, {order.user.username}!\n"
            f"Статус вашего заказа изменился на: {order.get_status_display()}.\n"
            f"Сумма заказа: {order.cake.total_price} руб."
        )
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@cakeshop.com',
            recipient_list=[order.user.email] if order.user.email else ['admin@cakeshop.com'],
            fail_silently=True,
        )



class ExternalAnalyticsModule:
    def log_business_event(self, event_type: str, payload: dict, timestamp: str):
        # лог
        log_file_path = os.path.join(settings.BASE_DIR, 'analytics_report.log')
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {event_type.upper()} | DATA: {payload}\n")


class AnalyticsAdapter(Observer):
    # преобразует update
    def __init__(self, analytics_system: ExternalAnalyticsModule):
        self.analytics = analytics_system

    def update(self, order):
        #формат
        payload = {
            "order_id": order.id,
            "user": order.user.username,
            "new_status": order.status,
            "price": float(order.cake.total_price)
        }
        timestamp = datetime.datetime.now().isoformat()
        
        self.analytics.log_business_event("order_status_changed", payload, timestamp)

# инициализация
notifier = OrderNotifier()
notifier.attach(EmailNotificationObserver())
notifier.attach(AnalyticsAdapter(ExternalAnalyticsModule()))