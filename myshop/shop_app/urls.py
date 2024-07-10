from django.urls import path
from . import views

app_name = 'shop_app'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    # path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    path('cart/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', views.OrderDetailsView.as_view(), name='order_details'),
    path('add_to_cart/<int:product_pk>/', views.AddToCardView.as_view(), name='add_to_cart'),
    path('update_quantity/<int:pk>/', views.UpdateQuantityView.as_view(), name='update_quantity'),
    path('delete_order_item/<int:pk>/', views.DeleteOrderItemView.as_view(), name='delete_order_item'),
    path('checkout/', views.CheckOutView.as_view(), name='checkout'),
    path('checkout_completed/', views.CheckoutCompletedView.as_view(), name='checkout_completed'),
]
