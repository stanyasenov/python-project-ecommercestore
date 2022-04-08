import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.http import JsonResponse

from ecommercestore.accounts.models import Customer
from ecommercestore.store.forms import CreateProductForm, DeleteProductForm, EditProductForm2
from ecommercestore.store.models import Product, Order, OrderItem, ShippingAddress
import json


def HomeView(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=Customer.objects.get(user=request.user), complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=Customer.objects.get(user=request.user), complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #Create empty cart for now for non-logged in user
        items = []
        order = {'get_card_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems':cartItems}

    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=Customer.objects.get(user=request.user), complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
       #Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', type(productId))

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=Customer.objects.get(user=request.user), complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=Customer.objects.get(user=request.user), complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        print(customer.id)
        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=Customer.objects.get(user=request.user),
                order=Order.objects.get(id=order.id),
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('User is not logged in')

    return JsonResponse('Payment submitted..', safe=False)


@method_decorator(staff_member_required, name='dispatch')
class AddProductView(CreateView):
    template_name = 'store/product_add.html'
    form_class = CreateProductForm
    success_url = reverse_lazy('store')

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('store'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.user_id = self.request.user.id
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items

        context.update({
            'cartItems': cartItems,
        })
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.user_id = self.request.user.id
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items

        context.update({
            'cartItems': cartItems,
        })
        return context


@method_decorator(staff_member_required, name='dispatch')
class EditProductView(UpdateView):
    model = Product
    template_name = 'store/product_edit.html'
    form_class = EditProductForm2
    success_url = reverse_lazy('store')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.user_id = self.request.user.id
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items

        context.update({
            'cartItems': cartItems,
        })
        return context


@method_decorator(staff_member_required, name='dispatch')
class DeleteProductView(DeleteView):
    model = Product
    template_name = 'store/product_delete.html'
    form_class = DeleteProductForm
    success_url = reverse_lazy('store')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.user_id = self.request.user.id
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items

        context.update({
            'cartItems': cartItems,
        })
        return context






