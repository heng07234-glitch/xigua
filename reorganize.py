#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重组项目目录结构
将文件归类到以下结构：
web/              # 前端页面
  index.html      # 首页
  ling-shi/       # 灵饰相关页面
  bao-bao/        # 宝宝相关页面
  tests/          # 测试页面
data/             # 数据文件（JS）
assets/           # 资源文件
  sources/        # 源Excel文件
  lingshi-logos/  # 灵饰图标
"""

import os
import shutil
import re
from pathlib import Path

def ensure_dir(path):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)

def move_file(src, dst, update_refs=None):
    """移动文件并可选地更新引用"""
    if not os.path.exists(src):
        print(f"警告: 源文件不存在: {src}")
        return False

    ensure_dir(os.path.dirname(dst))
    shutil.move(src, dst)
    print(f"移动: {src} -> {dst}")
    return True

def update_html_references(html_file, old_js_path, new_js_path):
    """更新HTML文件中的JS引用路径"""
    if not os.path.exists(html_file):
        return

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 更新JS引用
    updated = content.replace(f'src="{old_js_path}"', f'src="{new_js_path}"')

    if updated != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"更新引用: {html_file} ({old_js_path} -> {new_js_path})")

def update_image_references(html_file, old_img_path, new_img_path):
    """更新HTML文件中的图片引用路径"""
    if not os.path.exists(html_file):
        return

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 更新图片引用
    updated = content.replace(old_img_path, new_img_path)

    if updated != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"更新图片引用: {html_file}")

def main():
    base_dir = Path(__file__).parent
    mifangame_dir = base_dir / "mifangame-price-main"

    # 创建目录结构
    dirs = [
        "web",
        "web/ling-shi",
        "web/bao-bao",
        "web/tests",
        "data",
        "assets",
        "assets/sources",
        "assets/lingshi-logos"
    ]

    for d in dirs:
        ensure_dir(base_dir / d)

    # 文件映射：源路径 -> 目标路径
    file_mappings = [
        # 前端页面
        (mifangame_dir / "index.html", base_dir / "web" / "index.html"),
        (mifangame_dir / "lingshi_estimate.html", base_dir / "web" / "ling-shi" / "estimate.html"),
        (mifangame_dir / "baobao_estimate.html", base_dir / "web" / "bao-bao" / "estimate.html"),
        (mifangame_dir / "debug_ling_shi.html", base_dir / "web" / "ling-shi" / "debug.html"),
        (mifangame_dir / "test.html", base_dir / "web" / "tests" / "test.html"),
        (mifangame_dir / "test_data_loading.html", base_dir / "web" / "tests" / "data-loading.html"),
        (mifangame_dir / "test_icons.html", base_dir / "web" / "tests" / "icons.html"),
        (mifangame_dir / "test_lingshi_images.html", base_dir / "web" / "tests" / "lingshi-images.html"),

        # 数据文件（JS）
        (mifangame_dir / "lingshi_data.js", base_dir / "data" / "lingshi_data.js"),
        (mifangame_dir / "baobao_data.js", base_dir / "data" / "baobao_data.js"),
        (mifangame_dir / "baobao_data_v2.js", base_dir / "data" / "baobao_data_v2.js"),
        (mifangame_dir / "baobao_data_full.js", base_dir / "data" / "baobao_data_full.js"),
        (mifangame_dir / "baobao_table_data.js", base_dir / "data" / "baobao_table_data.js"),
        (mifangame_dir / "improved_rules.js", base_dir / "data" / "improved_rules.js"),
        (mifangame_dir / "rules.js", base_dir / "data" / "rules.js"),
        (mifangame_dir / "icon_mapping.js", base_dir / "data" / "icon_mapping.js"),

        # 资源文件
        (mifangame_dir / "logo.png", base_dir / "assets" / "logo.png"),
    ]

    # 移动文件
    for src, dst in file_mappings:
        if src.exists():
            move_file(str(src), str(dst))

    # 移动灵饰图标
    lingshi_logo_dir = base_dir / "灵饰logo"
    if lingshi_logo_dir.exists():
        for img_file in lingshi_logo_dir.glob("*.png"):
            dst = base_dir / "assets" / "lingshi-logos" / img_file.name
            move_file(str(img_file), str(dst))

    # 移动源Excel文件
    excel_files = [
        ("灵饰价格表.xlsx", "lingshi.xlsx"),
        ("宝宝价格表.xlsx", "baobao.xlsx"),
    ]

    for old_name, new_name in excel_files:
        src = base_dir / old_name
        if src.exists():
            dst = base_dir / "assets" / "sources" / new_name
            move_file(str(src), str(dst))

    # 更新HTML文件中的引用
    html_updates = [
        # (html文件, 旧JS路径, 新JS路径)
        (base_dir / "web" / "index.html", "improved_rules.js", "../data/improved_rules.js"),
        (base_dir / "web" / "ling-shi" / "estimate.html", "icon_mapping.js", "../../data/icon_mapping.js"),
        (base_dir / "web" / "ling-shi" / "estimate.html", "lingshi_data.js", "../../data/lingshi_data.js"),
        (base_dir / "web" / "bao-bao" / "estimate.html", "baobao_table_data.js", "../../data/baobao_table_data.js"),
        (base_dir / "web" / "ling-shi" / "debug.html", "improved_rules.js", "../../data/improved_rules.js"),
        (base_dir / "web" / "tests" / "test.html", "rules.js", "../../data/rules.js"),
        (base_dir / "web" / "tests" / "data-loading.html", "icon_mapping.js", "../../data/icon_mapping.js"),
        (base_dir / "web" / "tests" / "data-loading.html", "lingshi_data.js", "../../data/lingshi_data.js"),
        (base_dir / "web" / "tests" / "data-loading.html", "improved_rules.js", "../../data/improved_rules.js"),
        (base_dir / "web" / "tests" / "icons.html", "icon_mapping.js", "../../data/icon_mapping.js"),
    ]

    for html_file, old_js, new_js in html_updates:
        update_html_references(str(html_file), old_js, new_js)

    # 更新灵饰估价页面中的图片路径
    lingshi_estimate = base_dir / "web" / "ling-shi" / "estimate.html"
    if lingshi_estimate.exists():
        with open(lingshi_estimate, 'r', encoding='utf-8') as f:
            content = f.read()

        # 更新图片路径：../灵饰logo/ -> ../../assets/lingshi-logos/
        updated = content.replace('../灵饰logo/', '../../assets/lingshi-logos/')

        if updated != content:
            with open(lingshi_estimate, 'w', encoding='utf-8') as f:
                f.write(updated)
            print(f"更新灵饰图片路径: {lingshi_estimate}")

    # 更新index.html中的页面链接
    index_file = base_dir / "web" / "index.html"
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 更新链接
        updated = content.replace('lingshi_estimate.html', 'ling-shi/estimate.html')
        updated = updated.replace('baobao_estimate.html', 'bao-bao/estimate.html')

        if updated != content:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(updated)
            print(f"更新首页链接: {index_file}")

    # 更新Python脚本中的Excel文件路径
    scripts_dir = base_dir / "scripts"
    if scripts_dir.exists():
        for script_file in scripts_dir.glob("*.py"):
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 更新Excel路径
            updated = content.replace(r'E:\\gujia\\灵饰价格表.xlsx', str(base_dir / 'assets' / 'sources' / 'lingshi.xlsx'))
            updated = updated.replace(r'E:\gujia\灵饰价格表.xlsx', str(base_dir / 'assets' / 'sources' / 'lingshi.xlsx'))
            updated = updated.replace('灵饰价格表.xlsx', str(base_dir / 'assets' / 'sources' / 'lingshi.xlsx'))

            updated = updated.replace(r'E:\\gujia\\宝宝价格表.xlsx', str(base_dir / 'assets' / 'sources' / 'baobao.xlsx'))
            updated = updated.replace(r'E:\gujia\宝宝价格表.xlsx', str(base_dir / 'assets' / 'sources' / 'baobao.xlsx'))
            updated = updated.replace('宝宝价格表.xlsx', str(base_dir / 'assets' / 'sources' / 'baobao.xlsx'))

            if updated != content:
                with open(script_file, 'w', encoding='utf-8') as f:
                    f.write(updated)
                print(f"更新脚本Excel路径: {script_file}")

    # 更新批处理文件
    bat_file = base_dir / "convert_lingshi.bat"
    if bat_file.exists():
        with open(bat_file, 'r', encoding='utf-8') as f:
            content = f.read()

        updated = content.replace('E:\\gujia\\灵饰价格表.xlsx', str(base_dir / 'assets' / 'sources' / 'lingshi.xlsx'))
        updated = updated.replace('E:\\Users\\Administrator\\Desktop\\灵饰价格表.xlsx', str(base_dir / 'assets' / 'sources' / 'lingshi.xlsx'))

        if updated != content:
            with open(bat_file, 'w', encoding='utf-8') as f:
                f.write(updated)
            print(f"更新批处理文件: {bat_file}")

    print("\n重组完成！")
    print("新目录结构：")
    print("  web/ - 前端页面")
    print("  data/ - 数据文件")
    print("  assets/ - 资源文件")
    print("  scripts/ - Python脚本")
    print("  docs/ - 文档")

if __name__ == "__main__":
    main()