#!/usr/bin/env python3
"""
中文字體修復腳本 - Chinese Font Fix Script

解決 Jupyter Notebook 和 matplotlib 中文字體顯示問題。
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import sys
from pathlib import Path
import subprocess

def check_available_fonts():
    """檢查可用的中文字體"""
    print("🔍 檢查系統可用字體 Checking available fonts...")
    
    # 獲取所有可用字體
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    # 中文字體列表
    chinese_fonts = [
        'DejaVu Sans',
        'SimHei',
        'Microsoft YaHei', 
        'WenQuanYi Micro Hei',
        'Noto Sans CJK SC',
        'Source Han Sans SC',
        'Arial Unicode MS',
        'Droid Sans Fallback',
        'Liberation Sans'
    ]
    
    print("\n📋 可用的中文字體 Available Chinese fonts:")
    found_fonts = []
    for font in chinese_fonts:
        if font in available_fonts:
            print(f"  ✅ {font}")
            found_fonts.append(font)
        else:
            print(f"  ❌ {font}")
    
    return found_fonts

def install_chinese_fonts():
    """安裝中文字體"""
    print("\n📦 嘗試安裝中文字體 Attempting to install Chinese fonts...")
    
    try:
        # 檢查作業系統
        if sys.platform.startswith('linux'):
            # Ubuntu/Debian
            print("🐧 檢測到 Linux 系統，嘗試安裝字體...")
            subprocess.run([
                'sudo', 'apt-get', 'update'
            ], check=False, capture_output=True)
            
            subprocess.run([
                'sudo', 'apt-get', 'install', '-y', 
                'fonts-dejavu', 'fonts-liberation', 
                'fonts-noto-cjk', 'fonts-wqy-microhei'
            ], check=False, capture_output=True)
            
        elif sys.platform == 'darwin':
            # macOS
            print("🍎 檢測到 macOS 系統，嘗試安裝字體...")
            subprocess.run([
                'brew', 'install', 'font-dejavu', 'font-liberation'
            ], check=False, capture_output=True)
            
        print("✅ 字體安裝完成 Font installation completed")
        
    except Exception as e:
        print(f"⚠️ 字體安裝失敗 Font installation failed: {e}")
        print("請手動安裝中文字體 Please install Chinese fonts manually")

def configure_matplotlib():
    """配置 matplotlib 中文字體"""
    print("\n🎨 配置 matplotlib 中文字體 Configuring matplotlib Chinese fonts...")
    
    # 檢查可用字體
    found_fonts = check_available_fonts()
    
    if not found_fonts:
        print("❌ 未找到可用的中文字體 No Chinese fonts found")
        install_chinese_fonts()
        # 重新檢查
        found_fonts = check_available_fonts()
    
    if found_fonts:
        # 使用第一個可用的字體
        selected_font = found_fonts[0]
        print(f"✅ 選擇字體 Selected font: {selected_font}")
        
        # 設置 matplotlib 配置
        plt.rcParams['font.sans-serif'] = [selected_font] + plt.rcParams['font.sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 測試中文顯示
        test_chinese_display(selected_font)
        
        return selected_font
    else:
        print("❌ 仍然無法找到中文字體 Still cannot find Chinese fonts")
        return None

def test_chinese_display(font_name):
    """測試中文字體顯示"""
    print(f"\n🧪 測試中文字體顯示 Testing Chinese font display with {font_name}...")
    
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        # 建立測試圖表
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 測試資料
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        ax.plot(x, y, label='正弦波 Sine Wave')
        ax.set_title('中文字體測試 Chinese Font Test', fontsize=16)
        ax.set_xlabel('時間 Time')
        ax.set_ylabel('數值 Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 儲存測試圖片
        test_dir = Path('plots')
        test_dir.mkdir(exist_ok=True)
        plt.savefig(test_dir / 'chinese_font_test.png', dpi=150, bbox_inches='tight')
        
        print(f"✅ 中文字體測試完成 Chinese font test completed")
        print(f"📁 測試圖片已儲存至 Test image saved to: {test_dir / 'chinese_font_test.png'}")
        
        plt.close()
        
    except Exception as e:
        print(f"❌ 中文字體測試失敗 Chinese font test failed: {e}")

def create_matplotlib_config():
    """建立 matplotlib 配置檔案"""
    print("\n📝 建立 matplotlib 配置檔案 Creating matplotlib config file...")
    
    try:
        # 獲取 matplotlib 配置目錄
        config_dir = Path(plt.get_configdir())
        config_file = config_dir / 'matplotlibrc'
        
        # 檢查可用字體
        found_fonts = check_available_fonts()
        
        if found_fonts:
            font_list = ', '.join(found_fonts)
            
            # 建立配置內容
            config_content = f"""
