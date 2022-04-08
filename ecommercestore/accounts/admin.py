from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin

from ecommercestore.accounts.forms import CreateProfileForm
from ecommercestore.accounts.models import Customer, PetstagramUser
from ecommercestore.store.models import Product, Order, OrderItem, ShippingAddress


class UserAdminConfig(UserAdmin):
    model = PetstagramUser
    list_display = ('username', 'is_staff', 'is_superuser', 'is_active')

    list_filter = ('groups',)
    fieldsets = (
        # Other fieldsets

        ('Group Permissions', {
            'fields': ('groups', 'user_permissions', 'is_staff', 'is_superuser', )
        }),
    )


admin.site.register(PetstagramUser, UserAdminConfig)

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)



