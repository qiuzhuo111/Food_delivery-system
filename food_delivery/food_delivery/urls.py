from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("readme/", views.readme, name="readme"),
    path("dev/", views.dev_index, name="dev_index"),
    path("shops/", views.shop_list, name="shop_list"),
    path("shops/<int:pk>/", views.shop_detail, name="shop_detail"),
    path("deals/", views.deals, name="deals"),
    path("membership/", views.membership, name="membership"),
    path("membership/open/<slug:tier>/", views.membership_open, name="membership_open"),
    path("help-center/", views.help_center, name="help_center"),
    path("map/", views.map_tracker, name="map_tracker"),
    path("riders/", views.riders_page, name="riders_page"),
    path("rider/login/", views.rider_login, name="rider_login"),
    path("rider/dashboard/", views.rider_dashboard, name="rider_dashboard"),
    path("rider/orders/<int:pk>/take/", views.rider_take_order, name="rider_take_order"),
    path("rider/orders/<int:pk>/status/", views.rider_update_order_status, name="rider_update_order_status"),
    path("rider/orders/<int:pk>/reject/", views.rider_reject_order, name="rider_reject_order"),
    path("rider/orders/<int:pk>/issue/", views.rider_report_issue, name="rider_report_issue"),
    path("shops/<int:pk>/cart/add/", views.cart_add, name="cart_add"),
    path("shops/<int:pk>/cart/update/", views.cart_update, name="cart_update"),
    path("shops/<int:pk>/cart/clear/", views.cart_clear, name="cart_clear"),
    path("cart/checkout/", views.checkout, name="checkout"),
    path("accounts/login/", views.user_login, name="login"),
    path("accounts/register/", views.user_register, name="register"),
    path("accounts/logout/", views.user_logout, name="logout"),
    path("orders/", views.my_orders, name="my_orders"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("orders/<int:pk>/cancel/", views.order_cancel, name="order_cancel"),
    path("admin/", admin.site.urls),
    path("api/", include("orders.urls")),
]
