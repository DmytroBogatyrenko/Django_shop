from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Promocode


@require_POST
def apply_promocode(request):

    code = request.POST.get('code', '').strip().upper()

    if not code:
        return JsonResponse({'success': False, 'error': 'Введіть код промокоду'})

    try:
        promocode = Promocode.objects.filter(code__iexact=code).first()
        if not promocode:
            return JsonResponse({'success': False, 'error': 'Промокод не знайдено'})
    except Exception:
        return JsonResponse({'success': False, 'error': 'Помилка перевірки промокоду'})

    if not promocode.is_valid():
        return JsonResponse({'success': False, 'error': 'Промокод прострочений або вичерпаний'})

    request.session['promocode_id'] = promocode.id
    request.session['promocode_code'] = promocode.code
    request.session['promocode_value'] = promocode.value

    return JsonResponse({
        'success': True,
        'code': promocode.code,
        'value': promocode.value,
        'message': f'Промокод застосовано! Знижка {promocode.value}%'
    })


def remove_promocode(request):
    for key in ['promocode_id', 'promocode_code', 'promocode_value']:
        request.session.pop(key, None)
    return JsonResponse({'success': True})