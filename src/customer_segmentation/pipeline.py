"""
客戶分群分析管道 - Customer Segmentation Analysis Pipeline

提供完整的分析管道，整合所有模組功能。
"""

from pathlib import Path
from typing import Dict, Optional, Union

import pandas as pd
from loguru import logger

from customer_segmentation.analysis.rfm_calculator import RFMCalculator
from customer_segmentation.data.cleaner import DataCleaner
from customer_segmentation.data.loader import DataLoader
from customer_segmentation.utils.config import get_config
from customer_segmentation.utils.logger import LoggerMixin, log_execution_time
from customer_segmentation.visualization.visualizer import DataVisualizer


class CustomerSegmentationPipeline(LoggerMixin):
    """
    客戶分群分析管道
    
    整合資料載入、清理、RFM 分析、分群和視覺化的完整流程。
    """
    
    def __init__(self, config_override: Optional[Dict] = None):
        """
        初始化分析管道
        
        Args:
            config_override: 覆蓋預設配置的字典
        """
        self.config = get_config()
        if config_override:
            for key, value in config_override.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
        
        self.loader = None
        self.cleaner = None
        self.rfm_calculator = None
        self.visualizer = None
        
        # 資料儲存
        self.raw_data = None
        self.cleaned_data = None
        self.rfm_data = None
        self.segmented_data = None
        
        self.logger.info("🔧 客戶分群分析管道初始化完成 Pipeline initialized")
    
    @log_execution_time
    def load_data(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        載入資料
        
        Args:
            file_path: 資料檔案路徑
            
        Returns:
            pd.DataFrame: 載入的資料
        """
        self.logger.info(f"📂 載入資料 Loading data from: {file_path}")
        
        self.loader = DataLoader(str(file_path))
        self.raw_data = self.loader.load_data()
        
        # 驗證必要欄位
        required_columns = [
            'InvoiceNo', 'StockCode', 'Description', 'Quantity',
            'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'
        ]
        
        if not self.loader.validate_columns(required_columns):
            raise ValueError("資料缺少必要欄位，無法進行分析")
        
        self.logger.info(f"✅ 資料載入完成 Data loaded: {self.raw_data.shape}")
        return self.raw_data
    
    @log_execution_time
    def clean_data(self, remove_outliers: bool = False) -> pd.DataFrame:
        """
        清理資料
        
        Args:
            remove_outliers: 是否移除異常值
            
        Returns:
            pd.DataFrame: 清理後的資料
        """
        if self.raw_data is None:
            raise ValueError("請先載入資料 Please load data first")
        
        self.logger.info("🧹 開始資料清理 Starting data cleaning")
        
        self.cleaner = DataCleaner(self.raw_data)
        self.cleaned_data = self.cleaner.clean_all(remove_outliers=remove_outliers)
        
        # 記錄清理結果
        cleaning_summary = self.cleaner.get_cleaning_summary()
        self.logger.info(
            f"✅ 資料清理完成 Data cleaning completed: "
            f"{cleaning_summary['final_count']:,} records "
            f"({cleaning_summary['retention_rate']:.1f}% retained)"
        )
        
        return self.cleaned_data
    
    @log_execution_time
    def calculate_rfm(self, analysis_date: Optional[str] = None) -> pd.DataFrame:
        """
        計算 RFM 指標
        
        Args:
            analysis_date: 分析日期 (YYYY-MM-DD 格式)
            
        Returns:
            pd.DataFrame: RFM 資料
        """
        if self.cleaned_data is None:
            raise ValueError("請先清理資料 Please clean data first")
        
        self.logger.info("🎯 開始 RFM 分析 Starting RFM analysis")
        
        # 處理分析日期
        if analysis_date:
            from datetime import datetime
            analysis_date = datetime.strptime(analysis_date, "%Y-%m-%d")
        
        self.rfm_calculator = RFMCalculator(self.cleaned_data)
        self.rfm_data = self.rfm_calculator.calculate_rfm(analysis_date)
        
        self.logger.info(f"✅ RFM 計算完成 RFM calculation completed: {len(self.rfm_data):,} customers")
        return self.rfm_data
    
    @log_execution_time
    def segment_customers(self, rfm_bins: int = 5) -> pd.DataFrame:
        """
        進行客戶分群
        
        Args:
            rfm_bins: RFM 分數的分組數量
            
        Returns:
            pd.DataFrame: 分群後的客戶資料
        """
        if self.rfm_data is None:
            raise ValueError("請先計算 RFM 指標 Please calculate RFM first")
        
        self.logger.info("👥 開始客戶分群 Starting customer segmentation")
        
        # 計算 RFM 分數
        rfm_scores = self.rfm_calculator.calculate_rfm_scores(
            r_bins=rfm_bins, f_bins=rfm_bins, m_bins=rfm_bins
        )
        
        # 進行分群
        self.segmented_data = self.rfm_calculator.segment_customers(rfm_scores)
        
        # 計算客戶終身價值
        self.segmented_data = self.rfm_calculator.calculate_customer_lifetime_value(
            self.segmented_data
        )
        
        segment_counts = self.segmented_data['Customer_Segment'].value_counts()
        self.logger.info(f"✅ 客戶分群完成 Customer segmentation completed: {len(segment_counts)} segments")
        
        return self.segmented_data
    
    @log_execution_time
    def create_visualizations(self, save_plots: bool = True) -> None:
        """
        建立視覺化圖表
        
        Args:
            save_plots: 是否儲存圖表
        """
        if self.segmented_data is None:
            raise ValueError("請先完成客戶分群 Please complete customer segmentation first")
        
        self.logger.info("🎨 開始建立視覺化圖表 Starting visualization creation")
        
        self.visualizer = DataVisualizer()
        
        # 設置圖表保存路徑
        plots_dir = Path("plots")
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        # 建立各種圖表
        try:
            if save_plots:
                # 保存所有圖表到 plots 目錄
                self.visualizer.save_all_plots(
                    rfm_data=self.rfm_data,
                    segmented_data=self.segmented_data,
                    cleaned_data=self.cleaned_data,
                    output_dir=plots_dir
                )
            else:
                # 只顯示圖表，不保存
                self.visualizer.plot_rfm_distributions(self.rfm_data)
                self.visualizer.plot_rfm_correlation(self.rfm_data)
                self.visualizer.plot_customer_segments(self.segmented_data)
                self.visualizer.plot_time_series_analysis(self.cleaned_data)
                self.visualizer.plot_geographic_analysis(self.cleaned_data)
            
            self.logger.info("✅ 視覺化圖表建立完成 Visualization creation completed")
            
        except Exception as e:
            self.logger.error(f"❌ 視覺化建立失敗 Visualization creation failed: {e}")
            raise
    
    @log_execution_time
    def export_results(self, output_dir: Optional[Path] = None) -> Dict[str, Path]:
        """
        匯出分析結果
        
        Args:
            output_dir: 輸出目錄，預設使用配置中的 results_dir
            
        Returns:
            Dict[str, Path]: 匯出檔案的路徑字典
        """
        if self.segmented_data is None:
            raise ValueError("請先完成分析 Please complete analysis first")
        
        if output_dir is None:
            output_dir = self.config.results_dir
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"💾 匯出分析結果 Exporting results to: {output_dir}")
        
        exported_files = {}
        
        try:
            # 匯出完整分析結果
            results_file = output_dir / "customer_segmentation_results.csv"
            self.segmented_data.to_csv(results_file, index=False, encoding=self.config.encoding)
            exported_files['segmentation_results'] = results_file
            
            # 匯出清理後的資料到 processed 目錄
            processed_dir = self.config.processed_data_dir
            processed_dir.mkdir(parents=True, exist_ok=True)
            cleaned_file = processed_dir / "cleaned_data.csv"
            self.cleaned_data.to_csv(cleaned_file, index=False, encoding=self.config.encoding)
            exported_files['cleaned_data'] = cleaned_file
            
            # 匯出 RFM 資料
            rfm_file = output_dir / "rfm_data.csv"
            self.rfm_data.to_csv(rfm_file, index=False, encoding=self.config.encoding)
            exported_files['rfm_data'] = rfm_file
            
            # 匯出分群摘要
            segment_summary = self.rfm_calculator.get_segment_summary(self.segmented_data)
            summary_file = output_dir / "segment_summary.csv"
            segment_summary.to_csv(summary_file, encoding=self.config.encoding)
            exported_files['segment_summary'] = summary_file
            
            self.logger.info(f"✅ 結果匯出完成 Results exported: {len(exported_files)} files")
            
        except Exception as e:
            self.logger.error(f"❌ 結果匯出失敗 Results export failed: {e}")
            raise
        
        return exported_files
    
    @log_execution_time
    def run_full_analysis(
        self,
        file_path: Union[str, Path],
        remove_outliers: bool = False,
        rfm_bins: int = 5,
        analysis_date: Optional[str] = None,
        create_plots: bool = True,
        export_results: bool = True
    ) -> Dict:
        """
        執行完整的分析流程
        
        Args:
            file_path: 資料檔案路徑
            remove_outliers: 是否移除異常值
            rfm_bins: RFM 分數的分組數量
            analysis_date: 分析日期
            create_plots: 是否建立視覺化圖表
            export_results: 是否匯出結果
            
        Returns:
            Dict: 分析結果摘要
        """
        self.logger.info("🚀 開始完整分析流程 Starting full analysis pipeline")
        
        try:
            # 1. 載入資料
            self.load_data(file_path)
            
            # 2. 清理資料
            self.clean_data(remove_outliers=remove_outliers)
            
            # 3. 計算 RFM
            self.calculate_rfm(analysis_date=analysis_date)
            
            # 4. 客戶分群
            self.segment_customers(rfm_bins=rfm_bins)
            
            # 5. 建立視覺化
            if create_plots:
                self.create_visualizations()
            
            # 6. 匯出結果
            exported_files = {}
            if export_results:
                exported_files = self.export_results()
            
            # 生成分析摘要
            summary = self.generate_analysis_summary()
            summary['exported_files'] = exported_files
            
            self.logger.info("🎉 完整分析流程完成 Full analysis pipeline completed")
            return summary
            
        except Exception as e:
            self.logger.error(f"❌ 分析流程失敗 Analysis pipeline failed: {e}")
            raise
    
    def generate_analysis_summary(self) -> Dict:
        """
        生成分析摘要報告
        
        Returns:
            Dict: 分析摘要
        """
        if self.segmented_data is None:
            raise ValueError("請先完成分析 Please complete analysis first")
        
        # 基本統計
        cleaning_summary = self.cleaner.get_cleaning_summary()
        segment_summary = self.rfm_calculator.get_segment_summary(self.segmented_data)
        
        summary = {
            'data_overview': {
                'original_records': cleaning_summary['original_count'],
                'cleaned_records': cleaning_summary['final_count'],
                'retention_rate': cleaning_summary['retention_rate'],
                'customers_analyzed': len(self.rfm_data),
                'date_range': {
                    'start': self.cleaned_data['InvoiceDate'].min().date().isoformat(),
                    'end': self.cleaned_data['InvoiceDate'].max().date().isoformat()
                }
            },
            'rfm_statistics': {
                'avg_recency': float(self.rfm_data['Recency'].mean()),
                'avg_frequency': float(self.rfm_data['Frequency'].mean()),
                'avg_monetary': float(self.rfm_data['Monetary'].mean()),
                'total_revenue': float(self.rfm_data['Monetary'].sum())
            },
            'segmentation_results': {
                'total_segments': self.segmented_data['Customer_Segment'].nunique(),
                'top_segments': segment_summary.head(3).to_dict('index')
            }
        }
        
        return summary
    
    def get_business_insights(self) -> Dict:
        """
        獲取業務洞察
        
        Returns:
            Dict: 業務洞察和建議
        """
        if self.segmented_data is None:
            raise ValueError("請先完成分析 Please complete analysis first")
        
        insights = {}
        
        # 高價值客戶分析
        champions = self.segmented_data[
            self.segmented_data['Customer_Segment'] == 'Champions'
        ]
        if len(champions) > 0:
            champions_revenue = champions['Monetary'].sum()
            champions_percentage = len(champions) / len(self.segmented_data) * 100
            insights['champions'] = {
                'count': len(champions),
                'percentage': champions_percentage,
                'revenue_contribution': champions_revenue,
                'avg_clv': champions['CLV'].mean() if 'CLV' in champions.columns else None
            }
        
        # 風險客戶分析
        at_risk = self.segmented_data[
            self.segmented_data['Customer_Segment'].isin(['At Risk', 'Cannot Lose Them'])
        ]
        if len(at_risk) > 0:
            insights['at_risk'] = {
                'count': len(at_risk),
                'percentage': len(at_risk) / len(self.segmented_data) * 100,
                'potential_loss': at_risk['Monetary'].sum()
            }
        
        return insights
