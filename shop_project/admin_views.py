import csv
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone


@staff_member_required
def dashboard(request):
    from orders.models import Order, OrderItem

    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    last_7_days  = now - timedelta(days=7)

    total_stats = Order.objects.filter(
        status__in=['processing', 'shipped', 'delivered']
    ).aggregate(
        total_revenue=Sum('total_price'),
        total_orders=Count('id'),
        avg_order=Avg('total_price'),
    )

    recent_stats = Order.objects.filter(
        created_at__gte=last_30_days,
        status__in=['processing', 'shipped', 'delivered'],
    ).aggregate(
        revenue=Sum('total_price'),
        orders=Count('id'),
    )

    top_products = (
        OrderItem.objects
        .filter(order__status__in=['processing', 'shipped', 'delivered'])
        .values('product_name')
        .annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('price'),
        )
        .order_by('-total_quantity')[:10]
    )

    sales_by_day = []
    for i in range(6, -1, -1):
        day = now - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0)
        day_end   = day.replace(hour=23, minute=59, second=59)

        day_revenue = Order.objects.filter(
            created_at__range=(day_start, day_end),
            status__in=['processing', 'shipped', 'delivered'],
        ).aggregate(rev=Sum('total_price'))['rev'] or 0

        sales_by_day.append({
            'date': day.strftime('%d.%m'),
            'revenue': float(day_revenue),
        })

    orders_by_status = (
        Order.objects
        .values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )

    return render(request, 'admin/dashboard.html', {
        'total_stats': total_stats,
        'recent_stats': recent_stats,
        'top_products': top_products,
        'sales_by_day': sales_by_day,
        'orders_by_status': orders_by_status,
        'title': 'Analytics Dashboard',
    })


@staff_member_required
def export_orders_csv(request):

    from orders.models import Order

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Покупець', 'Статус', 'Сума', 'Знижка %',
        'Дата створення', 'Очікувана доставка',
    ])

    orders = Order.objects.select_related('user').order_by('-created_at')
    for order in orders:
        writer.writerow([
            order.id,
            order.user.username if order.user else 'Гість',
            order.get_status_display(),
            order.total_price,
            order.discount,
            order.created_at.strftime('%d.%m.%Y %H:%M'),
            order.estimated_delivery.strftime('%d.%m.%Y') if order.estimated_delivery else '',
        ])

    return response