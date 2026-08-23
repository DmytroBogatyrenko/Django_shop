from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from shop.models import Product
from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if Review.objects.filter(user=request.user, product=product).exists():
        messages.warning(request, 'Ви вже залишили відгук на цей товар.')
        return redirect(product.get_absolute_url())

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(
                request,
                'Дякуємо за відгук! Він зʼявиться після модерації'
            )
        else:
            messages.error(request, 'Перевірте правильність заповнення форми')

    return redirect(product.get_absolute_url())