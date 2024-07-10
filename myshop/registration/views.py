from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserProfileForm
from .models import UserProfile

from shop_app.models import Order, OrderItem


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('registration:user_info')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('registration:user_info')


class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'registration/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('shop_app:home')


class MyUserInfoView(TemplateView):
    template_name = 'registration/user_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        completed_orders = (Order.objects
                            .filter(user=user, is_completed=True)
                            .prefetch_related(
                                Prefetch(
                                    'order_items',
                                    queryset=OrderItem.objects.select_related('product'))))
        context['completed_orders'] = completed_orders
        return context


class UpdateUserInfoView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'registration/update_user_info.html'
    success_url = reverse_lazy('registration:user_info')

    def get_object(self, queryset=None):
        try:
            return self.request.user.userprofile
        except UserProfile.DoesNotExist:
            return UserProfile.objects.create(user=self.request.user)