# matplotlib 中文字體配置
# Chinese font configuration for matplotlib

font.sans-serif: {font_list}, DejaVu Sans, Arial, sans-serif
axes.unicode_minus: False
font.size: 10
figure.figsize: 12, 8
figure.dpi: 100
savefig.dpi: 300
"""
            
            # 寫入配置檔案
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content.strip())
            
            print(f"✅ 配置檔案已建立 Config file created: {config_file}")
            
        else:
            print("❌ 無法建立配置檔案，未找到中文字體 Cannot create config file, no Chinese fonts found")
            
    except Exception as e:
        print(f"❌ 配置檔案建立失敗 Config file creation failed: {e}")

def clear_matplotlib_cache():
    """清除 matplotlib 快取"""
    print("\n🗑️ 清除 matplotlib 快取 Clearing matplotlib cache...")
    
    try:
        # 清除字體快取
        fm._rebuild()
        
        # 清除 matplotlib 快取目錄
        cache_dir = Path(plt.get_cachedir())
        if cache_dir.exists():
            import shutil
            shutil.rmtree(cache_dir, ignore_errors=True)
            print("✅ matplotlib 快取已清除 matplotlib cache cleared")
        
    except Exception as e:
        print(f"⚠️ 快取清除失敗 Cache clearing failed: {e}")

def create_jupyter_config():
    """建立 Jupyter 配置"""
    print("\n📓 建立 Jupyter 中文字體配置 Creating Jupyter Chinese font config...")
    
    try:
        # 建立 Jupyter 配置目錄
        jupyter_config_dir = Path.home() / '.jupyter'
        jupyter_config_dir.mkdir(exist_ok=True)
        
        # 建立自訂 CSS
        custom_css = jupyter_config_dir / 'custom' / 'custom.css'
        custom_css.parent.mkdir(exist_ok=True)
        
        css_content = """
/* Jupyter Notebook 中文字體配置 */
/* Chinese font configuration for Jupyter Notebook */

.CodeMirror {
    font-family: 'DejaVu Sans Mono', 'Liberation Mono', 'Consolas', monospace !important;
}

.rendered_html {
    font-family: 'DejaVu Sans', 'Liberation Sans', 'Arial', sans-serif !important;
}

.output_text {
    font-family: 'DejaVu Sans', 'Liberation Sans', 'Arial', sans-serif !important;
}
"""
        
        with open(custom_css, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print(f"✅ Jupyter 配置已建立 Jupyter config created: {custom_css}")
        
    except Exception as e:
        print(f"❌ Jupyter 配置建立失敗 Jupyter config creation failed: {e}")

def main():
    """主函數"""
    print("🛍️ 中文字體修復腳本 Chinese Font Fix Script")
    print("=" * 60)
    
    # 1. 檢查可用字體
    found_fonts = check_available_fonts()
    
    # 2. 如果沒有字體，嘗試安裝
    if not found_fonts:
        install_chinese_fonts()
    
    # 3. 配置 matplotlib
    selected_font = configure_matplotlib()
    
    # 4. 清除快取
    clear_matplotlib_cache()
    
    # 5. 建立配置檔案
    create_matplotlib_config()
    
    # 6. 建立 Jupyter 配置
    create_jupyter_config()
    
    print("\n" + "=" * 60)
    print("🎉 中文字體修復完成 Chinese font fix completed!")
    print("\n📋 後續步驟 Next steps:")
    print("1. 重新啟動 Jupyter Notebook Restart Jupyter Notebook")
    print("2. 重新執行包含圖表的程式碼 Re-run code with plots")
    print("3. 檢查中文字體是否正常顯示 Check if Chinese fonts display correctly")
    
    if selected_font:
        print(f"\n✅ 推薦使用的字體 Recommended font: {selected_font}")
    
    print("\n💡 如果問題仍然存在 If problems persist:")
    print("   - 重新啟動 Python kernel")
    print("   - 檢查 plots/chinese_font_test.png 測試圖片")
    print("   - 手動安裝更多中文字體")

if __name__ == "__main__":
    main()
