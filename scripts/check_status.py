#!/usr/bin/env python3
"""
專案狀態檢查腳本 - Project Status Check Script

檢查專案的設置狀態和依賴項目。
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple

# 添加 src 目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def check_python_version() -> Tuple[bool, str]:
    """檢查 Python 版本"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 9:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        else:
            return False, f"Python {version.major}.{version.minor}.{version.micro} (需要 3.9+)"
    except Exception as e:
        return False, f"無法檢查 Python 版本: {e}"

def check_package_import() -> Tuple[bool, str]:
    """檢查套件導入"""
    try:
        from customer_segmentation import CustomerSegmentationPipeline
        return True, "客戶分群分析套件導入成功"
    except ImportError as e:
        return False, f"套件導入失敗: {e}"

def check_dependencies() -> List[Tuple[str, bool, str]]:
    """檢查依賴套件"""
    dependencies = [
        "pandas",
        "numpy", 
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "plotly",
        "click",
        "rich",
        "loguru",
        "pydantic"
    ]
    
    results = []
    for dep in dependencies:
        try:
            __import__(dep)
            results.append((dep, True, "已安裝"))
        except ImportError:
            results.append((dep, False, "未安裝"))
    
    return results

def check_directories() -> List[Tuple[str, bool, str]]:
    """檢查專案目錄結構"""
    required_dirs = [
        "src/customer_segmentation",
        "data/raw",
        "data/processed", 
        "data/results",
        "notebooks",
        "scripts"
    ]
    
    results = []
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            results.append((dir_path, True, "存在"))
        else:
            results.append((dir_path, False, "不存在"))
    
    return results

def check_data_files() -> List[Tuple[str, bool, str]]:
    """檢查資料檔案"""
    data_files = [
        "data/raw/data.csv",
        "data/data_description.md"
    ]
    
    results = []
    for file_path in data_files:
        full_path = project_root / file_path
        if full_path.exists():
            size = full_path.stat().st_size / (1024 * 1024)  # MB
            results.append((file_path, True, f"存在 ({size:.1f} MB)"))
        else:
            results.append((file_path, False, "不存在"))
    
    return results

def check_conda_environment() -> Tuple[bool, str]:
    """檢查 Conda 環境"""
    try:
        result = subprocess.run(
            ["conda", "env", "list"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if "customer-segmentation" in result.stdout:
            return True, "Conda 環境 'customer-segmentation' 存在"
        else:
            return False, "Conda 環境 'customer-segmentation' 不存在"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "Conda 未安裝或無法執行"

def check_poetry() -> Tuple[bool, str]:
    """檢查 Poetry"""
    try:
        result = subprocess.run(
            ["poetry", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            return True, f"Poetry 已安裝: {result.stdout.strip()}"
        else:
            return False, "Poetry 執行失敗"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "Poetry 未安裝"

def print_status_table(title: str, items: List[Tuple[str, bool, str]]):
    """打印狀態表格"""
    print(f"\n📋 {title}")
    print("=" * 60)
    
    for item, status, message in items:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {item:<30} {message}")

def main():
    """主函數"""
    print("🛍️ 客戶分群分析系統 - 專案狀態檢查")
    print("Customer Segmentation Analysis System - Project Status Check")
    print("=" * 70)
    
    # 檢查 Python 版本
    python_ok, python_msg = check_python_version()
    print(f"\n🐍 Python 版本檢查: {'✅' if python_ok else '❌'} {python_msg}")
    
    # 檢查套件導入
    import_ok, import_msg = check_package_import()
    print(f"📦 套件導入檢查: {'✅' if import_ok else '❌'} {import_msg}")
    
    # 檢查 Conda 環境
    conda_ok, conda_msg = check_conda_environment()
    print(f"🐍 Conda 環境檢查: {'✅' if conda_ok else '❌'} {conda_msg}")
    
    # 檢查 Poetry
    poetry_ok, poetry_msg = check_poetry()
    print(f"📝 Poetry 檢查: {'✅' if poetry_ok else '❌'} {poetry_msg}")
    
    # 檢查依賴套件
    deps = check_dependencies()
    print_status_table("依賴套件檢查 Dependencies Check", deps)
    
    # 檢查目錄結構
    dirs = check_directories()
    print_status_table("目錄結構檢查 Directory Structure Check", dirs)
    
    # 檢查資料檔案
    files = check_data_files()
    print_status_table("資料檔案檢查 Data Files Check", files)
    
    # 總結
    print(f"\n📊 檢查摘要 Summary")
    print("=" * 30)
    
    total_checks = len(deps) + len(dirs) + len(files) + 4  # +4 for python, import, conda, poetry
    passed_checks = (
        sum(1 for _, status, _ in deps if status) +
        sum(1 for _, status, _ in dirs if status) +
        sum(1 for _, status, _ in files if status) +
        sum([python_ok, import_ok, conda_ok, poetry_ok])
    )
    
    print(f"通過檢查 Passed: {passed_checks}/{total_checks}")
    print(f"成功率 Success Rate: {passed_checks/total_checks*100:.1f}%")
    
    if passed_checks == total_checks:
        print("\n🎉 所有檢查都通過！專案已準備就緒。")
        print("🎉 All checks passed! Project is ready to use.")
    else:
        print(f"\n⚠️ 有 {total_checks - passed_checks} 項檢查未通過。")
        print("⚠️ Some checks failed. Please review the issues above.")
        
        # 提供修復建議
        print("\n🔧 修復建議 Fix Suggestions:")
        if not python_ok:
            print("  • 請安裝 Python 3.9 或更高版本")
        if not import_ok:
            print("  • 請執行 'python scripts/setup.sh' 安裝依賴")
        if not conda_ok:
            print("  • 請執行 'conda env create -f environment.yml'")
        if not poetry_ok:
            print("  • 請安裝 Poetry: 'pip install poetry'")
        
        failed_deps = [name for name, status, _ in deps if not status]
        if failed_deps:
            print(f"  • 請安裝缺失的套件: {', '.join(failed_deps)}")

if __name__ == "__main__":
    main()
