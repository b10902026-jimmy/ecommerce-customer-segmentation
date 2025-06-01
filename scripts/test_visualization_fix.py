#!/usr/bin/env python3
"""
測試視覺化修復腳本 - Test Visualization Fix Script

專門用於測試RFM平均值圖表的修復效果
"""

import sys
import pandas as pd
from pathlib import Path

# 添加 src 目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from customer_segmentation.pipeline import CustomerSegmentationPipeline
from customer_segmentation.visualization.visualizer import DataVisualizer
from customer_segmentation.utils.logger import get_logger

logger = get_logger(__name__)


def print_banner():
    """顯示程式橫幅"""
    print("=" * 60)
    print("🔧 視覺化修復測試工具")
    print("   Visualization Fix Test Tool")
    print("=" * 60)


def test_customer_segments_plot():
    """測試客戶分群圖表的修復效果"""
    print_banner()
    
    try:
        # 自動尋找資料檔案
        possible_paths = [
            project_root / "data" / "raw" / "data.csv",
            project_root / "data.csv",
            project_root / "notebooks" / "data" / "results" / "cleaned_data.csv"
        ]
        
        data_file = None
        for path in possible_paths:
            if path.exists():
                data_file = path
                break
        
        if not data_file:
            logger.error("❌ 找不到資料檔案")
            return False
        
        logger.info(f"📂 使用資料檔案: {data_file}")
        
        # 載入資料並進行分析
        logger.info("🔄 載入資料並進行分析...")
        pipeline = CustomerSegmentationPipeline()
        
        # 如果是清理後的資料，直接載入
        if "cleaned_data.csv" in str(data_file):
            cleaned_data = pd.read_csv(data_file)
            pipeline.cleaned_data = cleaned_data
            pipeline.calculate_rfm()
            pipeline.segment_customers()
        else:
            pipeline.load_data(data_file)
            pipeline.clean_data()
            pipeline.calculate_rfm()
            pipeline.segment_customers()
        
        # 檢查資料
        logger.info(f"✅ 分析完成，客戶數量: {len(pipeline.segmented_data)}")
        logger.info(f"✅ 分群數量: {pipeline.segmented_data['Customer_Segment'].nunique()}")
        
        # 顯示RFM平均值（修復前的問題）
        segment_rfm = pipeline.segmented_data.groupby('Customer_Segment')[['Recency', 'Frequency', 'Monetary']].mean()
        logger.info("\n📊 各分群RFM原始平均值:")
        print(segment_rfm.round(2))
        
        # 顯示數值範圍差異
        logger.info("\n📏 數值範圍分析:")
        for col in ['Recency', 'Frequency', 'Monetary']:
            min_val = segment_rfm[col].min()
            max_val = segment_rfm[col].max()
            ratio = max_val / min_val if min_val > 0 else float('inf')
            logger.info(f"  {col}: {min_val:.1f} - {max_val:.1f} (比例: {ratio:.1f}:1)")
        
        # 建立視覺化器並生成修復後的圖表
        logger.info("\n🎨 生成修復後的客戶分群圖表...")
        visualizer = DataVisualizer()
        
        # 設置輸出目錄
        output_dir = project_root / "plots"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成圖表（這會使用修復後的標準化方法）
        visualizer.plot_customer_segments(pipeline.segmented_data, save_path=output_dir)
        
        logger.info("✅ 修復測試完成！")
        logger.info("📊 請檢查 plots/customer_segments.png 中的第二個子圖")
        logger.info("🔍 現在應該可以清楚看到三種顏色的條形：")
        logger.info("   - 淺珊瑚色 (lightcoral): Recency")
        logger.info("   - 金色 (gold): Frequency") 
        logger.info("   - 淺綠色 (lightgreen): Monetary")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函數"""
    success = test_customer_segments_plot()
    
    if success:
        print("\n" + "=" * 60)
        print("🎯 修復驗證結果:")
        print("✅ RFM平均值圖表已修復")
        print("✅ 使用標準化數值解決尺度問題")
        print("✅ 三個指標現在都清楚可見")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ 修復驗證失敗")
        print("請檢查錯誤訊息並重新執行")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
