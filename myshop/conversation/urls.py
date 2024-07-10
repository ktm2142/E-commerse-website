from django.urls import path
from .views import AdminConversationView, UserConversationView

urlpatterns = [
    path('admin_user_list/', AdminConversationView.as_view(), name='admin_user_list'),
    path('admin_conversation/<int:user_id>/', AdminConversationView.as_view(), name='admin_conversation'),
    path('user_conversation/', UserConversationView.as_view(), name='user_conversation'),
]
