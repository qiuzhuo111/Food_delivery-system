from decimal import Decimal

from django.db import transaction

from orders.models import Dish, Order, OrderItem


@transaction.atomic
def create_order_from_lines(user, shop, lines, contact_phone, delivery_address, remark):
    """
    lines: dict[str, int] dish_id -> quantity
    """
    dish_ids = [int(i) for i in lines.keys()]
    dishes = {
        d.id: d
        for d in Dish.objects.select_related("category").filter(
            id__in=dish_ids,
            category__shop=shop,
            is_available=True,
        )
    }
    if set(dish_ids) != set(dishes.keys()):
        return None, "部分菜品无效或已下架"

    items_total = Decimal("0")
    order_items_data = []
    for did, qty in lines.items():
        qty = int(qty)
        if qty <= 0:
            continue
        dish = dishes[int(did)]
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

    if not order_items_data:
        return None, "购物车为空"

    delivery_fee = shop.delivery_fee
    total = items_total + delivery_fee

    order = Order.objects.create(
        user=user,
        shop=shop,
        status=Order.Status.PLACED,
        delivery_fee=delivery_fee,
        items_total=items_total,
        total_amount=total,
        contact_phone=contact_phone,
        delivery_address=delivery_address,
        remark=remark or "",
    )
    for oi in order_items_data:
        OrderItem.objects.create(order=order, **oi)

    return order, None
