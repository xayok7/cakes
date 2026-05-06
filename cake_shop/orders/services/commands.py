from abc import ABC, abstractmethod
from .observers import notifier


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class PayOrderCommand(Command):
    def __init__(self, payment, order):
        self.payment = payment
        self.order = order

    def execute(self):
        # статус меняется
        self.payment.status = 'paid'
        self.payment.save()
        self.order.status = 'processing'
        self.order.save()
        
        #наблюдатель
        notifier.notify(self.order)

class AdvanceOrderStatusCommand(Command):
    def __init__(self, order):
        self.order = order

    def execute(self):
        self.order.next_status()
        notifier.notify(self.order)

class OrderInvoker:
    def execute_command(self, command: Command):
        command.execute()