# 鲜达外卖 · 小型订单系统（升级版）

基于 **Django 5** 与 **Django REST Framework** 的外卖订单演示项目：包含用户端网页（点餐、购物车、结算、订单）、REST API，以及 Django 管理后台。默认使用 **SQLite**，适合学习与本地演示。

本版本已完成一轮前端升级：采用更偏 **Apple 风格** 的视觉方向（大图背景、玻璃态层次、细腻动效），并新增平台成熟化模块（优惠专区、会员计划、帮助中心）。

## 功能概览

### 用户端网站

- 首页（升级版 Hero + 高级视觉风格）
- 餐厅列表 / 餐厅详情 / 菜单浏览
- Session 购物车（加购、改数量、清空）
- 登录 / 注册
- 结算下单
- 我的订单 / 订单详情 / 订单取消（按状态限制）

### 新增模块（本次升级）

- **优惠专区**（`/deals/`）
  - 活动卡片展示
  - 可快速跳转到门店选购
- **会员计划**（`/membership/`）
  - Silver / Gold / Platinum 分层权益展示
- **帮助中心**（`/help-center/`）
  - FAQ 折叠面板，覆盖配送、退款、发票等常见问题

### REST API

- 注册 / 登录（Token）
- 店铺与菜品查询
- 订单相关 CRUD 接口（供移动端或第三方调用）

### 管理后台

- 维护店铺、分类、菜品与订单状态

---

## 环境要求

- Python **3.10+**（推荐 3.12）
- Windows / macOS / Linux

## 依赖

见 `requirements.txt`：

- Django 5.x
- djangorestframework 3.x

安装：

```bash
python -m pip install -r requirements.txt
```

---

## 快速开始

### 1) 数据库迁移

在项目根目录（与 `manage.py` 同级）执行：

```bash
python manage.py migrate
```

### 2) 初始化演示数据（可选）

```bash
python manage.py seed_demo
```

会创建一组更完整的演示数据：

- **10 家热门餐厅**（新增汉堡、墨西哥、法式烘焙、烤鱼等风格）
- 每家店包含多分类菜品（主食 / 小吃 / 饮品等）
- 菜品总量显著增加，命名与描述尽量不重样，方便你直接演示“丰富菜单 + 多店铺”场景

### 3) 创建管理员（可选）

```bash
python manage.py createsuperuser
```

用于登录 `/admin/` 管理数据。

### 4) 启动开发服务器

```bash
python manage.py runserver
```

浏览器访问：**http://127.0.0.1:8000/**

### Windows 一键脚本

在项目根目录双击 **`run.bat`**，或在命令提示符中执行：

```bat
cd /d D:\path\to\food_delivery
run.bat
```

脚本会安装依赖、迁移、写入演示数据并启动服务。

---

## 常用地址

| 说明 | URL |
|------|-----|
| 用户端首页 | http://127.0.0.1:8000/ |
| 餐厅列表 | http://127.0.0.1:8000/shops/ |
| 优惠专区（新增） | http://127.0.0.1:8000/deals/ |
| 会员计划（新增） | http://127.0.0.1:8000/membership/ |
| 帮助中心（新增） | http://127.0.0.1:8000/help-center/ |
| README（网页版） | http://127.0.0.1:8000/readme/ |
| API 说明（简易页） | http://127.0.0.1:8000/dev/ |
| 管理后台 | http://127.0.0.1:8000/admin/ |
| 店铺 API（JSON） | http://127.0.0.1:8000/api/shops/ |

---

## API 简要说明

- `POST /api/auth/register/` — 注册，Body：`username`、`password`
- `POST /api/auth/login/` — 登录，返回 `token`
- 需认证接口在 Header 中携带：`Authorization: Token <token>`
- `GET /api/shops/`、`GET /api/shops/<id>/` — 店铺
- `GET` / `POST /api/orders/` — 订单列表与创建（详见 `orders` 应用内序列化字段）

---

## 项目结构（主要部分）

```text
food_delivery/                 # 项目包
  settings.py                  # 配置（含模板路径、静态文件、登录 URL 等）
  urls.py                      # 总路由（页面 + admin + api）
  views.py                     # 用户端页面视图（含 deals/membership/help_center）
  forms.py                     # 登录、注册、结账表单
  cart_session.py              # 购物车 Session 逻辑
  order_service.py             # 从购物车生成订单
  templates/                   # HTML 模板
  static/food_delivery/css/    # 站点样式
  static/food_delivery/js/     # 站点交互脚本
orders/                        # 业务应用：模型、API、Admin、演示数据命令
manage.py
requirements.txt
run.bat                        # Windows 启动脚本
```

---

## 视觉与交互升级说明（本次）

### 风格层

- 全站统一极简玻璃拟态语言（间距、色阶、圆角、阴影、半透明层）
- 多区域背景图与卡片层次增强
- 导航扩展为：首页 / 餐厅 / 优惠专区 / 会员 / 帮助中心 / 我的订单
- 餐厅卡片封面支持按店铺自动轮换（`cover-1` ~ `cover-8`），首页 / 餐厅页 / 优惠页保持一致视觉映射

### 主页交互层（重点）

- 引入 **Tailwind CSS（CDN）** 做局部快速增强布局
- 引入 **Framer Motion（浏览器 UMD）** 做漂浮光球与动效氛围
- 增加 **滚动视差**（Hero 背景层随滚动产生景深）
- 增加 **3D 鼠标跟随倾斜**（功能卡、餐厅卡片 hover 倾斜）
- 增加 **文字流光渐变**（主标题 Shine 动效）
- 增加 **商家卡片入场弹射**（进入视口后弹性过渡）
- 增加 **图标 3D 悬浮反馈**（hover 浮起与轻旋转）
- 保留无障碍体验：兼容 `prefers-reduced-motion`

> 说明：当前背景图与前端动效资源使用在线地址（CDN/外链图），便于演示；生产环境建议替换为自有 CDN 或本地静态资源并加版本管理。

---

## 注意事项

- 当前 `SECRET_KEY`、`DEBUG` 等配置仅适合**本地开发**。
- 上线前务必：关闭 `DEBUG`、更换密钥、使用生产数据库、配置 HTTPS 与日志审计。
- 用户端购物车保存在 **Session** 中，清除浏览器 Cookie 会清空购物车。
- 生产环境静态文件需使用 `collectstatic` 并由 Web 服务器或 CDN 提供。

---

## 许可证

学习与演示用途；如需商用请自行完善安全、支付、合规与运维方案。
