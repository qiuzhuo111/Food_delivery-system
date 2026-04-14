import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Shop",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="店铺名称")),
                ("address", models.CharField(blank=True, max_length=255, verbose_name="地址")),
                ("phone", models.CharField(blank=True, max_length=32, verbose_name="电话")),
                ("is_open", models.BooleanField(default=True, verbose_name="营业中")),
                (
                    "delivery_fee",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("5.00"),
                        max_digits=8,
                        verbose_name="配送费",
                    ),
                ),
            ],
            options={
                "verbose_name": "店铺",
                "verbose_name_plural": "店铺",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, verbose_name="分类名")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="排序")),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="categories",
                        to="orders.shop",
                        verbose_name="店铺",
                    ),
                ),
            ],
            options={
                "verbose_name": "菜品分类",
                "verbose_name_plural": "菜品分类",
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="Dish",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="菜品名")),
                ("price", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="单价")),
                ("description", models.TextField(blank=True, verbose_name="描述")),
                ("is_available", models.BooleanField(default=True, verbose_name="可售")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dishes",
                        to="orders.category",
                        verbose_name="分类",
                    ),
                ),
            ],
            options={
                "verbose_name": "菜品",
                "verbose_name_plural": "菜品",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("placed", "待接单"),
                            ("accepted", "已接单"),
                            ("preparing", "备餐中"),
                            ("delivering", "配送中"),
                            ("completed", "已完成"),
                            ("cancelled", "已取消"),
                        ],
                        default="placed",
                        max_length=20,
                        verbose_name="状态",
                    ),
                ),
                ("delivery_fee", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="配送费")),
                ("items_total", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="商品小计")),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="应付总额")),
                ("contact_phone", models.CharField(max_length=32, verbose_name="联系电话")),
                ("delivery_address", models.CharField(max_length=255, verbose_name="配送地址")),
                ("remark", models.CharField(blank=True, max_length=200, verbose_name="备注")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="下单时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="orders",
                        to="orders.shop",
                        verbose_name="店铺",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单",
                "verbose_name_plural": "订单",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("dish_name", models.CharField(max_length=100, verbose_name="菜品名称快照")),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="单价快照")),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="数量",
                    ),
                ),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="小计")),
                (
                    "dish",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="orders.dish",
                        verbose_name="菜品",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="orders.order",
                        verbose_name="订单",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单明细",
                "verbose_name_plural": "订单明细",
            },
        ),
    ]
