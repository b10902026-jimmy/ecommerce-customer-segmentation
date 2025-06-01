"""
客戶分群分析系統 - Customer Segmentation Analysis System

這是一個基於 RFM (Recency, Frequency, Monetary) 模型的客戶分群分析系統，
專為電商交易資料設計，幫助企業識別不同類型的客戶群體。

主要功能：
- 資料載入和清理
- RFM 指標計算
- 客戶分群分析
- 視覺化分析
- 客戶終身價值計算

使用範例：
    from customer_segmentation import CustomerSegmentationPipeline
    
    pipeline = CustomerSegmentationPipeline()
    results = pipeline.run_analysis('data.csv')
"""

__version__ = "1.0.0"
__author__ = "Customer Segmentation Team"
__email__ = "team@example.com"

# 主要類別的快速導入
from customer_segmentation.analysis.rfm_calculator import RFMCalculator
from customer_segmentation.data.cleaner import DataCleaner
from customer_segmentation.data.loader import DataLoader
from customer_segmentation.visualization.visualizer import DataVisualizer

# 便利的管道類別
from customer_segmentation.pipeline import CustomerSegmentationPipeline

__all__ = [
    "DataLoader",
    "DataCleaner", 
    "RFMCalculator",
    "DataVisualizer",
    "CustomerSegmentationPipeline",
]
