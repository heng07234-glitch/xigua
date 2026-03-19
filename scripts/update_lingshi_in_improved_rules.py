#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json
import os

def extract_lingshi_data(js_file_path):
    """从lingshi_data.js中提取LINGSHI_DATA数组"""
    with open(js_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找LINGSHI_DATA数组
    match = re.search(r'const LINGSHI_DATA = (\[.*?\]);', content, re.DOTALL)
    if not match:
        print("错误: 未找到LINGSHI_DATA数组")
        return None

    json_str = match.group(1)
    try:
        data = json.loads(json_str)
        print(f"从 {js_file_path} 读取 {len(data)} 条灵饰数据")
        return data
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None

def update_improved_rules(improved_rules_path, lingshi_data):
    """更新improved_rules.js中的ling_shi部分"""
    with open(improved_rules_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 构建新的ling_shi部分
    lingshi_json = json.dumps(lingshi_data, ensure_ascii=False, indent=2)
    new_lingshi_section = '''  "ling_shi": {
    "data": ''' + lingshi_json + ''',
    "metadata": {
      "source": "E:\gujia\assets\sources\lingshi.xlsx",
      "count": ''' + str(len(lingshi_data)) + ''',
      "last_updated": "2026-03-18",
      "description": "结构化灵饰价格数据，包含前排和后排"
    }
  }'''

    # 查找并替换ling_shi部分
    # 查找"ling_shi": {到下一个顶级大括号结束
    # 使用正则表达式匹配整个ling_shi对象
    pattern = r'(\s*)"ling_shi":\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        print("找到ling_shi部分，进行替换...")
        old_section = match.group(0)
        indent = match.group(1)

        # 调整新部分的缩进
        lines = new_lingshi_section.split('\n')
        new_section = '\n'.join(indent + line if line.strip() else line for line in lines)

        new_content = content.replace(old_section, new_section)
    else:
        print("未找到ling_shi部分，尝试手动查找...")
        # 手动查找
        start = content.find('"ling_shi": {')
        if start == -1:
            print("错误: 找不到ling_shi部分")
            return None

        # 找到匹配的结束大括号
        brace_count = 0
        i = start
        while i < len(content):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i
                    break
            i += 1
        else:
            print("错误: 找不到ling_shi部分的结束大括号")
            return None

        old_section = content[start:end+1]
        # 获取缩进
        indent_start = start
        while indent_start > 0 and content[indent_start-1] != '\n':
            indent_start -= 1
        indent = content[indent_start:start]

        # 调整缩进
        lines = new_lingshi_section.split('\n')
        new_section = '\n'.join(indent + line if line.strip() else line for line in lines)

        new_content = content[:start] + new_section + content[end+1:]

    # 更新生成时间
    new_content = re.sub(
        r'生成时间: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}（整合灵饰数据）',
        '生成时间: 2026-03-18 20:15:00（更新后排数据）',
        new_content
    )

    # 写入文件
    backup_path = improved_rules_path.replace('.js', '_backup_before_rear.js')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"原文件已备份到: {backup_path}")

    with open(improved_rules_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"已更新 {improved_rules_path}")
    return new_content

def main():
    lingshi_data_path = '../assets/data/lingshi_data.js'
    improved_rules_path = '../assets/data/improved_rules.js'

    if not os.path.exists(lingshi_data_path):
        print(f"错误: {lingshi_data_path} 不存在")
        return

    if not os.path.exists(improved_rules_path):
        print(f"错误: {improved_rules_path} 不存在")
        return

    # 提取灵饰数据
    lingshi_data = extract_lingshi_data(lingshi_data_path)
    if not lingshi_data:
        return

    # 更新improved_rules.js
    update_improved_rules(improved_rules_path, lingshi_data)

    print("更新完成！")

if __name__ == "__main__":
    main()