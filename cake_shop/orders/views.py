from django.shortcuts import render, redirect
from .forms import CakeForm, OrderForm
from .models import Cake, Order, Payment
from django.shortcuts import redirect

def home(request):
    return redirect('create_cake')


def create_cake(request):
    if request.method == 'POST':
        form = CakeForm(request.POST)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.user = request.user
            cake.save()
            form.save_m2m()
            return redirect('create_order', cake_id=cake.id)
    else:
        form = CakeForm()

    return render(request, 'orders/create_cake.html', {'form': form})


def create_order(request, cake_id):
    cake = Cake.objects.get(id=cake_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.cake = cake

            if order.delivery_type == 'pickup':
                order.address = 'Самовывоз'

            order.save()
            return redirect('pay_order', order_id=order.id)

    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {
        'form': form,
        'cake': cake
    })

def edit_cake(request, cake_id):
    cake = Cake.objects.get(id=cake_id)

    if request.method == 'POST':
        form = CakeForm(request.POST, instance=cake)
        if form.is_valid():
            form.save()
            return redirect('create_order', cake_id=cake.id)
    else:
        form = CakeForm(instance=cake)

    return render(request, 'orders/edit_cake.html', {'form': form})

def pay_order(request, order_id):
    order = Order.objects.get(id=order_id)

    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            'amount': order.cake.total_price
        }
    )

    # имитация успешной оплаты
    payment.status = 'paid'
    payment.save()

    # обновляем статус заказа
    order.status = 'processing'
    order.save()

    return render(request, 'orders/payment_success.html', {
        'order': order
    })

def advance_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.next_status()
    return redirect('order_detail', order_id=order.id)



def success(request):
    return render(request, 'orders/success.html')