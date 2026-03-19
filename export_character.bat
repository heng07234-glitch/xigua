@echo off
chcp 65001 >nul
echo 角色数据更新工具
echo ===================
echo.
echo 选项:
echo  1. 从Excel估价表导入角色估价规则数据（推荐）
echo  2. 从MongoDB导出实时角色数据（原始藏宝阁数据）
echo  3. 退出
echo.
set /p choice="请选择 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 正在从Excel导入角色估价规则数据...
    echo.
    cd /d "%~dp0"
    py scripts\import_character_rules.py
) else if "%choice%"=="2" (
    echo.
    echo 正在从MongoDB导出实时角色数据...
    echo.
    cd /d "%~dp0"
    py scripts\export_character_data.py --export
) else (
    echo 退出
    exit /b 0
)

echo.
pause