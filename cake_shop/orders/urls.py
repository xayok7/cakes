from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cake/', views.create_cake, name='create_cake'),
    path('order/<int:cake_id>/', views.create_order, name='create_order'),
    path('success/', views.success, name='success'),
    path('pay/<int:order_id>/', views.pay_order, name='pay_order'),
    path('cake/edit/<int:cake_id>/', views.edit_cake, name='edit_cake'),
]