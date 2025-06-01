#!/usr/bin/env python3
"""
簡單的中文字體設置腳本 - Simple Chinese Font Setup Script
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def setup_chinese_fonts():
    """設置中文字體"""
    
    # 重新載入字體管理器
    fm.fontManager.__init__()
    
    # 檢查可用字體
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    # 中文字體優先順序
    chinese_fonts = [
        'Noto Sans CJK SC',
        'WenQuanYi Micro Hei', 
        'Noto Serif CJK SC',
        'DejaVu Sans'
    ]
    
    print("🔍 檢查可用字體:")
    found_fonts = []
    for font in chinese_fonts:
        if font in available_fonts:
            print(f"  ✅ {font}")
            found_fonts.append(font)
        else:
            print(f"  ❌ {font}")
    
    if found_fonts:
        # 設置字體
        plt.rcParams['font.sans-serif'] = found_fonts + ['Arial', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        print(f"\n✅ 已設置中文字體: {found_fonts[0]}")
        
        # 測試中文顯示
        test_chinese_display(found_fonts[0])
        
        return True
    else:
        print("\n❌ 未找到中文字體")
        return False

def test_chinese_display(font_name):
    """測試中文顯示"""
    import numpy as np
    from pathlib import Path
    
    print(f"\n🧪 測試中文字體顯示...")
    
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        ax.plot(x, y, label='正弦波')
        ax.set_title('中文字體測試', fontsize=16)
        ax.set_xlabel('時間')
        ax.set_ylabel('數值')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 儲存測試圖片
        test_dir = Path('plots')
        test_dir.mkdir(exist_ok=True)
        plt.savefig(test_dir / 'chinese_font_test.png', dpi=150, bbox_inches='tight')
        
        print(f"✅ 測試完成，圖片已儲存至: {test_dir / 'chinese_font_test.png'}")
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🛍️ 中文字體設置腳本")
    print("=" * 40)
    
    success = setup_chinese_fonts()
    
    if success:
        print("\n🎉 中文字體設置完成！")
        print("\n📋 接下來請:")
        print("1. 重新啟動 Jupyter Notebook")
        print("2. 在 Notebook 中執行以下代碼:")
        print("   import matplotlib.pyplot as plt")
        print("   plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']")
        print("   plt.rcParams['axes.unicode_minus'] = False")
    else:
        print("\n❌ 字體設置失敗")
