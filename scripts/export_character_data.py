#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从MongoDB数据库cbg的xigua集合导出角色数据为JSON文件
用于角色估价页面数据源
"""

import json
import sys
import os
import argparse
from datetime import datetime

# 尝试导入pymongo
try:
    from pymongo import MongoClient
except ImportError:
    print("错误: 未安装pymongo库")
    print("请运行: py -m pip install pymongo")
    sys.exit(1)

def export_character_data(host="localhost", port=27017, database="cbg", collection="xigua"):
    """从MongoDB导出角色数据"""

    # MongoDB连接配置
    mongo_host = host
    mongo_port = port
    database_name = database
    collection_name = collection

    # 输出文件路径（两个位置）
    # 1. 项目根目录的assets/data（与其他数据文件一致）
    output_dir1 = os.path.join(os.path.dirname(__file__), "..", "assets", "data")
    output_file1 = os.path.join(output_dir1, "character_data.json")

    # 2. 页面目录docs/app/character（页面直接访问的位置）
    output_dir2 = os.path.join(os.path.dirname(__file__), "..", "docs", "app", "character")
    output_file2 = os.path.join(output_dir2, "character_data.json")

    # 确保输出目录存在
    os.makedirs(output_dir1, exist_ok=True)
    os.makedirs(output_dir2, exist_ok=True)

    print(f"正在连接MongoDB: {mongo_host}:{mongo_port}")
    print(f"数据库: {database_name}, 集合: {collection_name}")

    try:
        # 连接MongoDB
        client = MongoClient(mongo_host, mongo_port)

        # 检查数据库和集合是否存在
        if database_name not in client.list_database_names():
            print(f"错误: 数据库 '{database_name}' 不存在")
            print(f"可用的数据库: {client.list_database_names()}")
            return False

        db = client[database_name]

        if collection_name not in db.list_collection_names():
            print(f"错误: 集合 '{collection_name}' 不存在")
            print(f"可用的集合: {db.list_collection_names()}")
            return False

        collection = db[collection_name]

        # 获取所有文档
        documents = list(collection.find())

        print(f"找到 {len(documents)} 个文档")

        if not documents:
            print("警告: 集合为空，无法导出数据")
            return False

        # 转换文档为可序列化的格式
        # 处理MongoDB的特殊类型：_id ObjectId和datetime对象
        for doc in documents:
            for key, value in list(doc.items()):
                # 处理ObjectId
                if key == '_id':
                    doc[key] = str(value)
                # 处理datetime对象
                elif isinstance(value, datetime):
                    doc[key] = value.isoformat()
                # 处理其他可能的非JSON可序列化类型
                elif not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    doc[key] = str(value)

        # 添加元数据
        export_data = {
            "metadata": {
                "export_time": datetime.now().isoformat(),
                "source": f"mongodb://{mongo_host}:{mongo_port}/{database_name}.{collection_name}",
                "document_count": len(documents)
            },
            "data": documents
        }

        # 写入JSON文件（两个位置）
        with open(output_file1, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        with open(output_file2, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        print(f"数据已导出到两个位置:")
        print(f"  1. {output_file1}")
        print(f"  2. {output_file2}")
        print(f"文档数量: {len(documents)}")

        # 显示字段示例
        if documents:
            print("\n文档字段示例:")
            sample_doc = documents[0]
            for key, value in list(sample_doc.items())[:10]:  # 只显示前10个字段
                print(f"  {key}: {type(value).__name__}")

        return True

    except Exception as e:
        print(f"导出数据时出错: {e}")
        return False
    finally:
        if 'client' in locals():
            client.close()

def create_sample_data():
    """创建示例数据文件（用于测试）"""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "data")
    output_file = os.path.join(output_dir, "character_data_sample.json")

    sample_data = {
        "metadata": {
            "export_time": datetime.now().isoformat(),
            "source": "sample_data",
            "document_count": 5
        },
        "data": [
            {
                "level": "69",
                "type": "男天青",
                "school": "大唐官府",
                "base_price": 180000,
                "limit_item": "滑板",
                "extra_price": 500,
                "total_price": 180500,
                "notes": "满底子满机缘"
            },
            {
                "level": "69",
                "type": "女天青",
                "school": "女儿村",
                "base_price": 80000,
                "limit_item": None,
                "extra_price": None,
                "total_price": 80000,
                "notes": "无限量"
            },
            {
                "level": "109",
                "type": "男狐青",
                "school": "龙宫",
                "base_price": 63000,
                "limit_item": "天使猪",
                "extra_price": 10000,
                "total_price": 73000,
                "notes": "带天使猪"
            },
            {
                "level": "129",
                "type": "满底子/满机缘",
                "school": "化生寺",
                "base_price": 250000,
                "limit_item": "浪淘",
                "extra_price": 1000,
                "total_price": 251000,
                "notes": "辅助角色"
            },
            {
                "level": "175",
                "type": "男单青",
                "school": "狮驼岭",
                "base_price": 42000,
                "limit_item": "九尾冰狐",
                "extra_price": 6000,
                "total_price": 48000,
                "notes": "物理输出"
            }
        ]
    }

    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

    print(f"示例数据已创建: {output_file}")
    print("注意: 这是示例数据，实际使用时请从MongoDB导出真实数据")

    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="从MongoDB导出角色数据")
    parser.add_argument("--export", action="store_true", help="直接导出数据（非交互模式）")
    parser.add_argument("--host", default="localhost", help="MongoDB主机地址（默认：localhost）")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB端口（默认：27017）")
    parser.add_argument("--database", default="cbg", help="数据库名称（默认：cbg）")
    parser.add_argument("--collection", default="xigua", help="集合名称（默认：xigua）")
    parser.add_argument("--sample", action="store_true", help="创建示例数据")

    args = parser.parse_args()

    # 如果是非交互模式
    if args.export:
        print("=" * 60)
        print("从MongoDB导出角色数据")
        print("=" * 60)
        print(f"连接配置: {args.host}:{args.port}/{args.database}.{args.collection}")
        success = export_character_data(
            host=args.host,
            port=args.port,
            database=args.database,
            collection=args.collection
        )
        if success:
            print("[成功] 导出完成")
        else:
            print("[失败] 导出失败")
        return

    if args.sample:
        print("\n创建示例数据...")
        success = create_sample_data()
        if success:
            print("[成功] 示例数据创建完成")
        return

    # 交互模式
    print("=" * 60)
    print("角色数据导出工具")
    print("=" * 60)
    print("选项:")
    print("  1. 从MongoDB导出真实数据")
    print("  2. 创建示例数据（用于测试）")
    print("  3. 退出")

    try:
        choice = input("请选择 (1-3): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消")
        return

    if choice == "1":
        print("\n正在从MongoDB导出数据...")
        success = export_character_data()
        if success:
            print("[成功] 导出完成")
        else:
            print("[失败] 导出失败")
    elif choice == "2":
        print("\n创建示例数据...")
        success = create_sample_data()
        if success:
            print("[成功] 示例数据创建完成")
    elif choice == "3":
        print("退出")
    else:
        print("无效选择")

if __name__ == "__main__":
    main()