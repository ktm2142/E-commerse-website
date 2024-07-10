from django import forms
from .models import Order, OrderItem, Category


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.userprofile.first_name
            self.fields['last_name'].initial = user.userprofile.last_name
            self.fields['phone_number'].initial = user.userprofile.phone_number
            self.fields['city'].initial = user.userprofile.city
            self.fields['address'].initial = user.userprofile.address

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'city', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UpdateQuantityForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control',
                                                 'style': 'width: 100px;'}),
        }
