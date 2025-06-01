"""
資料視覺化模組 - Data Visualization Module

提供客戶分群分析的視覺化功能，支援中文字體顯示。
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, List
import warnings

from customer_segmentation.utils.config import get_config
from customer_segmentation.utils.logger import LoggerMixin, get_logger

# 忽略警告
warnings.filterwarnings('ignore')

logger = get_logger(__name__)


class DataVisualizer(LoggerMixin):
    """
    資料視覺化器
    
    提供各種圖表生成功能，支援中文字體顯示。
    """
    
    def __init__(self, style: str = "seaborn-v0_8", figsize: tuple = (12, 8)):
        """
        初始化視覺化器
        
        Args:
            style: matplotlib 樣式
            figsize: 圖表大小
        """
        self.config = get_config()
        self.style = style
        self.figsize = figsize
        
        # 設置中文字體
        self._setup_chinese_fonts()
        
        # 設置樣式
        self._setup_style()
        
        self.logger.info("🎨 資料視覺化器初始化完成 Data visualizer initialized")
    
    def _setup_chinese_fonts(self):
        """設置中文字體支援"""
        try:
            # 重新載入字體管理器
            fm.fontManager.__init__()
            
            # 嘗試設置中文字體（按優先順序）
            chinese_fonts = [
                'WenQuanYi Micro Hei',  # 文泉驛微米黑（已安裝）
                'Noto Sans CJK SC',     # Google Noto 字體
                'Noto Serif CJK SC',    # Google Noto 襯線字體
                'SimHei',               # 黑體
                'Microsoft YaHei',      # 微軟雅黑
                'Source Han Sans SC',   # 思源黑體
                'DejaVu Sans',          # 通用字體（備用）
            ]
            
            # 檢查可用字體
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            
            font_found = False
            selected_font = None
            for font in chinese_fonts:
                if font in available_fonts:
                    selected_font = font
                    font_found = True
                    self.logger.info(f"✅ 使用中文字體 Using Chinese font: {font}")
                    break
            
            if font_found:
                # 設置字體優先順序
                plt.rcParams['font.sans-serif'] = [selected_font] + ['DejaVu Sans', 'Arial', 'sans-serif']
            else:
                # 如果沒有找到中文字體，使用 DejaVu Sans
                plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
                self.logger.warning("⚠️ 未找到中文字體，使用 DejaVu Sans No Chinese font found, using DejaVu Sans")
            
            # 設置負號正常顯示
            plt.rcParams['axes.unicode_minus'] = False
            
            # 忽略字體警告
            warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
            
        except Exception as e:
            self.logger.warning(f"⚠️ 字體設置失敗 Font setup failed: {e}")
            # 使用默認字體
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
            plt.rcParams['axes.unicode_minus'] = False
    
    def _setup_style(self):
        """設置圖表樣式"""
        try:
            # 設置 matplotlib 樣式
            if self.style in plt.style.available:
                plt.style.use(self.style)
            else:
                plt.style.use('default')
                self.logger.warning(f"⚠️ 樣式 {self.style} 不可用，使用默認樣式")
            
            # 設置 seaborn 樣式
            sns.set_palette("husl")
            
            # 設置圖表參數
            plt.rcParams.update({
                'figure.figsize': self.figsize,
                'figure.dpi': self.config.dpi,
                'savefig.dpi': self.config.dpi,
                'font.size': 10,
                'axes.titlesize': 14,
                'axes.labelsize': 12,
                'xtick.labelsize': 10,
                'ytick.labelsize': 10,
                'legend.fontsize': 10,
                'figure.titlesize': 16
            })
            
        except Exception as e:
            self.logger.warning(f"⚠️ 樣式設置失敗 Style setup failed: {e}")
    
    def plot_rfm_distributions(self, rfm_data: pd.DataFrame, save_path: Optional[Path] = None):
        """
        繪製 RFM 分布圖
        
        Args:
            rfm_data: RFM 資料
            save_path: 儲存路徑
        """
        try:
            # 確保字體設置正確
            self._setup_chinese_fonts()
            
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('RFM 指標分布分析 RFM Metrics Distribution Analysis', fontsize=16, y=0.98)
            
            # Recency 分布
            axes[0, 0].hist(rfm_data['Recency'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
            axes[0, 0].set_title('Recency 近期性 Distribution\n(距離上次購買天數 Days since last purchase)')
            axes[0, 0].set_xlabel('Recency (天 Days)')
            axes[0, 0].set_ylabel('客戶數量 Customer Count')
            axes[0, 0].grid(True, alpha=0.3)
            
            # Frequency 分布
            axes[0, 1].hist(rfm_data['Frequency'], bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
            axes[0, 1].set_title('Frequency 頻率性 Distribution\n(交易次數 Number of transactions)')
            axes[0, 1].set_xlabel('Frequency (次 Transactions)')
            axes[0, 1].set_ylabel('客戶數量 Customer Count')
            axes[0, 1].grid(True, alpha=0.3)
            
            # Monetary 分布
            axes[0, 2].hist(rfm_data['Monetary'], bins=50, alpha=0.7, color='lightcoral', edgecolor='black')
            axes[0, 2].set_title('Monetary 購買力 Distribution\n(總消費金額 Total amount spent)')
            axes[0, 2].set_xlabel('Monetary (英鎊 GBP £)')
            axes[0, 2].set_ylabel('客戶數量 Customer Count')
            axes[0, 2].grid(True, alpha=0.3)
            
            # Recency 箱線圖
            axes[1, 0].boxplot(rfm_data['Recency'])
            axes[1, 0].set_title('Recency 近期性 Box Plot')
            axes[1, 0].set_ylabel('Recency (天 Days)')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Frequency 箱線圖
            axes[1, 1].boxplot(rfm_data['Frequency'])
            axes[1, 1].set_title('Frequency 頻率性 Box Plot')
            axes[1, 1].set_ylabel('Frequency (次 Transactions)')
            axes[1, 1].grid(True, alpha=0.3)
            
            # Monetary 箱線圖 (95% 分位數)
            monetary_95 = rfm_data['Monetary'].quantile(0.95)
            monetary_filtered = rfm_data[rfm_data['Monetary'] <= monetary_95]['Monetary']
            axes[1, 2].boxplot(monetary_filtered)
            axes[1, 2].set_title('Monetary 購買力 Box Plot\n(95% quantile)')
            axes[1, 2].set_ylabel('Monetary (英鎊 GBP £)')
            axes[1, 2].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path / 'rfm_distributions.png', dpi=self.config.dpi, bbox_inches='tight')
                self.logger.info(f"📊 RFM 分布圖已儲存 RFM distribution plot saved: {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"❌ RFM 分布圖繪製失敗 RFM distribution plot failed: {e}")
            raise
    
    def plot_rfm_correlation(self, rfm_data: pd.DataFrame, save_path: Optional[Path] = None):
        """
        繪製 RFM 相關性熱力圖
        
        Args:
            rfm_data: RFM 資料
            save_path: 儲存路徑
        """
        try:
            # 確保字體設置正確
            self._setup_chinese_fonts()
            
            plt.figure(figsize=(10, 8))
            
            # 計算相關性矩陣
            correlation_matrix = rfm_data[['Recency', 'Frequency', 'Monetary']].corr()
            
            # 繪製熱力圖
            sns.heatmap(correlation_matrix, 
                       annot=True, 
                       cmap='coolwarm', 
                       center=0,
                       square=True,
                       fmt='.3f',
                       cbar_kws={'label': '相關係數 Correlation Coefficient'})
            
            plt.title('RFM 指標相關性分析 RFM Metrics Correlation Analysis', fontsize=14, pad=20)
            plt.xlabel('RFM 指標 RFM Metrics')
            plt.ylabel('RFM 指標 RFM Metrics')
            
            if save_path:
                plt.savefig(save_path / 'rfm_correlation.png', dpi=self.config.dpi, bbox_inches='tight')
                self.logger.info(f"🔗 RFM 相關性圖已儲存 RFM correlation plot saved: {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"❌ RFM 相關性圖繪製失敗 RFM correlation plot failed: {e}")
            raise
    
    def plot_customer_segments(self, segmented_data: pd.DataFrame, save_path: Optional[Path] = None):
        """
        繪製客戶分群分析圖
        
        Args:
            segmented_data: 分群後的客戶資料
            save_path: 儲存路徑
        """
        try:
            # 確保字體設置正確
            self._setup_chinese_fonts()
            
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('客戶分群分析 Customer Segmentation Analysis', fontsize=16, y=0.98)
            
            # 1. 分群數量分布
            segment_counts = segmented_data['Customer_Segment'].value_counts()
            axes[0, 0].pie(segment_counts.values, 
                          labels=segment_counts.index, 
                          autopct='%1.1f%%',
                          startangle=90)
            axes[0, 0].set_title('客戶分群分布 Customer Segment Distribution')
            
            # 2. 各分群的 RFM 平均值（標準化顯示）
            segment_rfm = segmented_data.groupby('Customer_Segment')[['Recency', 'Frequency', 'Monetary']].mean()
            
            # 標準化數據以便在同一圖表中顯示
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            segment_rfm_normalized = pd.DataFrame(
                scaler.fit_transform(segment_rfm),
                index=segment_rfm.index,
                columns=segment_rfm.columns
            )
            
            segment_rfm_normalized.plot(kind='bar', ax=axes[0, 1], 
                                      color=['lightcoral', 'gold', 'lightgreen'])
            axes[0, 1].set_title('各分群 RFM 標準化平均值\nAverage RFM by Segment (Standardized)')
            axes[0, 1].set_xlabel('客戶分群 Customer Segment')
            axes[0, 1].set_ylabel('標準化數值 Standardized Value')
            axes[0, 1].legend(['Recency', 'Frequency', 'Monetary'])
            axes[0, 1].tick_params(axis='x', rotation=45)
            axes[0, 1].grid(True, alpha=0.3)
            
            # 添加零線參考
            axes[0, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
            
            # 3. 分群的營收貢獻
            segment_revenue = segmented_data.groupby('Customer_Segment')['Monetary'].sum().sort_values(ascending=False)
            axes[1, 0].bar(range(len(segment_revenue)), segment_revenue.values, color='lightblue')
            axes[1, 0].set_title('各分群營收貢獻 Revenue Contribution by Segment')
            axes[1, 0].set_xlabel('客戶分群 Customer Segment')
            axes[1, 0].set_ylabel('總營收 Total Revenue (英鎊 GBP £)')
            axes[1, 0].set_xticks(range(len(segment_revenue)))
            axes[1, 0].set_xticklabels(segment_revenue.index, rotation=45)
            
            # 4. RFM 分數散點圖
            if 'RFM_Score' in segmented_data.columns:
                for segment in segmented_data['Customer_Segment'].unique():
                    segment_data = segmented_data[segmented_data['Customer_Segment'] == segment]
                    axes[1, 1].scatter(segment_data['Frequency'], 
                                     segment_data['Monetary'], 
                                     label=segment, 
                                     alpha=0.6)
                
                axes[1, 1].set_title('客戶分群散點圖 Customer Segment Scatter Plot')
                axes[1, 1].set_xlabel('Frequency 頻率性 (次 Transactions)')
                axes[1, 1].set_ylabel('Monetary 購買力 (英鎊 GBP £)')
                axes[1, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path / 'customer_segments.png', dpi=self.config.dpi, bbox_inches='tight')
                self.logger.info(f"👥 客戶分群圖已儲存 Customer segments plot saved: {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"❌ 客戶分群圖繪製失敗 Customer segments plot failed: {e}")
            raise
    
    def plot_time_series_analysis(self, data: pd.DataFrame, save_path: Optional[Path] = None):
        """
        繪製時間序列分析圖
        
        Args:
            data: 清理後的交易資料
            save_path: 儲存路徑
        """
        try:
            # 確保字體設置正確
            self._setup_chinese_fonts()
            
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('時間序列分析 Time Series Analysis', fontsize=16, y=0.98)
            
            # 準備時間序列資料
            data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
            data['YearMonth'] = data['InvoiceDate'].dt.to_period('M')
            data['TotalAmount'] = data['Quantity'] * data['UnitPrice']
            
            # 1. 月度銷售趨勢
            monthly_sales = data.groupby('YearMonth')['TotalAmount'].sum()
            axes[0, 0].plot(monthly_sales.index.astype(str), monthly_sales.values, marker='o')
            axes[0, 0].set_title('月度銷售趨勢 Monthly Sales Trend')
            axes[0, 0].set_xlabel('年月 Year-Month')
            axes[0, 0].set_ylabel('銷售額 Sales Amount ($)')
            axes[0, 0].tick_params(axis='x', rotation=45)
            axes[0, 0].grid(True, alpha=0.3)
            
            # 2. 月度交易數量
            monthly_transactions = data.groupby('YearMonth').size()
            axes[0, 1].plot(monthly_transactions.index.astype(str), monthly_transactions.values, 
                           marker='s', color='orange')
            axes[0, 1].set_title('月度交易數量 Monthly Transaction Count')
            axes[0, 1].set_xlabel('年月 Year-Month')
            axes[0, 1].set_ylabel('交易數量 Transaction Count')
            axes[0, 1].tick_params(axis='x', rotation=45)
            axes[0, 1].grid(True, alpha=0.3)
            
            # 3. 月度新客戶數
            first_purchase = data.groupby('CustomerID')['InvoiceDate'].min().dt.to_period('M')
            monthly_new_customers = first_purchase.value_counts().sort_index()
            axes[1, 0].bar(monthly_new_customers.index.astype(str), monthly_new_customers.values, 
                          color='lightgreen')
            axes[1, 0].set_title('月度新客戶數 Monthly New Customers')
            axes[1, 0].set_xlabel('年月 Year-Month')
            axes[1, 0].set_ylabel('新客戶數 New Customer Count')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # 4. 平均訂單價值
            monthly_aov = data.groupby('YearMonth')['TotalAmount'].mean()
            axes[1, 1].plot(monthly_aov.index.astype(str), monthly_aov.values, 
                           marker='^', color='red')
            axes[1, 1].set_title('月度平均訂單價值 Monthly Average Order Value')
            axes[1, 1].set_xlabel('年月 Year-Month')
            axes[1, 1].set_ylabel('平均訂單價值 AOV ($)')
            axes[1, 1].tick_params(axis='x', rotation=45)
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path / 'time_series_analysis.png', dpi=self.config.dpi, bbox_inches='tight')
                self.logger.info(f"📅 時間序列圖已儲存 Time series plot saved: {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"❌ 時間序列圖繪製失敗 Time series plot failed: {e}")
            raise
    
    def plot_geographic_analysis(self, data: pd.DataFrame, save_path: Optional[Path] = None):
        """
        繪製地理分析圖
        
        Args:
            data: 清理後的交易資料
            save_path: 儲存路徑
        """
        try:
            # 確保字體設置正確
            self._setup_chinese_fonts()
            
            fig, axes = plt.subplots(1, 2, figsize=(16, 6))
            fig.suptitle('地理分析 Geographic Analysis', fontsize=16, y=1.02)
            
            # 準備地理資料
            data['TotalAmount'] = data['Quantity'] * data['UnitPrice']
            
            # 1. 各國銷售額
            country_sales = data.groupby('Country')['TotalAmount'].sum().sort_values(ascending=False).head(10)
            axes[0].barh(range(len(country_sales)), country_sales.values)
            axes[0].set_title('前10名國家銷售額 Top 10 Countries by Sales')
            axes[0].set_xlabel('銷售額 Sales Amount ($)')
            axes[0].set_ylabel('國家 Country')
            axes[0].set_yticks(range(len(country_sales)))
            axes[0].set_yticklabels(country_sales.index)
            
            # 2. 各國客戶數
            country_customers = data.groupby('Country')['CustomerID'].nunique().sort_values(ascending=False).head(10)
            axes[1].barh(range(len(country_customers)), country_customers.values, color='lightcoral')
            axes[1].set_title('前10名國家客戶數 Top 10 Countries by Customer Count')
            axes[1].set_xlabel('客戶數 Customer Count')
            axes[1].set_ylabel('國家 Country')
            axes[1].set_yticks(range(len(country_customers)))
            axes[1].set_yticklabels(country_customers.index)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path / 'geographic_analysis.png', dpi=self.config.dpi, bbox_inches='tight')
                self.logger.info(f"🌍 地理分析圖已儲存 Geographic analysis plot saved: {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"❌ 地理分析圖繪製失敗 Geographic analysis plot failed: {e}")
            raise
    
    def create_interactive_rfm_plot(self, rfm_data: pd.DataFrame, save_path: Optional[Path] = None):
        """
        建立互動式 RFM 圖表
        
        Args:
            rfm_data: RFM 資料
            save_path: 儲存路徑
        """
        try:
            # 建立子圖
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('RFM 3D 散點圖 RFM 3D Scatter', 
                               'Recency vs Frequency', 
                               'Frequency vs Monetary', 
                               'Recency vs Monetary'),
                specs=[[{"type": "scatter3d"}, {"type": "scatter"}],
                       [{"type": "scatter"}, {"type": "scatter"}]]
            )
            
            # 3D 散點圖
            fig.add_trace(
                go.Scatter3d(
                    x=rfm_data['Recency'],
                    y=rfm_data['Frequency'],
                    z=rfm_data['Monetary'],
                    mode='markers',
                    marker=dict(
                        size=3,
                        color=rfm_data['Monetary'],
                        colorscale='Viridis',
                        showscale=True
                    ),
                    text=rfm_data.index,
                    name='Customers'
                ),
                row=1, col=1
            )
            
            # 2D 散點圖
            fig.add_trace(
                go.Scatter(
                    x=rfm_data['Recency'],
                    y=rfm_data['Frequency'],
                    mode='markers',
                    marker=dict(color='blue', size=4),
                    name='R vs F'
                ),
                row=1, col=2
            )
            
            fig.add_trace(
                go.Scatter(
                    x=rfm_data['Frequency'],
                    y=rfm_data['Monetary'],
                    mode='markers',
                    marker=dict(color='green', size=4),
                    name='F vs M'
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=rfm_data['Recency'],
                    y=rfm_data['Monetary'],
                    mode='markers',
                    marker=dict(color='red', size=4),
                    name='R vs M'
                ),
                row=2, col=2
            )
            
            # 更新佈局
            fig.update_layout(
                title_text="互動式 RFM 分析 Interactive RFM Analysis",
                showlegend=False,
                height=800
            )
            
            if save_path:
                fig.write_html(save_path / 'interactive_rfm_plot.html')
                self.logger.info(f"🎮 互動式 RFM 圖已儲存 Interactive RFM plot saved: {save_path}")
            
            fig.show()
            
        except Exception as e:
            self.logger.error(f"❌ 互動式 RFM 圖建立失敗 Interactive RFM plot failed: {e}")
            raise
    
    def save_all_plots(self, rfm_data: pd.DataFrame, segmented_data: pd.DataFrame, 
                      cleaned_data: pd.DataFrame, output_dir: Optional[Path] = None):
        """
        儲存所有圖表
        
        Args:
            rfm_data: RFM 資料
            segmented_data: 分群資料
            cleaned_data: 清理後的資料
            output_dir: 輸出目錄
        """
        if output_dir is None:
            output_dir = Path("plots")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            self.logger.info("📊 開始儲存所有圖表 Starting to save all plots")
            
            # 儲存各種圖表
            self.plot_rfm_distributions(rfm_data, output_dir)
            self.plot_rfm_correlation(rfm_data, output_dir)
            self.plot_customer_segments(segmented_data, output_dir)
            self.plot_time_series_analysis(cleaned_data, output_dir)
            self.plot_geographic_analysis(cleaned_data, output_dir)
            self.create_interactive_rfm_plot(rfm_data, output_dir)
            
            self.logger.info(f"✅ 所有圖表已儲存至 All plots saved to: {output_dir}")
            
        except Exception as e:
            self.logger.error(f"❌ 圖表儲存失敗 Plot saving failed: {e}")
            raise
