from abc import ABC, abstractmethod


class OrderProcessor(ABC):

    def process_order(self):
        steps = []

        steps.append(self.validate_order())
        steps.append(self.prepare_cake())
        steps.append(self.process_payment())
        steps.append(self.finish_order())

        return steps

    def validate_order(self):
        return "Проверка заказа"

    @abstractmethod
    def prepare_cake(self):
        pass

    @abstractmethod
    def process_payment(self):
        pass

    def finish_order(self):
        return "Заказ завершен"
    
class DeliveryOrderProcessor(OrderProcessor):

    def prepare_cake(self):
        return "Торт подготовлен для доставки"

    def process_payment(self):
        return "Онлайн оплата выполнена"
    
class PickupOrderProcessor(OrderProcessor):

    def prepare_cake(self):
        return "Торт подготовлен для самовывоза"

    def process_payment(self):
        return "Оплата при получении"