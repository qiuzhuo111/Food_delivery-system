from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Shop(models.Model):
    name = models.CharField("店铺名称", max_length=100)
    address = models.CharField("地址", max_length=255, blank=True)
    phone = models.CharField("电话", max_length=32, blank=True)
    is_open = models.BooleanField("营业中", default=True)
    delivery_fee = models.DecimalField(
        "配送费",
        max_digits=8,
        decimal_places=2,
        default=Decimal("5.00"),
    )
    latitude = models.DecimalField("纬度", max_digits=9, decimal_places=6, default=Decimal("31.230400"))
    longitude = models.DecimalField("经度", max_digits=9, decimal_places=6, default=Decimal("121.473700"))

    class Meta:
        verbose_name = "店铺"
        verbose_name_plural = "店铺"

    def __str__(self):
        return self.name


class Category(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="店铺",
    )
    name = models.CharField("分类名", max_length=50)
    sort_order = models.PositiveSmallIntegerField("排序", default=0)

    class Meta:
        verbose_name = "菜品分类"
        verbose_name_plural = "菜品分类"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.shop.name} · {self.name}"


class Dish(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="dishes",
        verbose_name="分类",
    )
    name = models.CharField("菜品名", max_length=100)
    price = models.DecimalField("单价", max_digits=8, decimal_places=2)
    description = models.TextField("描述", blank=True)
    is_available = models.BooleanField("可售", default=True)

    class Meta:
        verbose_name = "菜品"
        verbose_name_plural = "菜品"

    def __str__(self):
        return self.name

    @property
    def shop(self):
        return self.category.shop


class Rider(models.Model):
    class Status(models.TextChoices):
        ONLINE = "online", "在线"
        DELIVERING = "delivering", "配送中"
        OFFLINE = "offline", "离线"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rider_profile",
        verbose_name="绑定账号",
    )
    name = models.CharField("骑手姓名", max_length=50)
    phone = models.CharField("联系电话", max_length=32, blank=True)
    status = models.CharField("状态", max_length=20, choices=Status.choices, default=Status.ONLINE)
    vehicle = models.CharField("交通工具", max_length=50, default="电动车")
    rating = models.DecimalField("评分", max_digits=3, decimal_places=1, default=Decimal("4.8"))
    current_latitude = models.DecimalField("当前位置纬度", max_digits=9, decimal_places=6, default=Decimal("31.225000"))
    current_longitude = models.DecimalField("当前位置经度", max_digits=9, decimal_places=6, default=Decimal("121.480000"))

    class Meta:
        verbose_name = "骑手"
        verbose_name_plural = "骑手"

    def __str__(self):
        return f"{self.name}（{self.get_status_display()}）"


class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = "placed", "待接单"
        ACCEPTED = "accepted", "已接单"
        PREPARING = "preparing", "备餐中"
        DELIVERING = "delivering", "配送中"
        COMPLETED = "completed", "已完成"
        CANCELLED = "cancelled", "已取消"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="用户",
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="店铺",
    )
    rider = models.ForeignKey(
        Rider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="骑手",
    )
    status = models.CharField(
        "状态",
        max_length=20,
        choices=Status.choices,
        default=Status.PLACED,
    )
    delivery_fee = models.DecimalField("配送费", max_digits=8, decimal_places=2)
    items_total = models.DecimalField("商品小计", max_digits=10, decimal_places=2)
    total_amount = models.DecimalField("应付总额", max_digits=10, decimal_places=2)
    contact_phone = models.CharField("联系电话", max_length=32)
    delivery_address = models.CharField("配送地址", max_length=255)
    remark = models.CharField("备注", max_length=200, blank=True)
    rider_note = models.CharField("骑手备注", max_length=200, blank=True)
    created_at = models.DateTimeField("下单时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"
        ordering = ["-created_at"]

    def __str__(self):
        return f"订单#{self.pk} {self.shop.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="订单",
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="菜品",
    )
    dish_name = models.CharField("菜品名称快照", max_length=100)
    unit_price = models.DecimalField("单价快照", max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField("数量", validators=[MinValueValidator(1)])
    subtotal = models.DecimalField("小计", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "订单明细"
        verbose_name_plural = "订单明细"

    def __str__(self):
        return f"{self.dish_name} x{self.quantity}"
