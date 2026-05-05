from decimal import Decimal


class PriceStrategy:

    def calculate(self, cake):
        raise NotImplementedError


class StandardPriceStrategy(PriceStrategy):

    def calculate(self, cake):
        return cake.calculate_price()


class DiscountPriceStrategy(PriceStrategy):

    def calculate(self, cake):
        return cake.calculate_price() * Decimal('0.9')


class VipPriceStrategy(PriceStrategy):

    def calculate(self, cake):
        return cake.calculate_price() * Decimal('0.8')