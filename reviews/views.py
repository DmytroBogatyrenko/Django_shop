from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from orders.models import OrderItem
from shop.models import Product
from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
    ).exists()

    if not has_purchased:
        messages.error(request, 'Ви можете залишати відгук лише на товари, які ви придбали.')
        return redirect(product.get_absolute_url())

    if Review.objects.filter(user=request.user, product=product).exists():
        messages.warning(request, 'Ви вже залишили відгук на цей товар.')
        return redirect(product.get_absolute_url())

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.is_verified_purchase = True
            review.save()
            messages.success(
                request,
                'Дякуємо за відгук! Він успішно доданий.'
            )
        else:
            messages.error(request, 'Перевірте правильність заповнення форми відгуку')

    return redirect(product.get_absolute_url())


@require_POST
def vote_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    vote_type = request.POST.get('vote_type')
    
    if vote_type == 'helpful':
        review.helpful_votes += 1
        review.save(update_fields=['helpful_votes'])
        return JsonResponse({'success': True, 'helpful_votes': review.helpful_votes})
    elif vote_type == 'unhelpful':
        review.unhelpful_votes += 1
        review.save(update_fields=['unhelpful_votes'])
        return JsonResponse({'success': True, 'unhelpful_votes': review.unhelpful_votes})

    return JsonResponse({'success': False, 'error': 'Некоректний тип голосу'})