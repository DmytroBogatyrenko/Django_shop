from django import forms

from .models import Order, ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model  = ShippingAddress
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'city', 'address', 'postal_code']
        widgets = {
            'first_name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Іванко'}),
            'last_name':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Петренко'}),
            'email':       forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}),
            'phone':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380991234567'}),
            'city':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Київ'}),
            'address':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'вул. Хрещатик, 1, кв. 10'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01001'}),
        }


class OrderCheckoutForm(forms.Form):

    payment_method = forms.ChoiceField(
        label='Спосіб оплати',
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        initial='cash',
    )
    notes = forms.CharField(
        label='Коментар до замовлення',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Необов’язково'}),
    )