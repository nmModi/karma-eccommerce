from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int, widget=forms.NumberInput(attrs={'class': 'input-text qty', 'min': '1', 'max': '10', 'value': '1'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
