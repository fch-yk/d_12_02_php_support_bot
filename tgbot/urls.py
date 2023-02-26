from django.urls import path

from tgbot import views

urlpatterns = [
    path('', views.show_home),
    path(
        'orders_quantity_report/<int:months_number>/',
        views.show_orders_quantity_report
    ),

]
