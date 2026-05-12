from decimal import Decimal


class PiePriceStrategy:

    def calculate(self, pie):
        raise NotImplementedError


class SimplePieStrategy(PiePriceStrategy):

    def calculate(self, pie):
        # база от типа пирога
        if pie.name == 'apple':
            base = Decimal('10')
        elif pie.name == 'cherry':
            base = Decimal('12')
        else:
            base = Decimal('15')

        # коэффициент размера
        if pie.size == 'M':
            base *= Decimal('1.2')
        elif pie.size == 'L':
            base *= Decimal('1.5')

        # тесто влияет на цену
        if pie.dough == 'puff':
            base += Decimal('3')
        elif pie.dough == 'sweet':
            base += Decimal('2')

        return base