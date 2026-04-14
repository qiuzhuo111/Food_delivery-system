CART_KEY = "fd_cart"


def get_cart(request):
    data = request.session.get(CART_KEY) or {}
    shop_id = data.get("shop_id")
    lines = data.get("lines") or {}
    if not isinstance(lines, dict):
        lines = {}
    return {"shop_id": shop_id, "lines": {str(k): int(v) for k, v in lines.items() if int(v) > 0}}


def set_cart(request, shop_id, lines):
    request.session[CART_KEY] = {"shop_id": shop_id, "lines": lines}
    request.session.modified = True


def clear_cart(request):
    request.session.pop(CART_KEY, None)
    request.session.modified = True


def add_line(request, shop_id, dish_id, qty=1):
    cart = get_cart(request)
    if cart["shop_id"] is not None and cart["shop_id"] != shop_id:
        cart = {"shop_id": shop_id, "lines": {}}
    lines = dict(cart["lines"])
    key = str(dish_id)
    lines[key] = lines.get(key, 0) + qty
    if lines[key] <= 0:
        lines.pop(key, None)
    set_cart(request, shop_id, lines)


def set_line_qty(request, shop_id, dish_id, qty):
    cart = get_cart(request)
    if cart["shop_id"] != shop_id:
        return
    lines = dict(cart["lines"])
    key = str(dish_id)
    if qty <= 0:
        lines.pop(key, None)
    else:
        lines[key] = qty
    if not lines:
        clear_cart(request)
    else:
        set_cart(request, shop_id, lines)
