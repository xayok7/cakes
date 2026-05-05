from decimal import Decimal


class CakeDecorator:
    def __init__(self, cake):
        self.cake = cake

    def get_price(self):
        # 👇 ВАЖНО: вызываем метод, а не поле
        if hasattr(self.cake, 'get_price'):
            return self.cake.get_price()
        return self.cake.total_price


class CandlesDecorator(CakeDecorator):
    def get_price(self):
        return super().get_price() + Decimal('3')


class TextDecorator(CakeDecorator):
    def get_price(self):
        return super().get_price() + Decimal('5')


class ExpressDecorator(CakeDecorator):
    def get_price(self):
        return super().get_price() * Decimal('1.2')