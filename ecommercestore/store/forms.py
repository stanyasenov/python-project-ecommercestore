
from django import forms


from ecommercestore.common.helpers import BootstrapFormMixin, DisabledFieldsFormMixin
from ecommercestore.store.models import Product, OrderItem


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class DeleteProductForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        orderitem = OrderItem(
            quantity=0
        )
        self.instance.delete()
        return self.instance, orderitem

    class Meta:
        model = Product
        exclude = {'name', 'price', 'digital', 'description', 'image'}


class EditProductForm2(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Product
        fields = "__all__"
