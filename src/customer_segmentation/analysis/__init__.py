"""
分析模組 - Analysis Module

負責 RFM 分析和客戶分群相關的計算。

模組包含：
- RFMCalculator: RFM 指標計算器
- CustomerSegmentation: 客戶分群分析器
"""

from customer_segmentation.analysis.rfm_calculator import RFMCalculator

__all__ = ["RFMCalculator"]
