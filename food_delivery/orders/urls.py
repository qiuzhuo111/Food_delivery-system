from django.urls import path

from . import views

urlpatterns = [
    path("auth/register/", views.RegisterView.as_view(), name="auth-register"),
    path("auth/login/", views.LoginView.as_view(), name="auth-login"),
    path("shops/", views.ShopListView.as_view(), name="shop-list"),
    path("shops/<int:pk>/", views.ShopDetailView.as_view(), name="shop-detail"),
    path("orders/", views.OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/cancel/", views.OrderCancelView.as_view(), name="order-cancel"),
]
