@echo off
chcp 65001 >nul
echo 灵饰数据导出工具
echo ===================
echo.
echo 选项:
echo  1. 从MongoDB导出实时灵饰数据（原始藏宝阁数据）
echo  2. 创建示例数据（用于测试）
echo  3. 退出
echo.
set /p choice="请选择 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 正在从MongoDB导出实时灵饰数据...
    echo.
    cd /d "%~dp0"
    py scripts\export_zbgls_data.py --export
) else if "%choice%"=="2" (
    echo.
    echo 正在创建示例数据...
    echo.
    cd /d "%~dp0"
    py scripts\export_zbgls_data.py --sample
) else (
    echo 退出
    exit /b 0
)

echo.
pause