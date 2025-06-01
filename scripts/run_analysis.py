#!/usr/bin/env python3
"""
現代化主執行腳本 - Modern Main Execution Script

提供向後相容的執行方式，同時整合新的管道系統。
"""

import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from customer_segmentation.pipeline import CustomerSegmentationPipeline
from customer_segmentation.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """
    主函數 - 執行完整的客戶分群分析流程
    """
    logger.info("🚀 開始客戶分群分析 Starting Customer Segmentation Analysis")
    
    try:
        # 建立分析管道
        pipeline = CustomerSegmentationPipeline()
        
        # 執行完整分析
        data_file = project_root / "data" / "raw" / "data.csv"
        
        if not data_file.exists():
            logger.error(f"❌ 資料檔案不存在 Data file not found: {data_file}")
            return
        
        results = pipeline.run_full_analysis(
            file_path=data_file,
            remove_outliers=False,
            rfm_bins=5,
            create_plots=True,
            export_results=True
        )
        
        # 確保圖表保存到 plots 目錄
        plots_dir = project_root / "plots"
        plots_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 圖表已保存到 Charts saved to: {plots_dir}")
        
        # 顯示摘要
        summary = results
        logger.info("📋 分析摘要 Analysis Summary:")
        logger.info(f"  原始資料: {summary['data_overview']['original_records']:,} 筆")
        logger.info(f"  清理後資料: {summary['data_overview']['cleaned_records']:,} 筆")
        logger.info(f"  分析客戶數: {summary['data_overview']['customers_analyzed']:,} 位")
        logger.info(f"  客戶分群數: {summary['segmentation_results']['total_segments']} 個")
        
        logger.info("✅ 客戶分群分析完成！Customer Segmentation Analysis Completed!")
        
    except Exception as e:
        logger.error(f"❌ 分析過程中發生錯誤 Error occurred during analysis: {e}")
        raise


def run_quick_analysis():
    """
    快速分析模式 - 僅執行核心分析，不包含詳細視覺化
    """
    logger.info("⚡ 快速分析模式 Quick Analysis Mode")
    
    try:
        # 建立分析管道
        pipeline = CustomerSegmentationPipeline()
        
        # 執行快速分析
        data_file = project_root / "data" / "raw" / "data.csv"
        
        if not data_file.exists():
            logger.error(f"❌ 資料檔案不存在 Data file not found: {data_file}")
            return
        
        # 逐步執行分析
        pipeline.load_data(data_file)
        pipeline.clean_data()
        pipeline.calculate_rfm()
        pipeline.segment_customers()
        
        # 匯出結果
        exported_files = pipeline.export_results()
        
        # 確保圖表保存到 plots 目錄（快速模式也生成基本圖表）
        plots_dir = project_root / "plots"
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成基本的 RFM 分布圖
        try:
            from customer_segmentation.visualization.visualizer import DataVisualizer
            visualizer = DataVisualizer()
            visualizer.plot_rfm_distributions(pipeline.rfm_data, save_path=plots_dir)
            logger.info(f"📁 基本圖表已保存到 Basic charts saved to: {plots_dir}")
        except Exception as e:
            logger.warning(f"⚠️ 圖表生成失敗 Chart generation failed: {e}")
        
        logger.info("✅ 快速分析完成！結果已匯出 Quick analysis completed! Results exported")
        
        return pipeline.segmented_data
        
    except Exception as e:
        logger.error(f"❌ 快速分析失敗 Quick analysis failed: {e}")
        raise


if __name__ == "__main__":
    # 檢查命令列參數
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        results = run_quick_analysis()
    else:
        results = main()
