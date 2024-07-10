from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector

from .models import Category, Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'is_completed', 'shipped')
    list_filter = ('is_completed', 'shipped')
    search_fields = ('user__username', 'user__email')
    readonly_fields = (
        'id',
        'user',
        'first_name',
        'last_name',
        'phone_number',
        'email',
        'address',
        'city',
        'created_at',
        'is_completed'
    )
    list_editable = ('is_completed', 'shipped')
    inlines = [OrderItemInline]


admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    exclude = ('search_vector',)