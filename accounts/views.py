from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit

from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm
from .models import UserProfile
from shop_project import settings

from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=not settings.DEBUG), name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


@ratelimit(key='ip', rate='10/m', method='POST', block=not settings.DEBUG)
def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Вітаємо, {user.username}! Ви успішно зареєструвались')
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Профіль успішно оновлено')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Перевірте правильність заповнення форми')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/profile.html', {
        'profile': user_profile,
        'u_form': u_form,
        'p_form': p_form,
    })