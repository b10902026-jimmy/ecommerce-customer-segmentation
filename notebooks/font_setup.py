"""
Jupyter Notebook 中文字體配置
在 Notebook 開始時執行此代碼來設置中文字體
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings

# 忽略字體警告
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

def setup_chinese_fonts_for_notebook():
    """為 Jupyter Notebook 設置中文字體"""
    
    # 重新載入字體管理器
    fm.fontManager.__init__()
    
    # 設置中文字體
    plt.rcParams['font.sans-serif'] = [
        'WenQuanYi Micro Hei',  # 文泉驛微米黑
        'Noto Sans CJK SC',     # Google Noto 字體
        'DejaVu Sans',          # 備用字體
        'Arial',
        'sans-serif'
    ]
    
    # 設置負號正常顯示
    plt.rcParams['axes.unicode_minus'] = False
    
    # 設置圖表樣式
    plt.rcParams.update({
        'figure.figsize': (12, 8),
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })
    
    print("✅ 中文字體配置完成！Chinese font setup completed!")
    print("📊 現在可以正常顯示中文圖表了 Chinese charts should now display correctly")

# 執行字體設置
setup_chinese_fonts_for_notebook()

# 測試中文顯示
def test_chinese_display():
    """測試中文字體顯示"""
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    ax.plot(x, y, label='正弦波 Sine Wave', linewidth=2)
    ax.set_title('中文字體測試 Chinese Font Test', fontsize=16)
    ax.set_xlabel('時間 Time')
    ax.set_ylabel('數值 Value')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("如果上面的圖表中文顯示正常，說明字體配置成功！")
    print("If Chinese text displays correctly above, font setup is successful!")

# 可選：執行測試
# test_chinese_display()
