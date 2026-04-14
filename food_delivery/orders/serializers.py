from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from .models import Category, Dish, Order, OrderItem, Shop


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("id", "name", "price", "description", "is_available")


class CategorySerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "sort_order", "dishes")


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("id", "name", "address", "phone", "is_open", "delivery_fee")


class ShopDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ("id", "name", "address", "phone", "is_open", "delivery_fee", "categories")


class OrderItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "dish_name", "unit_price", "quantity", "subtotal")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    shop_name = serializers.CharField(source="shop.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "shop",
            "shop_name",
            "status",
            "status_display",
            "delivery_fee",
            "items_total",
            "total_amount",
            "contact_phone",
            "delivery_address",
            "remark",
            "created_at",
            "items",
        )
        read_only_fields = fields


class OrderItemCreateSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    shop_id = serializers.IntegerField(min_value=1)
    items = OrderItemCreateSerializer(many=True)
    contact_phone = serializers.CharField(max_length=32)
    delivery_address = serializers.CharField(max_length=255)
    remark = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def validate(self, attrs):
        try:
            shop = Shop.objects.get(pk=attrs["shop_id"])
        except Shop.DoesNotExist as e:
            raise serializers.ValidationError({"shop_id": "店铺不存在"}) from e
        if not shop.is_open:
            raise serializers.ValidationError({"shop_id": "店铺休息中，无法下单"})
        attrs["shop"] = shop
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        shop = validated_data["shop"]
        rows = validated_data["items"]
        remark = validated_data.get("remark") or ""

        dish_ids = [r["dish_id"] for r in rows]
        dishes = {
            d.id: d
            for d in Dish.objects.select_related("category").filter(
                id__in=dish_ids,
                category__shop=shop,
                is_available=True,
            )
        }
        if len(dishes) != len(set(dish_ids)):
            missing = set(dish_ids) - set(dishes)
            raise serializers.ValidationError(
                {"items": f"部分菜品无效或已下架: {sorted(missing)}"}
            )

        items_total = Decimal("0")
        order_items_data = []
        for row in rows:
            dish = dishes[row["dish_id"]]
            qty = row["quantity"]
            subtotal = dish.price * qty
            items_total += subtotal
            order_items_data.append(
                {
                    "dish": dish,
                    "dish_name": dish.name,
                    "unit_price": dish.price,
                    "quantity": qty,
                    "subtotal": subtotal,
                }
            )

        delivery_fee = shop.delivery_fee
        total = items_total + delivery_fee

        order = Order.objects.create(
            user=user,
            shop=shop,
            status=Order.Status.PLACED,
            delivery_fee=delivery_fee,
            items_total=items_total,
            total_amount=total,
            contact_phone=validated_data["contact_phone"],
            delivery_address=validated_data["delivery_address"],
            remark=remark,
        )
        for oi in order_items_data:
            OrderItem.objects.create(order=order, **oi)

        return order
