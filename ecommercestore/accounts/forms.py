from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from ecommercestore.accounts.models import Customer
from ecommercestore.common.helpers import BootstrapFormMixin, DisabledFieldsFormMixin
from ecommercestore.store.models import Order, ShippingAddress


class CreateProfileForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    name = forms.CharField(
        max_length=Customer.CUSTOMER_NAME_MAX_LEN,
    )
    email = forms.EmailField()
    description = forms.CharField(
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=commit)
        order = Order(
            customer_id=user.id,
            transaction_id=user.id,
            complete=False,
        )
        profile = Customer(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            description=self.cleaned_data['description'],
            user=user,
        )

        if commit:
            profile.save()
            order.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'name', 'email', 'description')


class ProfileEditForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Customer
        exclude = {'user', 'email'}

