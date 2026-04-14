#!/usr/bin/env python
"""Django 管理入口。依赖安装、数据库迁移与启动方式见项目根目录 README.md。"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_delivery.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入 Django。请先执行: pip install -r requirements.txt（说明见 README.md）"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
