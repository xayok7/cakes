from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')


class Base(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Cream(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Filling(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Decoration(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Cake(models.Model):
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )

    SHAPE_CHOICES = (
        ('round', 'Round'),
        ('square', 'Square'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    base = models.ForeignKey(Base, on_delete=models.SET_NULL, null=True)
    cream = models.ForeignKey(Cream, on_delete=models.SET_NULL, null=True)
    filling = models.ForeignKey(Filling, on_delete=models.SET_NULL, null=True)
    decorations = models.ManyToManyField(Decoration, blank=True)

    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    shape = models.CharField(max_length=10, choices=SHAPE_CHOICES)

    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_price(self):
        price = 0

        if self.base:
            price += self.base.price
        if self.cream:
            price += self.cream.price
        if self.filling:
            price += self.filling.price

        for d in self.decorations.all():
            price += d.price

        # коэффициент размера
        if self.size == 'M':
            price *= Decimal('1.2')
        elif self.size == 'L':
            price *= Decimal('1.5')

        return round(price, 2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала сохраняем, чтобы был id

        self.total_price = self.calculate_price()
        super().save(update_fields=['total_price'])

    def __str__(self):
        return f"Cake #{self.id} - {self.user.username}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('processing', 'Processing'),
        ('baking', 'Baking'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    )

    DELIVERY_CHOICES = (
    ('delivery', 'Доставка'),
    ('pickup', 'Самовывоз'),
    )



    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cake = models.OneToOneField(Cake, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    delivery_type = models.CharField(
        max_length=10,
        choices=DELIVERY_CHOICES,
        default='delivery'
    )
    
    def __str__(self):
        return f"Order #{self.id} - {self.status}"
    
    def next_status(self):
        order_flow = ['new', 'processing', 'baking', 'ready', 'delivered']
        try:
            current_index = order_flow.index(self.status)
            self.status = order_flow[current_index + 1]
            self.save()
        except (ValueError, IndexError):
            pass


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.status}"
