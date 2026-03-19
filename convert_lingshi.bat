@echo off
echo 正在转换灵饰价格表...
echo.

REM 检查Excel文件是否存在
if not exist "E:\gujia\assets\sources\lingshi.xlsx" (
    echo 错误: 找不到灵饰价格表.xlsx
    echo 请确保文件位于以下位置:
    echo   - E:\gujia\assets\sources\lingshi.xlsx
    pause
    exit /b 1
)

REM 运行Python转换脚本
echo 运行Python转换脚本...
py scripts\convert_lingshi_v2.py

if %errorlevel% neq 0 (
    echo 转换失败，请检查Python环境
    pause
    exit /b 1
)


echo.
echo 转换完成!
echo 请打开 web\ling-shi\estimate.html 查看最新数据
echo.
pause