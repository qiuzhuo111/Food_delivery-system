from decimal import Decimal

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="latitude",
            field=models.DecimalField(decimal_places=6, default=Decimal("31.230400"), max_digits=9, verbose_name="纬度"),
        ),
        migrations.AddField(
            model_name="shop",
            name="longitude",
            field=models.DecimalField(decimal_places=6, default=Decimal("121.473700"), max_digits=9, verbose_name="经度"),
        ),
        migrations.CreateModel(
            name="Rider",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, verbose_name="骑手姓名")),
                ("phone", models.CharField(blank=True, max_length=32, verbose_name="联系电话")),
                (
                    "status",
                    models.CharField(
                        choices=[("online", "在线"), ("delivering", "配送中"), ("offline", "离线")],
                        default="online",
                        max_length=20,
                        verbose_name="状态",
                    ),
                ),
                ("vehicle", models.CharField(default="电动车", max_length=50, verbose_name="交通工具")),
                ("rating", models.DecimalField(decimal_places=1, default=Decimal("4.8"), max_digits=3, verbose_name="评分")),
                (
                    "current_latitude",
                    models.DecimalField(decimal_places=6, default=Decimal("31.225000"), max_digits=9, verbose_name="当前位置纬度"),
                ),
                (
                    "current_longitude",
                    models.DecimalField(decimal_places=6, default=Decimal("121.480000"), max_digits=9, verbose_name="当前位置经度"),
                ),
            ],
            options={
                "verbose_name": "骑手",
                "verbose_name_plural": "骑手",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="rider",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="orders.rider",
                verbose_name="骑手",
            ),
        ),
    ]
