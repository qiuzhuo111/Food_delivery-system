from decimal import Decimal
import math

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape
from django.views.decorators.http import require_POST

from orders.models import Category, Dish, Order, Rider, Shop

from .cart_session import add_line, clear_cart, get_cart, set_line_qty
from .forms import CheckoutForm, LoginForm, RegisterForm
from .order_service import create_order_from_lines


SHOP_COVER_KEYS = (
    "cover-1",
    "cover-2",
    "cover-3",
    "cover-4",
    "cover-5",
    "cover-6",
    "cover-7",
    "cover-8",
)


def _attach_shop_cover(shops):
    shop_list = list(shops)
    for idx, shop in enumerate(shop_list):
        shop.cover_key = SHOP_COVER_KEYS[idx % len(SHOP_COVER_KEYS)]
    return shop_list


def readme(_request):
    path = settings.BASE_DIR / "README.md"
    if not path.is_file():
        return HttpResponse("README.md 未找到", status=404, content_type="text/plain; charset=utf-8")
    raw = path.read_text(encoding="utf-8")
    body = escape(raw)
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>README · 鲜达外卖</title>
  <style>
    body {{ font-family: system-ui, "Segoe UI", "PingFang SC", sans-serif; margin: 0; background: #faf7f2; color: #1c1917; }}
    pre {{ white-space: pre-wrap; word-break: break-word; margin: 0; padding: 1.25rem 1.5rem 2rem; font-size: 0.9rem; line-height: 1.55; }}
    a.bar {{ display: inline-block; margin: 1rem 1.5rem 0; color: #ea580c; }}
  </style>
</head>
<body>
  <a class="bar" href="/">← 返回首页</a>
  <pre>{body}</pre>
</body>
</html>"""
    return HttpResponse(html, content_type="text/html; charset=utf-8")


def dev_index(_request):
    return HttpResponse(
        """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>API 说明</title></head>
<body style="font-family:system-ui;padding:2rem;">
<h1>开发者 · API</h1>
<ul>
  <li><a href="/readme/">README（完整说明）</a></li>
  <li><a href="/admin/">管理后台</a></li>
  <li><a href="/api/shops/">店铺列表 JSON</a></li>
  <li>注册：<code>POST /api/auth/register/</code></li>
</ul>
<p><a href="/">返回首页</a></p>
</body>
</html>""",
        content_type="text/html; charset=utf-8",
    )


def home(request):
    shops = _attach_shop_cover(Shop.objects.filter(is_open=True)[:12])
    return render(request, "food_delivery/home.html", {"shops": shops})


def shop_list(request):
    shops = _attach_shop_cover(Shop.objects.all())
    return render(request, "food_delivery/shop_list.html", {"shops": shops})


def deals(request):
    shops = _attach_shop_cover(Shop.objects.filter(is_open=True)[:8])
    highlights = [
        {
            "title": "新客立减",
            "desc": "首单最高减 ¥18，支持多家精选品牌。",
            "tag": "限时福利",
        },
        {
            "title": "夜宵频道",
            "desc": "22:00 后下单可享免配送费活动。",
            "tag": "夜间专属",
        },
        {
            "title": "周末家庭餐",
            "desc": "2-4 人套餐组合更省钱，覆盖主流菜系。",
            "tag": "人气爆款",
        },
    ]
    return render(
        request,
        "food_delivery/deals.html",
        {"shops": shops, "highlights": highlights},
    )


def membership(_request):
    tiers = [
        {"name": "Silver", "price": "¥19/月", "benefits": ["每月 4 张配送券", "专属客服通道"]},
        {"name": "Gold", "price": "¥39/月", "benefits": ["无限免配送（规则内）", "热门店铺 95 折", "优先骑手调度"]},
        {"name": "Platinum", "price": "¥79/月", "benefits": ["Gold 全部权益", "每月 2 张大额满减券", "新品尝鲜优先体验"]},
    ]
    return render(_request, "food_delivery/membership.html", {"tiers": tiers})


def membership_open(request, tier):
    plans = {
        "silver": {
            "name": "Silver",
            "price": "¥19/月",
            "desc": "适合日常轻度点餐用户",
            "benefits": ["每月 4 张配送券", "专属客服通道", "会员日优先提醒"],
        },
        "gold": {
            "name": "Gold",
            "price": "¥39/月",
            "desc": "高频用户首选，折扣与配送权益更全面",
            "benefits": ["无限免配送（规则内）", "热门店铺 95 折", "优先骑手调度"],
        },
        "platinum": {
            "name": "Platinum",
            "price": "¥79/月",
            "desc": "重度用户进阶权益，覆盖更多场景",
            "benefits": ["Gold 全部权益", "每月 2 张大额满减券", "新品尝鲜优先体验"],
        },
    }
    plan = plans.get(tier)
    if not plan:
        messages.error(request, "会员类型不存在")
        return redirect("membership")
    return render(request, "food_delivery/membership_open.html", {"plan": plan})


def help_center(_request):
    faqs = [
        {"q": "配送超时怎么办？", "a": "你可在订单详情页发起催单或联系客服，系统会按规则补偿优惠券。"},
        {"q": "如何申请退款？", "a": "订单页支持发起售后申请，平台将在审核后原路退款。"},
        {"q": "如何开具发票？", "a": "结算页可填写发票信息，订单完成后可在订单详情查看下载入口。"},
    ]
    return render(_request, "food_delivery/help_center.html", {"faqs": faqs})


def map_tracker(request):
    shops = list(Shop.objects.filter(is_open=True).order_by("id"))
    riders = list(Rider.objects.order_by("id"))
    return render(request, "food_delivery/map_tracker.html", {"shops": shops, "riders": riders})


def riders_page(request):
    riders = Rider.objects.order_by("status", "-rating", "name")
    return render(request, "food_delivery/riders.html", {"riders": riders})


def _get_current_rider(request):
    if not request.user.is_authenticated:
        return None
    return Rider.objects.filter(user=request.user).first()


def _distance_km(lat1, lng1, lat2, lng2):
    r = 6371.0
    phi1, phi2 = math.radians(float(lat1)), math.radians(float(lat2))
    d_phi = math.radians(float(lat2) - float(lat1))
    d_lambda = math.radians(float(lng2) - float(lng1))
    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def rider_login(request):
    if request.user.is_authenticated and _get_current_rider(request):
        return redirect("rider_dashboard")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        rider = Rider.objects.filter(user=user).first()
        if not rider:
            messages.error(request, "该账号未绑定骑手身份")
        else:
            login(request, user)
            messages.success(request, f"欢迎回来，{rider.name}")
            return redirect("rider_dashboard")

    return render(request, "food_delivery/rider_login.html", {"form": form})


@login_required
def rider_dashboard(request):
    rider = _get_current_rider(request)
    if not rider:
        messages.error(request, "当前账号未绑定骑手身份，请联系管理员")
        return redirect("home")

    raw_available_orders = list(
        Order.objects.filter(status=Order.Status.PLACED, rider__isnull=True)
        .select_related("shop", "user")
        .order_by("created_at")[:50]
    )
    for order in raw_available_orders:
        order.distance_km = _distance_km(
            rider.current_latitude,
            rider.current_longitude,
            order.shop.latitude,
            order.shop.longitude,
        )
    available_orders = sorted(raw_available_orders, key=lambda o: o.distance_km)[:30]

    my_orders = (
        Order.objects.filter(rider=rider)
        .select_related("shop", "user")
        .order_by("-created_at")[:50]
    )
    return render(
        request,
        "food_delivery/rider_dashboard.html",
        {
            "rider": rider,
            "available_orders": available_orders,
            "my_orders": my_orders,
        },
    )


@login_required
@require_POST
def rider_take_order(request, pk):
    rider = _get_current_rider(request)
    if not rider:
        messages.error(request, "当前账号未绑定骑手身份")
        return redirect("home")

    order = get_object_or_404(Order, pk=pk)
    if order.rider_id and order.rider_id != rider.id:
        messages.error(request, "该订单已被其他骑手接单")
        return redirect("rider_dashboard")
    if order.status != Order.Status.PLACED:
        messages.error(request, "该订单当前不可接单")
        return redirect("rider_dashboard")

    order.rider = rider
    order.status = Order.Status.ACCEPTED
    order.save(update_fields=["rider", "status", "updated_at"])
    rider.status = Rider.Status.DELIVERING
    rider.save(update_fields=["status"])
    messages.success(request, f"接单成功：订单 #{order.id}")
    return redirect("rider_dashboard")


@login_required
@require_POST
def rider_update_order_status(request, pk):
    rider = _get_current_rider(request)
    if not rider:
        messages.error(request, "当前账号未绑定骑手身份")
        return redirect("home")

    order = get_object_or_404(Order, pk=pk, rider=rider)
    next_status = request.POST.get("next_status", "")
    transitions = {
        Order.Status.ACCEPTED: Order.Status.DELIVERING,
        Order.Status.DELIVERING: Order.Status.COMPLETED,
    }
    expected_next = transitions.get(order.status)
    if not expected_next or next_status != expected_next:
        messages.error(request, "非法状态流转")
        return redirect("rider_dashboard")

    order.status = expected_next
    order.save(update_fields=["status", "updated_at"])
    if expected_next == Order.Status.COMPLETED:
        rider.status = Rider.Status.ONLINE
        rider.save(update_fields=["status"])
    messages.success(request, f"订单 #{order.id} 已更新为：{order.get_status_display()}")
    return redirect("rider_dashboard")


@login_required
@require_POST
def rider_reject_order(request, pk):
    rider = _get_current_rider(request)
    if not rider:
        messages.error(request, "当前账号未绑定骑手身份")
        return redirect("home")

    order = get_object_or_404(Order, pk=pk)
    if order.status != Order.Status.PLACED or order.rider_id is not None:
        messages.error(request, "该订单当前不可拒单")
        return redirect("rider_dashboard")

    reason = (request.POST.get("reason") or "").strip()[:120]
    if reason:
        messages.info(request, f"已跳过订单 #{order.id}（原因：{reason}）")
    else:
        messages.info(request, f"已跳过订单 #{order.id}")
    return redirect("rider_dashboard")


@login_required
@require_POST
def rider_report_issue(request, pk):
    rider = _get_current_rider(request)
    if not rider:
        messages.error(request, "当前账号未绑定骑手身份")
        return redirect("home")

    order = get_object_or_404(Order, pk=pk, rider=rider)
    issue_note = (request.POST.get("issue_note") or "").strip()
    if not issue_note:
        messages.error(request, "请填写异常说明")
        return redirect("rider_dashboard")

    order.rider_note = issue_note[:200]
    order.save(update_fields=["rider_note", "updated_at"])
    messages.warning(request, f"订单 #{order.id} 异常已上报")
    return redirect("rider_dashboard")


def shop_detail(request, pk):
    shop = get_object_or_404(
        Shop.objects.prefetch_related(
            Prefetch(
                "categories",
                queryset=Category.objects.order_by("sort_order", "id").prefetch_related(
                    Prefetch("dishes", queryset=Dish.objects.filter(is_available=True))
                ),
            )
        ),
        pk=pk,
    )
    cart = get_cart(request)
    cart_lines = {}
    if cart["shop_id"] == shop.id:
        cart_lines = cart["lines"]

    dish_rows = []
    for cat in shop.categories.all():
        for dish in cat.dishes.all():
            qty = cart_lines.get(str(dish.id), 0)
            line_total = dish.price * qty if qty else Decimal("0")
            dish_rows.append(
                {"category": cat.name, "dish": dish, "qty": qty, "line_total": line_total}
            )

    subtotal = Decimal("0")
    for row in dish_rows:
        if row["qty"]:
            subtotal += row["dish"].price * row["qty"]
    delivery = shop.delivery_fee if cart_lines else Decimal("0")
    total_preview = subtotal + delivery if cart_lines else Decimal("0")

    return render(
        request,
        "food_delivery/shop_detail.html",
        {
            "shop": shop,
            "dish_rows": dish_rows,
            "cart_lines": cart_lines,
            "subtotal": subtotal,
            "total_preview": total_preview,
            "has_cart": bool(cart_lines),
        },
    )


@require_POST
def cart_add(request, pk):
    get_object_or_404(Shop, pk=pk)
    dish_id = int(request.POST.get("dish_id", 0))
    dish = get_object_or_404(Dish, pk=dish_id, category__shop_id=pk, is_available=True)
    add_line(request, pk, dish.id, 1)
    messages.success(request, f"已加入：{dish.name}")
    return redirect("shop_detail", pk=pk)


@require_POST
def cart_update(request, pk):
    get_object_or_404(Shop, pk=pk)
    dish_id = int(request.POST.get("dish_id", 0))
    qty = int(request.POST.get("quantity", 0))
    get_object_or_404(Dish, pk=dish_id, category__shop_id=pk)
    set_line_qty(request, pk, dish_id, qty)
    return redirect("shop_detail", pk=pk)


@require_POST
def cart_clear(request, pk):
    get_object_or_404(Shop, pk=pk)
    cart = get_cart(request)
    if cart["shop_id"] == pk:
        clear_cart(request)
        messages.info(request, "已清空购物车")
    return redirect("shop_detail", pk=pk)


@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart["lines"] or cart["shop_id"] is None:
        messages.warning(request, "购物车是空的")
        return redirect("shop_list")

    shop = get_object_or_404(Shop, pk=cart["shop_id"], is_open=True)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order, err = create_order_from_lines(
                request.user,
                shop,
                cart["lines"],
                form.cleaned_data["contact_phone"],
                form.cleaned_data["delivery_address"],
                form.cleaned_data.get("remark") or "",
            )
            if err:
                messages.error(request, err)
            else:
                clear_cart(request)
                messages.success(request, "下单成功！")
                return redirect("order_detail", pk=order.pk)
    else:
        form = CheckoutForm()

    lines_display = []
    subtotal = Decimal("0")
    for did, qty in cart["lines"].items():
        dish = Dish.objects.filter(pk=int(did), category__shop=shop).first()
        if not dish:
            continue
        line_sub = dish.price * qty
        subtotal += line_sub
        lines_display.append({"dish": dish, "qty": qty, "subtotal": line_sub})

    return render(
        request,
        "food_delivery/checkout.html",
        {
            "shop": shop,
            "form": form,
            "lines_display": lines_display,
            "subtotal": subtotal,
            "delivery_fee": shop.delivery_fee,
            "total": subtotal + shop.delivery_fee,
        },
    )


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get("next") or ""
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect("home")
    else:
        form = LoginForm()
    return render(request, "food_delivery/login.html", {"form": form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "注册成功，欢迎点餐")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "food_delivery/register.html", {"form": form})


@require_POST
def user_logout(request):
    logout(request)
    messages.info(request, "已退出登录")
    return redirect("home")


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).select_related("shop").prefetch_related("items")[:50]
    return render(request, "food_delivery/my_orders.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related("items"),
        pk=pk,
        user=request.user,
    )
    return render(request, "food_delivery/order_detail.html", {"order": order})


@login_required
@require_POST
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status in (Order.Status.COMPLETED, Order.Status.CANCELLED):
        messages.error(request, "当前状态不可取消")
    elif order.status not in (Order.Status.PLACED, Order.Status.ACCEPTED):
        messages.error(request, "商家已备餐或配送中，请联系店铺")
    else:
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        messages.success(request, "订单已取消")
    return redirect("order_detail", pk=pk)
