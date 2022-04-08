from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

from ecommercestore.accounts.forms import CreateProfileForm, ProfileEditForm
from ecommercestore.accounts.models import Customer
from ecommercestore.store.models import Order


class ProfileDetailsView(DetailView):
    model = Customer
    template_name = 'store/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order, created = Order.objects.get_or_create(customer=self.object.user_id, complete=False)
        cartItems = order.get_cart_items

        context.update({
            'cartItems': cartItems,
        })
        return context


class UserRegistrationView(CreateView):
    form_class = CreateProfileForm
    template_name = 'store/register.html'
    success_url = reverse_lazy('store')


class UserLoginView(LoginView):
    template_name = 'store/login.html'

    def get_success_url(self):
        return reverse_lazy('store')


class UserLogoutView(LogoutView):

    def get_success_url(self):
        return reverse_lazy('store')


class ChangeUserPasswordView(PasswordChangeView):
    template_name = 'store/change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order, created = Order.objects.get_or_create(customer=self.request.user.id, complete=False)
        cartItems = order.get_cart_items

        context.update({
            'cartItems': cartItems,
        })
        return context


class ChangeProfileDetails(UpdateView):
    model = Customer
    template_name = 'store/profile_edit.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('store')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order, created = Order.objects.get_or_create(customer=self.object.user_id, complete=False)
        cartItems = order.get_cart_items

        context.update({
            'cartItems': cartItems,
        })
        return context



