class PricingProxy:

    def __init__(self, strategy):
        self.strategy = strategy

    def calculate(self, obj):
        print("Proxy: расчет цены")  # можно убрать потом
        return self.strategy.calculate(obj)