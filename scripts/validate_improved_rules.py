#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json

with open('../assets/data/improved_rules.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取IMPROVED_RULES对象
match = re.search(r'const IMPROVED_RULES = (\{.*?\});\s*// 智能价格解析函数', content, re.DOTALL)
if not match:
    print("未找到IMPROVED_RULES定义")
    exit(1)

json_str = match.group(1)
# 修复JSON
json_str = json_str.replace('NaN', 'null')
json_str = json_str.replace('Infinity', 'null')
# 修复未加引号的键名（但我们的键名都已经有引号了）

try:
    data = json.loads(json_str)
    print("JSON语法正确！")
    print(f"包含的键: {list(data.keys())}")
    if 'ling_shi' in data:
        print(f"ling_shi类型: {type(data['ling_shi'])}")
        if isinstance(data['ling_shi'], dict):
            print(f"ling_shi的键: {list(data['ling_shi'].keys())}")
            if 'data' in data['ling_shi']:
                print(f"data数组长度: {len(data['ling_shi']['data'])}")
            if 'metadata' in data['ling_shi']:
                print(f"metadata: {data['ling_shi']['metadata']}")
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
    print(f"错误位置: {e.pos}")
    # 打印错误附近的上下文
    start = max(0, e.pos - 100)
    end = min(len(json_str), e.pos + 100)
    print(f"错误上下文: {json_str[start:end]}")