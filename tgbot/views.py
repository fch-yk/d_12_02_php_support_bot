import calendar
import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db.models import Count
from django.shortcuts import render

from .models import Order


def show_home(request):
    context = {}
    return render(request, 'index.html', context=context)


def show_orders_quantity_report(request, months_number):
    now = datetime.date.today()
    start_date, end_date = get_report_month_period_dates(months_number)

    orders = Order.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    ).values('client', 'client__name').annotate(num_orders=Count('id'))

    orders_quantity = Order.objects.filter(
        created_at__gte=start_date, created_at__lte=end_date).count()

    period_format = '%d.%m.%Y'
    context = {
        'orders': orders,
        'orders_quantity': orders_quantity,
        'start_date': start_date.strftime(period_format),
        'end_date': end_date.strftime(period_format),
    }
    return render(request, 'oqreport.html', context=context)


def show_subcontractors_wages_report(request, months_number):
    order_price = settings.ORDER_PRICE
    start_date, end_date = get_report_month_period_dates(months_number)

    completed_orders = Order.objects.filter(
        due_date__gte=start_date,
        due_date__lte=end_date,
        status=Order.COMPLETED,
    ).exclude(subcontractor__isnull=True)

    orders_subcontractors_numbers = completed_orders.values(
        'subcontractor', 'subcontractor__name'
    ).annotate(sum=Count('id') * order_price, num_orders=Count('id'))

    orders_number = completed_orders.count()

    period_format = '%d.%m.%Y'
    context = {
        'orders_subcontractors_numbers': orders_subcontractors_numbers,
        'orders_number': orders_number,
        'start_date': start_date.strftime(period_format),
        'end_date': end_date.strftime(period_format),
        'total_sum': orders_number * order_price,
        'order_price': order_price,
    }
    return render(request, 'swreport.html', context=context)


def get_report_month_period_dates(subtracted_months_number):
    now = datetime.date.today()
    report_period_date = now - relativedelta(months=subtracted_months_number)
    year = report_period_date.year
    month = report_period_date.month
    end_day = calendar.monthrange(year, month)[1]
    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month, end_day, 23, 59, 59)
    return start_date, end_date
