from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit

from .forms import CustomUserCreationForm, UserUpdateForm
from .models import UserProfile


@ratelimit(key='header:x-forwarded-for', rate='10/m', method='POST', block=True)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Вітаємо, {user.username}! Ви успішно зареєструвались.')
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@ratelimit(key='header:x-forwarded-for', rate='20/m', method='POST', block=True)
def login_view(request):
    from django.contrib.auth.views import LoginView
    return LoginView.as_view(
        template_name='accounts/login.html',
    )(request)


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Ваші дані успішно оновлено.')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'u_form': u_form,
    })