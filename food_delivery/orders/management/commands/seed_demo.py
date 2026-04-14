from decimal import Decimal

from django.core.management.base import BaseCommand

from orders.models import Category, Dish, Rider, Shop


class Command(BaseCommand):
    help = "写入演示店铺、分类、菜品与骑手（可重复执行，按名称去重）"

    def handle(self, *args, **options):
        shops_payload = [
            {
                "name": "小巷快餐",
                "address": "示例路 1 号",
                "phone": "13800138000",
                "delivery_fee": Decimal("5.00"),
                "latitude": Decimal("31.231200"),
                "longitude": Decimal("121.472100"),
                "categories": [
                    ("招牌主食", [
                        ("黑椒牛柳盖饭", Decimal("24.00"), "厚切牛柳、洋葱与黄油黑椒酱汁"),
                        ("台式卤肉饭", Decimal("19.00"), "慢炖卤肉与溏心蛋组合"),
                        ("番茄鸡排蛋包饭", Decimal("22.00"), "酸甜番茄汁搭配嫩滑蛋包"),
                        ("香菇滑鸡煲仔饭", Decimal("23.00"), "现煲米饭与鲜香滑鸡"),
                    ]),
                    ("小食", [
                        ("蒜香鸡米花", Decimal("14.00"), "外酥里嫩，附甜辣酱"),
                        ("脆薯双拼", Decimal("13.00"), "细薯+粗薯双重口感"),
                    ]),
                    ("饮品", [
                        ("冰豆浆", Decimal("6.00"), "现磨黄豆，微甜"),
                        ("柠檬气泡水", Decimal("9.00"), "鲜切柠檬与苏打气泡"),
                    ]),
                ],
            },
            {
                "name": "云顶轻食碗",
                "address": "星河大道 66 号",
                "phone": "13800138001",
                "delivery_fee": Decimal("4.00"),
                "latitude": Decimal("31.226800"),
                "longitude": Decimal("121.481600"),
                "categories": [
                    ("能量碗", [
                        ("牛油果藜麦鸡胸碗", Decimal("32.00"), "低脂鸡胸、藜麦与牛油果丁"),
                        ("三文鱼糙米能量碗", Decimal("38.00"), "轻煎三文鱼配糙米饭"),
                        ("照烧豆腐素食碗", Decimal("28.00"), "照烧豆腐、玉米粒与紫甘蓝"),
                    ]),
                    ("沙拉", [
                        ("凯撒虾仁沙拉", Decimal("29.00"), "蒜香虾仁搭配凯撒酱"),
                        ("地中海鹰嘴豆沙拉", Decimal("26.00"), "橄榄油与香草风味"),
                    ]),
                    ("鲜榨饮品", [
                        ("羽衣甘蓝苹果汁", Decimal("16.00"), "冷压鲜榨，无额外加糖"),
                        ("莓果酸奶昔", Decimal("18.00"), "蓝莓草莓与酸奶融合"),
                    ]),
                ],
            },
            {
                "name": "渔港寿司屋",
                "address": "临海路 18 号",
                "phone": "13800138002",
                "delivery_fee": Decimal("6.00"),
                "latitude": Decimal("31.239900"),
                "longitude": Decimal("121.489100"),
                "categories": [
                    ("握寿司", [
                        ("炙烤三文鱼握", Decimal("26.00"), "焦香炙烤与特调酱汁"),
                        ("甜虾握寿司", Decimal("24.00"), "北极甜虾，口感清甜"),
                        ("鳗鱼握寿司", Decimal("28.00"), "蒲烧鳗鱼搭配海苔碎"),
                    ]),
                    ("卷物", [
                        ("火炙鳗鱼卷", Decimal("30.00"), "鳗鱼、黄瓜与日式蛋卷"),
                        ("加州蟹柳卷", Decimal("22.00"), "蟹柳、牛油果与飞鱼籽"),
                        ("辣金枪鱼卷", Decimal("25.00"), "微辣口感，层次丰富"),
                    ]),
                    ("汤与小食", [
                        ("味噌豆腐汤", Decimal("12.00"), "柴鱼高汤与嫩豆腐"),
                        ("日式炸鸡块", Decimal("16.00"), "姜蒜腌制，外脆内嫩"),
                    ]),
                ],
            },
            {
                "name": "川渝热浪",
                "address": "红椒街 9 号",
                "phone": "13800138003",
                "delivery_fee": Decimal("5.00"),
                "latitude": Decimal("31.221700"),
                "longitude": Decimal("121.468800"),
                "categories": [
                    ("川味主菜", [
                        ("藤椒牛肉饭", Decimal("27.00"), "青花椒香气与嫩牛肉"),
                        ("鱼香肉丝盖饭", Decimal("21.00"), "酸甜微辣，经典下饭"),
                        ("宫保鸡丁盖饭", Decimal("23.00"), "花生酥香与鸡丁爆炒"),
                    ]),
                    ("麻辣小吃", [
                        ("红油抄手", Decimal("17.00"), "手工抄手，麻辣鲜香"),
                        ("椒香土豆片", Decimal("12.00"), "薄切土豆，干香入味"),
                    ]),
                    ("解辣饮品", [
                        ("冰镇酸梅汤", Decimal("8.00"), "古法熬制，酸甜解腻"),
                        ("茉莉绿茶", Decimal("7.00"), "清新回甘"),
                    ]),
                ],
            },
            {
                "name": "意面星球",
                "address": "中央广场 B1-22",
                "phone": "13800138004",
                "delivery_fee": Decimal("6.00"),
                "latitude": Decimal("31.218300"),
                "longitude": Decimal("121.476200"),
                "categories": [
                    ("经典意面", [
                        ("奶油培根意面", Decimal("29.00"), "奶香浓郁，培根咸香"),
                        ("番茄海鲜意面", Decimal("33.00"), "鲜虾青口搭配番茄酱"),
                        ("蒜香橄榄油意面", Decimal("24.00"), "清爽蒜香，口感轻盈"),
                    ]),
                    ("焗饭", [
                        ("芝士鸡肉焗饭", Decimal("31.00"), "双层芝士拉丝"),
                        ("南瓜牛肉焗饭", Decimal("32.00"), "南瓜泥浓香顺滑"),
                    ]),
                    ("甜品饮品", [
                        ("提拉米苏杯", Decimal("15.00"), "马斯卡彭芝士层次丰富"),
                        ("青柠苏打", Decimal("10.00"), "微气泡清爽口感"),
                    ]),
                ],
            },
            {
                "name": "岭南点心坊",
                "address": "金穗路 88 号",
                "phone": "13800138005",
                "delivery_fee": Decimal("4.50"),
                "latitude": Decimal("31.235100"),
                "longitude": Decimal("121.461500"),
                "categories": [
                    ("蒸点", [
                        ("虾皇烧麦", Decimal("20.00"), "整只虾仁，口感弹牙"),
                        ("豉汁凤爪", Decimal("18.00"), "软糯脱骨，酱香浓郁"),
                        ("流沙奶黄包", Decimal("16.00"), "咸甜流心"),
                    ]),
                    ("肠粉粥品", [
                        ("鲜虾肠粉", Decimal("19.00"), "粉皮嫩滑"),
                        ("瑶柱瘦肉粥", Decimal("17.00"), "慢熬绵密米香"),
                    ]),
                    ("广式饮品", [
                        ("椰香马蹄露", Decimal("11.00"), "清甜爽口"),
                        ("冻柠茶", Decimal("9.00"), "茶香浓郁，酸甜平衡"),
                    ]),
                ],
            },
            {
                "name": "北境汉堡实验室",
                "address": "天际路 35 号",
                "phone": "13800138006",
                "delivery_fee": Decimal("5.50"),
                "latitude": Decimal("31.229500"),
                "longitude": Decimal("121.496400"),
                "categories": [
                    ("招牌汉堡", [
                        ("黑松露和牛堡", Decimal("39.00"), "和牛肉饼搭配黑松露蛋黄酱"),
                        ("烟熏培根双层堡", Decimal("34.00"), "双层牛肉与苹果木烟熏培根"),
                        ("香辣脆鸡菠萝堡", Decimal("28.00"), "酸甜菠萝与微辣脆鸡"),
                    ]),
                    ("炸物拼盘", [
                        ("芝士熔岩薯角", Decimal("18.00"), "薯角淋芝士酱与培根碎"),
                        ("洋葱圈风暴", Decimal("15.00"), "酥脆洋葱圈配蒜香蘸酱"),
                    ]),
                    ("奶昔特调", [
                        ("海盐焦糖奶昔", Decimal("14.00"), "海盐焦糖与香草冰淇淋"),
                        ("可可花生奶昔", Decimal("15.00"), "黑巧可可与花生酱风味"),
                    ]),
                ],
            },
            {
                "name": "墨西哥卷饼站",
                "address": "霓虹里 21 号",
                "phone": "13800138007",
                "delivery_fee": Decimal("5.00"),
                "latitude": Decimal("31.214900"),
                "longitude": Decimal("121.487300"),
                "categories": [
                    ("卷饼", [
                        ("牛肉墨西哥卷", Decimal("30.00"), "慢炖牛肉配莎莎酱"),
                        ("鸡肉芝士卷", Decimal("27.00"), "烤鸡腿肉与车打芝士"),
                        ("素食豆泥卷", Decimal("24.00"), "黑豆泥与彩椒洋葱"),
                    ]),
                    ("塔可", [
                        ("脆壳鳕鱼塔可", Decimal("23.00"), "香煎鳕鱼配青柠酸奶"),
                        ("辣味猪肉塔可", Decimal("22.00"), "香辣猪肉碎与玉米饼"),
                    ]),
                    ("配菜饮品", [
                        ("牛油果玉米片", Decimal("16.00"), "现做鳄梨酱搭配玉米片"),
                        ("西柚莫吉托气泡", Decimal("11.00"), "西柚与薄荷风味"),
                    ]),
                ],
            },
            {
                "name": "巴黎可颂厨房",
                "address": "梧桐大道 52 号",
                "phone": "13800138008",
                "delivery_fee": Decimal("4.00"),
                "latitude": Decimal("31.243800"),
                "longitude": Decimal("121.474500"),
                "categories": [
                    ("咸口可颂", [
                        ("火腿芝士可颂", Decimal("21.00"), "法式黄油可颂夹火腿芝士"),
                        ("烟熏三文鱼可颂", Decimal("25.00"), "奶油奶酪与烟熏三文鱼"),
                        ("蘑菇菠菜可颂", Decimal("20.00"), "黄油蘑菇与嫩菠菜"),
                    ]),
                    ("甜点", [
                        ("焦糖布蕾可颂卷", Decimal("19.00"), "外层焦糖脆壳"),
                        ("莓果开心果挞", Decimal("18.00"), "清新莓果与开心果碎"),
                    ]),
                    ("咖啡茶饮", [
                        ("榛果拿铁", Decimal("13.00"), "意式浓缩与榛果香气"),
                        ("伯爵奶茶", Decimal("12.00"), "伯爵茶底与牛乳融合"),
                    ]),
                ],
            },
            {
                "name": "海盐烤鱼工坊",
                "address": "港湾东路 7 号",
                "phone": "13800138009",
                "delivery_fee": Decimal("6.50"),
                "latitude": Decimal("31.247000"),
                "longitude": Decimal("121.462900"),
                "categories": [
                    ("招牌烤鱼", [
                        ("青花椒烤鲈鱼", Decimal("58.00"), "现烤鲈鱼配青花椒汤底"),
                        ("蒜蓉香辣烤鱼", Decimal("55.00"), "蒜蓉与干辣椒复合香气"),
                        ("番茄酸汤烤鱼", Decimal("56.00"), "番茄酸汤清爽开胃"),
                    ]),
                    ("配菜加料", [
                        ("手擀宽粉", Decimal("8.00"), "吸附汤汁口感劲道"),
                        ("炸豆皮卷", Decimal("9.00"), "豆香浓郁，越煮越入味"),
                    ]),
                    ("解腻饮料", [
                        ("青梅冰茶", Decimal("10.00"), "青梅与红茶复配"),
                        ("山楂乌梅饮", Decimal("9.00"), "酸甜平衡，适合重口味"),
                    ]),
                ],
            },
        ]

        riders_payload = [
            {
                "name": "王强",
                "phone": "13900139001",
                "status": Rider.Status.DELIVERING,
                "vehicle": "电动车",
                "rating": Decimal("4.9"),
                "current_latitude": Decimal("31.229800"),
                "current_longitude": Decimal("121.478900"),
            },
            {
                "name": "李娜",
                "phone": "13900139002",
                "status": Rider.Status.ONLINE,
                "vehicle": "摩托车",
                "rating": Decimal("4.8"),
                "current_latitude": Decimal("31.224600"),
                "current_longitude": Decimal("121.469700"),
            },
            {
                "name": "赵峰",
                "phone": "13900139003",
                "status": Rider.Status.ONLINE,
                "vehicle": "电动车",
                "rating": Decimal("4.7"),
                "current_latitude": Decimal("31.236500"),
                "current_longitude": Decimal("121.486200"),
            },
            {
                "name": "陈琳",
                "phone": "13900139004",
                "status": Rider.Status.OFFLINE,
                "vehicle": "电动车",
                "rating": Decimal("4.9"),
                "current_latitude": Decimal("31.241100"),
                "current_longitude": Decimal("121.472300"),
            },
        ]

        created_shops = 0
        for shop_data in shops_payload:
            categories = shop_data.pop("categories")
            shop, created = Shop.objects.get_or_create(
                name=shop_data["name"],
                defaults={
                    "address": shop_data["address"],
                    "phone": shop_data["phone"],
                    "is_open": True,
                    "delivery_fee": shop_data["delivery_fee"],
                    "latitude": shop_data["latitude"],
                    "longitude": shop_data["longitude"],
                },
            )
            if not created:
                needs_update = False
                for field in ("address", "phone", "delivery_fee", "latitude", "longitude"):
                    incoming = shop_data[field]
                    if getattr(shop, field) != incoming:
                        setattr(shop, field, incoming)
                        needs_update = True
                if not shop.is_open:
                    shop.is_open = True
                    needs_update = True
                if needs_update:
                    shop.save(
                        update_fields=[
                            "address",
                            "phone",
                            "delivery_fee",
                            "latitude",
                            "longitude",
                            "is_open",
                        ]
                    )
            else:
                created_shops += 1

            for idx, (cat_name, dishes) in enumerate(categories, start=1):
                cat, _ = Category.objects.get_or_create(
                    shop=shop,
                    name=cat_name,
                    defaults={"sort_order": idx},
                )

                for dish_name, dish_price, dish_desc in dishes:
                    Dish.objects.get_or_create(
                        category=cat,
                        name=dish_name,
                        defaults={
                            "price": dish_price,
                            "description": dish_desc,
                            "is_available": True,
                        },
                    )

        created_riders = 0
        for rider_data in riders_payload:
            rider, created = Rider.objects.get_or_create(
                name=rider_data["name"],
                defaults=rider_data,
            )
            if created:
                created_riders += 1
            else:
                needs_update = False
                for field in (
                    "phone",
                    "status",
                    "vehicle",
                    "rating",
                    "current_latitude",
                    "current_longitude",
                ):
                    incoming = rider_data[field]
                    if getattr(rider, field) != incoming:
                        setattr(rider, field, incoming)
                        needs_update = True
                if needs_update:
                    rider.save(
                        update_fields=[
                            "phone",
                            "status",
                            "vehicle",
                            "rating",
                            "current_latitude",
                            "current_longitude",
                        ]
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"演示数据就绪：共 {len(shops_payload)} 家店铺（本次新建 {created_shops} 家），"
                f"共 {len(riders_payload)} 位骑手（本次新建 {created_riders} 位）"
            )
        )
