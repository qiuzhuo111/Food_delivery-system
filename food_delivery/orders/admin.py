from django.contrib import admin

from .models import Category, Dish, Order, OrderItem, Rider, Shop


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "is_open", "delivery_fee", "phone", "latitude", "longitude")
    list_filter = ("is_open",)
    search_fields = ("name",)
    inlines = [CategoryInline]


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "status", "phone", "vehicle", "rating")
    list_filter = ("status", "vehicle")
    search_fields = ("name", "phone", "user__username")


class DishInline(admin.TabularInline):
    model = Dish
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "sort_order")
    list_filter = ("shop",)
    inlines = [DishInline]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("is_available", "category__shop")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("dish", "dish_name", "unit_price", "quantity", "subtotal")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "shop",
        "rider",
        "user",
        "status",
        "total_amount",
        "contact_phone",
        "created_at",
    )
    list_filter = ("status", "shop")
    list_editable = ("status",)
    search_fields = ("contact_phone", "delivery_address", "user__username")
    readonly_fields = (
        "user",
        "shop",
        "delivery_fee",
        "items_total",
        "total_amount",
        "created_at",
        "updated_at",
    )
    inlines = [OrderItemInline]
