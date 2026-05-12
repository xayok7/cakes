from django.shortcuts import render, redirect
from .forms import CakeForm, OrderForm
from .models import Cake, Order, User, Pie
from .services.breakdown import CakeCategory, CakeItem
from .services.facade import OrderManagementFacade
from .services.commands import OrderInvoker, AdvanceOrderStatusCommand
from .services.pricing import SimplePieStrategy
from .services.proxy import PricingProxy

def home(request):
    return redirect('create_cake')

def create_cake(request):
    if request.method == 'POST':
        form = CakeForm(request.POST)

        if form.is_valid():
            user = User.objects.first()
            validated_data = form.cleaned_data
            decorations = validated_data.get('decorations')

            extras = {
                'candles': request.POST.get('candles'),
                'text': request.POST.get('text'),
                'express': request.POST.get('express'),
            }

            facade = OrderManagementFacade()
            cake = facade.create_and_calculate_cake(user, validated_data, decorations, extras)

            return redirect('create_order', cake_id=cake.id)
        else:
            print(form.errors)
    else:
        form = CakeForm()

    return render(request, 'orders/create_cake.html', {'form': form})

def create_order(request, cake_id):
    cake = Cake.objects.get(id=cake_id)

    breakdown_root = CakeCategory("Спецификация вашего торта")

    base_cat = CakeCategory("Основа и размер")
    base_cat.add(CakeItem(f"Форма: {cake.get_shape_display()}"))
    base_cat.add(CakeItem(f"Размер: {cake.get_size_display()}"))
    breakdown_root.add(base_cat)

    if cake.base or cake.cream or cake.filling:
        fill_cat = CakeCategory("Внутреннее наполнение")
        if cake.base:
            fill_cat.add(CakeItem(f"Бисквит: {cake.base.name}"))
        if cake.cream:
            fill_cat.add(CakeItem(f"Крем: {cake.cream.name}"))
        if cake.filling:
            fill_cat.add(CakeItem(f"Начинка: {cake.filling.name}"))
        breakdown_root.add(fill_cat)

    if cake.decorations.exists():
        decor_cat = CakeCategory("Дополнительный декор")
        for decor in cake.decorations.all():
            decor_cat.add(CakeItem(decor.name))
        breakdown_root.add(decor_cat)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = User.objects.first()
            order.cake = cake
            if order.delivery_type == 'pickup':
                order.address = 'Самовывоз'
            order.save()

            facade = OrderManagementFacade()
            steps = facade.process_order_delivery(order)
            receipt, ticket = facade.get_order_documents(order)

            return render(request, 'orders/order_steps.html', {
                'steps': steps,
                'order': order,
                'receipt': receipt,
                'ticket': ticket
            })
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {
        'form': form,
        'cake': cake,
        'breakdown': breakdown_root
    })

def create_pie(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        size = request.POST.get('size')
        dough = request.POST.get('dough')

        pie = Pie.objects.create(
            name=name,
            size=size,
            dough=dough
        )

        strategy = SimplePieStrategy()
        proxy = PricingProxy(strategy)

        pie.total_price = proxy.calculate(pie)
        pie.save()

        return redirect('success')

    return redirect('home')

def edit_cake(request, cake_id):
    cake = Cake.objects.get(id=cake_id)

    if request.method == 'POST':
        form = CakeForm(request.POST, instance=cake)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.save()

            form.save_m2m()

            cake.total_price = cake.calculate_price()
            cake.save()
            return redirect('create_order', cake_id=cake.id)
    else:
        form = CakeForm(instance=cake)

    return render(request, 'orders/edit_cake.html', {'form': form})

def pay_order(request, order_id):
    order = Order.objects.get(id=order_id)
    
    wants_email = bool(request.POST.get('send_email'))

    facade = OrderManagementFacade()
    facade.process_payment(order, send_email=wants_email)

    return render(request, 'orders/payment_success.html', {'order': order})

def advance_order(request, order_id):
    order = Order.objects.get(id=order_id)

    invoker = OrderInvoker()
    command = AdvanceOrderStatusCommand(order)
    invoker.execute_command(command)

    return redirect('home')

def success(request):
    return render(request, 'orders/success.html')
