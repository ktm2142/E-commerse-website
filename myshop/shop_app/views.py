from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, View, FormView, TemplateView
from django.contrib import messages

from .forms import OrderForm, UpdateQuantityForm
from .models import Category, Product, Order, OrderItem
from registration.models import UserProfile


class HomeView(ListView):
    model = Category
    template_name = 'shop_app/home.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop_app/category_detail.html'
    context_object_name = 'category'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_options = {
            'price_asc': 'price',
            'price_desc': '-price'
        }
        sort_by = self.request.GET.get('sort', 'price_asc')
        sort_field = sort_options.get(sort_by, 'price')

        show_available = self.request.GET.get('show_available', False)
        if show_available:
            products = Product.objects.filter(category=self.object, available=True).order_by(sort_field)
        else:
            products = Product.objects.filter(category=self.object).order_by(sort_field)

        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['show_available'] = show_available
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop_app/product_detail.html'
    context_object_name = 'product'


class OrderListView(LoginRequiredMixin, ListView):
    """Here's get_queryset() instead of Django queryset,
    because in Django queryset you load all uncompleted orders of all users"""
    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user, is_completed=False)
            .prefetch_related(
                Prefetch(
                    'order_items',
                    queryset=OrderItem.objects.select_related('product')
                )
            )
        )


class OrderDetailsView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop_app/order_details.html'
    queryset = (Order.objects
                .prefetch_related(Prefetch('order_items', queryset=OrderItem.objects.select_related('product')))
                .select_related('user'))


class AddToCardView(LoginRequiredMixin, View):
    def post(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'price': product.price, 'quantity': 1}
        )
        if not created:
            order_item.quantity += 1
            order_item.save()

        messages.success(request, f'{product.title} added to cart')

        return redirect('shop_app:product_detail', pk=product_pk)


class UpdateQuantityView(LoginRequiredMixin, UpdateView):
    model = OrderItem
    template_name_suffix = '_update_form'
    form_class = UpdateQuantityForm
    context_object_name = 'order_item'

    def get_success_url(self):
        return reverse('shop_app:order_list')

    def form_valid(self, form):
        order_item = self.get_object()
        quantity = form.cleaned_data['quantity']
        if quantity <= 0:
            return redirect(reverse('shop_app:delete_order_item', kwargs={'pk': order_item.pk}))
        else:
            order_item.quantity = quantity
            order_item.save()
            return super().form_valid(form)


class DeleteOrderItemView(LoginRequiredMixin, DeleteView):
    model = OrderItem
    success_url = reverse_lazy('shop_app:order_list')


class ProductSearchView(ListView):
    model = Product
    template_name = 'shop_app/product_search.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = super().get_queryset().annotate(
                similarity=TrigramSimilarity('title', query) + TrigramSimilarity('description', query)
            ).filter(similarity__gt=0.3)
        else:
            queryset = Product.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        if not context['query']:
            context['message'] = "Please, enter your search request"
        return context


class CheckOutView(LoginRequiredMixin, FormView):
    template_name = 'shop_app/checkout.html'
    form_class = OrderForm
    success_url = reverse_lazy('shop_app:checkout_completed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = (Order.objects
                 .filter(user=self.request.user, is_completed=False)
                 .prefetch_related(
                    Prefetch('order_items', queryset=OrderItem.objects.select_related('product')))
                 .first())
        if order:
            context['order'] = order
            cart_items = order.order_items.all()
            context['cart_items'] = cart_items
            context['total_price'] = sum(item.total_price for item in cart_items)
        else:
            redirect('shop_app:order_list')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        order = get_object_or_404(Order, user=self.request.user, is_completed=False)
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        order.first_name = form.cleaned_data['first_name']
        order.last_name = form.cleaned_data['last_name']
        order.phone_number = form.cleaned_data['phone_number']
        order.email = user_profile.email
        order.address = form.cleaned_data['address']
        order.city = form.cleaned_data['city']
        order.is_completed = True
        order.save()

        super().form_valid(form)
        return redirect('shop_app:checkout_completed')


class CheckoutCompletedView(LoginRequiredMixin, TemplateView):
    template_name = 'shop_app/checkout_completed.html'
