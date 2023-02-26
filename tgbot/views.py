import calendar
import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.shortcuts import render

from .models import Order


def show_home(request):
    context = {}
    return render(request, 'index.html', context=context)


def show_orders_quantity_report(request, months_number):
    now = datetime.date.today()
    report_period_date = now - relativedelta(months=months_number)
    year = report_period_date.year
    month = report_period_date.month
    end_day = calendar.monthrange(year, month)[1]
    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month, end_day, 23, 59, 59)

    orders = Order.objects.filter(
        created_at__gte=start_date, created_at__lte=end_date
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
