from ..models import Payment, Pie
from .commands import PayOrderCommand, OrderInvoker
from .observers import notifier, email_observer
from .generators import ClientReceipt, KitchenTicket
from .order_processing import DeliveryOrderProcessor, PickupOrderProcessor
from ..factories import get_factory
from .decorators import CandlesDecorator, TextDecorator, ExpressDecorator


from .pricing import SimplePieStrategy
from .proxy import PricingProxy


class OrderManagementFacade:
    def __init__(self):
        self.invoker = OrderInvoker()


    def create_and_calculate_cake(self, user, validated_data, decorations, extras: dict):
        cake_type = validated_data.get('cake_type', 'standard')
        factory = get_factory(cake_type)
        cake = factory.create(user, validated_data, decorations)

        cake.total_price = cake.calculate_price()

        decorated = cake
        if extras.get('candles'):
            decorated = CandlesDecorator(decorated)
        if extras.get('text'):
            decorated = TextDecorator(decorated)
        if extras.get('express'):
            decorated = ExpressDecorator(decorated)

        cake.total_price = decorated.get_price()
        cake.save()
        return cake

    def create_and_calculate_pie(self, name, size, dough):
        pie = Pie.objects.create(name=name, size=size, dough=dough)
        
        strategy = SimplePieStrategy()
        proxy = PricingProxy(strategy)
        
        pie.total_price = proxy.calculate(pie)
        pie.save()
        return pie

    def process_order_delivery(self, order):
        if order.delivery_type == 'delivery':
            processor = DeliveryOrderProcessor()
        else:
            processor = PickupOrderProcessor()
        return processor.process_order()

    def process_payment(self, order, send_email: bool):
        if send_email:
            notifier.attach(email_observer)
        else:
            notifier.detach(email_observer)

        payment, _ = Payment.objects.get_or_create(
            order=order, defaults={'amount': order.cake.total_price}
        )
        command = PayOrderCommand(payment, order)
        self.invoker.execute_command(command)

    def get_order_documents(self, order):
        receipt = ClientReceipt().generate(order)
        ticket = KitchenTicket().generate(order)
        return receipt, ticket
