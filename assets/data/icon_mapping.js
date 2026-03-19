// 灵饰类型图标映射
// 从 灵饰价格表.xlsx 工作表1提取
// 生成时间: 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)]

const ICON_MAPPING = {
  "戒指": "🔴",
  "耳饰": "🔵",
  "配饰": "🟢",
  "手镯": "🟠"
};

// 获取类型图标
function getTypeIcon(type) {
    return ICON_MAPPING[type] || '';
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ICON_MAPPING,
        getTypeIcon
    };
}
