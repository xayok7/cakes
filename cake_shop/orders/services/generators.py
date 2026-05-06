from abc import ABC, abstractmethod

class DocumentTemplate(ABC):
    
    def generate(self, order) -> str:
        return f"{self.build_header(order)}\n{self.build_body(order)}\n{self.build_footer()}"

    def build_header(self, order) -> str:
        return f"=== ДОКУМЕНТ ЗАКАЗА #{order.id} ==="

    @abstractmethod
    def build_body(self, order) -> str:
        pass

    def build_footer(self) -> str:
        return "==========================="


class ClientReceipt(DocumentTemplate):
# чек клиента
    def build_body(self, order) -> str:
        cake = order.cake
        return (f"Ваш торт: {cake.get_shape_display()}, {cake.get_size_display()}\n"
                f"Итого к оплате: {cake.total_price} руб.\n"
                f"Доставка: {order.get_delivery_type_display()}")


class KitchenTicket(DocumentTemplate):
# заказ для кухни
    def build_body(self, order) -> str:
        cake = order.cake
        decorations = ", ".join([d.name for d in cake.decorations.all()]) or "Без декора"
        return (f"Основа: {cake.base.name if cake.base else 'Нет'}\n"
                f"Начинка: {cake.filling.name if cake.filling else 'Нет'}\n"
                f"Декор: {decorations}")