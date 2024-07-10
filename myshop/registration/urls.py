from django.urls import path

from . import views

app_name = 'registration'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('admin_dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('user_info/', views.MyUserInfoView.as_view(), name='user_info'),
    path('update_user_info/', views.UpdateUserInfoView.as_view(), name='update_user_info'),
]
