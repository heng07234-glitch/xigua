# 灵饰页面数据加载问题修复指南

## 问题症状
- 打开 `lingshi_estimate.html` 后一直显示"加载数据中..."
- 表格数据无法显示

## 可能的原因
1. `lingshi_data.js` 文件不存在或加载失败
2. `lingshi_data.js` 文件格式错误
3. JavaScript 语法错误阻止页面执行
4. 数据文件未正确生成

## 诊断步骤

### 步骤1：检查浏览器控制台
1. 打开 `lingshi_estimate.html`
2. 按 **F12** 打开开发者工具
3. 切换到 **控制台(Console)** 标签
4. 查看是否有红色错误信息

### 步骤2：运行数据加载测试
1. 打开 `test_data_loading.html`
2. 查看页面显示的测试结果
3. 确认 `LINGSHI_DATA` 是否已定义且包含数据

### 步骤3：重新生成数据文件
1. 双击运行 `E:\gujia\convert_lingshi.bat`
2. 按照提示操作
3. 如果转换成功，会显示"转换完成!"
4. 重新打开 `lingshi_estimate.html`

## 快速修复

### 如果看到错误 "LINGSHI_DATA未定义"
1. 检查 `mifangame-price-main\lingshi_data.js` 文件是否存在
2. 如果文件不存在，运行 `convert_lingshi.bat` 生成
3. 如果文件存在但为空，同样运行 `convert_lingshi.bat` 重新生成

### 如果看到JavaScript语法错误
1. 查看控制台错误信息
2. 根据错误信息定位问题
3. 可能需要手动修复 `lingshi_data.js` 文件

## 文件结构说明

```
E:\gujia\
├── convert_lingshi.bat          # 一键转换脚本
├── 灵饰价格表.xlsx              # Excel数据源
├── 灵饰logo\                    # 灵饰图标目录
└── mifangame-price-main\
    ├── lingshi_estimate.html    # 灵饰估价页面
    ├── lingshi_data.js          # 灵饰数据文件（自动生成）
    ├── test_data_loading.html   # 数据加载测试页面
    ├── icon_mapping.js          # 图标映射文件
    └── improved_rules.js        # 完整规则库（备用）
```

## 数据生成流程

1. 更新 `灵饰价格表.xlsx` 文件
2. 运行 `convert_lingshi.bat`
3. 脚本会调用 `scripts\convert_lingshi_v2.py`
4. 生成 `mifangame-price-main\lingshi_data.js`
5. 打开 `lingshi_estimate.html` 查看最新数据

## 常见问题解决

### Q: 运行 convert_lingshi.bat 时提示 "找不到灵饰价格表.xlsx"
A: 确保 Excel 文件位于以下位置之一：
   - `E:\gujia\灵饰价格表.xlsx`
   - `E:\Users\Administrator\Desktop\灵饰价格表.xlsx`

### Q: 运行 convert_lingshi.bat 时提示 Python 错误
A: 确保已安装 Python 和 required 依赖：
   ```cmd
   py -m pip install openpyxl
   ```

### Q: 页面显示但表格为空
A: 检查控制台是否有警告信息，可能需要调整数据解析逻辑

## 联系支持
如果以上步骤无法解决问题，请提供：
1. 浏览器控制台完整错误信息
2. `test_data_loading.html` 的测试结果截图
3. `convert_lingshi.bat` 的运行结果