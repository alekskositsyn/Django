from django import forms

from mainapp.models import Product
from ordersapp.models import Order, OrderItem


class BaseFormControlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control btn btn-outline-secondary'


class OrderForm(BaseFormControlForm):
    class Meta:
        model = Order
        exclude = ('user', 'status', 'is_active')


class OrderItemForm(BaseFormControlForm):
    price = forms.FloatField(label='цена', required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.get_active_items()
