from django import forms


class PromocodeForm(forms.Form):
    code = forms.CharField(
        max_length=50,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть промокод: ',
        })
    )