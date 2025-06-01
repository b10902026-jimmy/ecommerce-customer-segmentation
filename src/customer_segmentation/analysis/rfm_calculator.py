"""
RFM 計算模組 - RFM Calculator Module
負責計算 Recency, Frequency, Monetary 指標
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional

class RFMCalculator:
    """RFM 計算器類別"""
    
    def __init__(self, df: pd.DataFrame, customer_id_col: str = 'CustomerID',
                 date_col: str = 'InvoiceDate', invoice_col: str = 'InvoiceNo',
                 monetary_col: str = 'TotalPrice'):
        """
        初始化 RFM 計算器
        
        Args:
            df (pd.DataFrame): 清理後的資料框
            customer_id_col (str): 客戶ID欄位名稱
            date_col (str): 日期欄位名稱
            invoice_col (str): 發票號碼欄位名稱
            monetary_col (str): 金額欄位名稱
        """
        self.df = df.copy()
        self.customer_id_col = customer_id_col
        self.date_col = date_col
        self.invoice_col = invoice_col
        self.monetary_col = monetary_col
        self.rfm_df = None
        self.analysis_date = None
        
        # 驗證必要欄位
        self._validate_columns()
        
    def _validate_columns(self) -> None:
        """驗證必要欄位是否存在"""
        required_cols = [self.customer_id_col, self.date_col, 
                        self.invoice_col, self.monetary_col]
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        
        if missing_cols:
            raise ValueError(f"缺少必要欄位 Missing required columns: {missing_cols}")
            
        # 確保日期欄位是 datetime 格式
        if not pd.api.types.is_datetime64_any_dtype(self.df[self.date_col]):
            print(f"⚠️ 轉換 {self.date_col} 為 datetime 格式...")
            self.df[self.date_col] = pd.to_datetime(self.df[self.date_col])
    
    def set_analysis_date(self, analysis_date: Optional[datetime] = None) -> datetime:
        """
        設定分析日期
        
        Args:
            analysis_date (Optional[datetime]): 分析日期，如果為 None 則使用資料最後日期+1天
            
        Returns:
            datetime: 分析日期
        """
        if analysis_date is None:
            self.analysis_date = self.df[self.date_col].max() + timedelta(days=1)
        else:
            self.analysis_date = analysis_date
            
        print(f"📅 分析日期 Analysis date: {self.analysis_date.date()}")
        print(f"📅 資料最後日期 Last data date: {self.df[self.date_col].max().date()}")
        
        return self.analysis_date
    
    def calculate_recency(self) -> pd.Series:
        """
        計算 Recency（最近一次購買距今天數）
        
        Returns:
            pd.Series: 每位客戶的 Recency 值
        """
        if self.analysis_date is None:
            self.set_analysis_date()
            
        print("🔢 計算 Recency (最近購買天數)...")
        
        recency = self.df.groupby(self.customer_id_col)[self.date_col].max()
        recency = (self.analysis_date - recency).dt.days
        
        print(f"✅ Recency 計算完成，範圍: {recency.min()} - {recency.max()} 天")
        
        return recency
    
    def calculate_frequency(self) -> pd.Series:
        """
        計算 Frequency（購買頻率 - 交易次數）
        
        Returns:
            pd.Series: 每位客戶的 Frequency 值
        """
        print("🔢 計算 Frequency (購買頻率)...")
        
        frequency = self.df.groupby(self.customer_id_col)[self.invoice_col].nunique()
        
        print(f"✅ Frequency 計算完成，範圍: {frequency.min()} - {frequency.max()} 次")
        
        return frequency
    
    def calculate_monetary(self) -> pd.Series:
        """
        計算 Monetary（購買金額總和）
        
        Returns:
            pd.Series: 每位客戶的 Monetary 值
        """
        print("🔢 計算 Monetary (購買金額)...")
        
        monetary = self.df.groupby(self.customer_id_col)[self.monetary_col].sum()
        
        print(f"✅ Monetary 計算完成，範圍: ${monetary.min():.2f} - ${monetary.max():.2f}")
        
        return monetary
    
    def calculate_rfm(self, analysis_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        計算完整的 RFM 指標
        
        Args:
            analysis_date (Optional[datetime]): 分析日期
            
        Returns:
            pd.DataFrame: RFM 資料框
        """
        print("🎯 開始計算 RFM 指標 Starting RFM calculation...")
        print("=" * 50)
        
        # 設定分析日期
        self.set_analysis_date(analysis_date)
        
        # 計算各項指標
        recency = self.calculate_recency()
        frequency = self.calculate_frequency()
        monetary = self.calculate_monetary()
        
        # 合併成 RFM 資料框
        self.rfm_df = pd.DataFrame({
            'CustomerID': recency.index,
            'Recency': recency.values,
            'Frequency': frequency.values,
            'Monetary': monetary.values
        }).reset_index(drop=True)
        
        print(f"\n✅ RFM 計算完成 RFM calculation completed!")
        print(f"客戶數量 Number of customers: {len(self.rfm_df):,}")
        
        return self.rfm_df
    
    def get_rfm_summary(self) -> pd.DataFrame:
        """
        獲取 RFM 統計摘要
        
        Returns:
            pd.DataFrame: RFM 統計摘要
        """
        if self.rfm_df is None:
            raise ValueError("請先計算 RFM 指標 Please calculate RFM first")
            
        return self.rfm_df[['Recency', 'Frequency', 'Monetary']].describe()
    
    def print_rfm_summary(self) -> None:
        """列印 RFM 統計摘要"""
        if self.rfm_df is None:
            raise ValueError("請先計算 RFM 指標 Please calculate RFM first")
            
        print("\n📊 RFM 統計摘要 RFM Statistical Summary")
        print("=" * 50)
        summary = self.get_rfm_summary()
        print(summary.to_string())
        
        # 檢查異常值
        print("\n⚠️ 異常值檢查 Outlier Check:")
        print(f"Recency 最大值 Max: {self.rfm_df['Recency'].max()} 天 days")
        print(f"Frequency 最大值 Max: {self.rfm_df['Frequency'].max()} 次 transactions")
        print(f"Monetary 最大值 Max: ${self.rfm_df['Monetary'].max():,.2f}")
        print(f"Monetary 最小值 Min: ${self.rfm_df['Monetary'].min():,.2f}")
    
    def calculate_rfm_scores(self, r_bins: int = 5, f_bins: int = 5, m_bins: int = 5) -> pd.DataFrame:
        """
        計算 RFM 分數（1-5 分）
        
        Args:
            r_bins (int): Recency 分組數
            f_bins (int): Frequency 分組數
            m_bins (int): Monetary 分組數
            
        Returns:
            pd.DataFrame: 包含 RFM 分數的資料框
        """
        if self.rfm_df is None:
            raise ValueError("請先計算 RFM 指標 Please calculate RFM first")
            
        print("🏆 計算 RFM 分數 Calculating RFM scores...")
        
        rfm_scores = self.rfm_df.copy()
        
        # 計算分數（Recency 越小越好，所以要反轉）
        rfm_scores['R_Score'] = pd.qcut(rfm_scores['Recency'], r_bins, labels=range(r_bins, 0, -1))
        rfm_scores['F_Score'] = pd.qcut(rfm_scores['Frequency'].rank(method='first'), f_bins, labels=range(1, f_bins + 1))
        rfm_scores['M_Score'] = pd.qcut(rfm_scores['Monetary'].rank(method='first'), m_bins, labels=range(1, m_bins + 1))
        
        # 轉換為數值
        rfm_scores['R_Score'] = rfm_scores['R_Score'].astype(int)
        rfm_scores['F_Score'] = rfm_scores['F_Score'].astype(int)
        rfm_scores['M_Score'] = rfm_scores['M_Score'].astype(int)
        
        # 計算綜合分數
        rfm_scores['RFM_Score'] = rfm_scores['R_Score'].astype(str) + \
                                 rfm_scores['F_Score'].astype(str) + \
                                 rfm_scores['M_Score'].astype(str)
        
        print("✅ RFM 分數計算完成 RFM scores calculated!")
        
        return rfm_scores
    
    def segment_customers(self, rfm_scores_df: pd.DataFrame) -> pd.DataFrame:
        """
        根據 RFM 分數進行客戶分群
        
        Args:
            rfm_scores_df (pd.DataFrame): 包含 RFM 分數的資料框
            
        Returns:
            pd.DataFrame: 包含客戶分群的資料框
        """
        print("👥 進行客戶分群 Customer segmentation...")
        
        segmented_df = rfm_scores_df.copy()
        
        def segment_customers_func(row):
            """根據 RFM 分數定義客戶群體"""
            r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
            
            # 高價值客戶 Champions
            if r >= 4 and f >= 4 and m >= 4:
                return 'Champions'
            # 忠實客戶 Loyal Customers
            elif r >= 3 and f >= 4 and m >= 3:
                return 'Loyal Customers'
            # 潛在忠實客戶 Potential Loyalists
            elif r >= 3 and f >= 2 and m >= 2:
                return 'Potential Loyalists'
            # 新客戶 New Customers
            elif r >= 4 and f <= 2 and m <= 2:
                return 'New Customers'
            # 有前景客戶 Promising
            elif r >= 3 and f <= 2 and m <= 2:
                return 'Promising'
            # 需要關注客戶 Need Attention
            elif r >= 2 and f >= 2 and m >= 2:
                return 'Need Attention'
            # 即將流失客戶 About to Sleep
            elif r <= 2 and f >= 2 and m >= 2:
                return 'About to Sleep'
            # 有風險客戶 At Risk
            elif r <= 2 and f >= 3 and m >= 3:
                return 'At Risk'
            # 無法挽回客戶 Cannot Lose Them
            elif r <= 1 and f >= 4 and m >= 4:
                return 'Cannot Lose Them'
            # 冬眠客戶 Hibernating
            elif r <= 2 and f <= 2 and m <= 2:
                return 'Hibernating'
            # 已流失客戶 Lost
            else:
                return 'Lost'
        
        segmented_df['Customer_Segment'] = segmented_df.apply(segment_customers_func, axis=1)
        
        print("✅ 客戶分群完成 Customer segmentation completed!")
        
        return segmented_df
    
    def get_segment_summary(self, segmented_df: pd.DataFrame) -> pd.DataFrame:
        """
        獲取客戶分群摘要
        
        Args:
            segmented_df (pd.DataFrame): 包含客戶分群的資料框
            
        Returns:
            pd.DataFrame: 分群摘要統計
        """
        summary = segmented_df.groupby('Customer_Segment').agg({
            'CustomerID': 'count',
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': ['mean', 'sum']
        }).round(2)
        
        # 扁平化欄位名稱
        summary.columns = ['Customer_Count', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Total_Monetary']
        
        # 計算百分比
        summary['Percentage'] = (summary['Customer_Count'] / len(segmented_df) * 100).round(2)
        
        # 按客戶數量排序
        summary = summary.sort_values('Customer_Count', ascending=False)
        
        return summary
    
    def print_segment_summary(self, segmented_df: pd.DataFrame) -> None:
        """列印客戶分群摘要"""
        print("\n👥 客戶分群摘要 Customer Segment Summary")
        print("=" * 80)
        
        summary = self.get_segment_summary(segmented_df)
        print(summary.to_string())
        
        print(f"\n📊 分群統計 Segment Statistics:")
        print(f"總客戶數 Total customers: {len(segmented_df):,}")
        print(f"分群數量 Number of segments: {segmented_df['Customer_Segment'].nunique()}")
        
        # 顯示前三大客戶群
        top_segments = summary.head(3)
        print(f"\n🏆 前三大客戶群 Top 3 segments:")
        for idx, (segment, row) in enumerate(top_segments.iterrows(), 1):
            print(f"{idx}. {segment}: {row['Customer_Count']:,} 客戶 ({row['Percentage']:.1f}%)")
    
    def calculate_customer_lifetime_value(self, segmented_df: pd.DataFrame, 
                                        avg_lifespan_days: int = 365) -> pd.DataFrame:
        """
        計算客戶終身價值 (CLV)
        
        Args:
            segmented_df (pd.DataFrame): 包含客戶分群的資料框
            avg_lifespan_days (int): 平均客戶生命週期（天）
            
        Returns:
            pd.DataFrame: 包含 CLV 的資料框
        """
        print("💰 計算客戶終身價值 Calculating Customer Lifetime Value...")
        
        clv_df = segmented_df.copy()
        
        # 計算平均訂單價值 (AOV)
        clv_df['AOV'] = clv_df['Monetary'] / clv_df['Frequency']
        
        # 計算購買頻率（每年）
        clv_df['Purchase_Frequency_Yearly'] = clv_df['Frequency'] * (365 / (365 - clv_df['Recency'] + 1))
        
        # 計算客戶終身價值
        clv_df['CLV'] = clv_df['AOV'] * clv_df['Purchase_Frequency_Yearly'] * (avg_lifespan_days / 365)
        
        print("✅ 客戶終身價值計算完成 CLV calculation completed!")
        
        return clv_df
    
    def export_rfm_results(self, segmented_df: pd.DataFrame, 
                          filename: str = 'rfm_analysis_results.csv') -> None:
        """
        匯出 RFM 分析結果
        
        Args:
            segmented_df (pd.DataFrame): 包含完整分析結果的資料框
            filename (str): 輸出檔案名稱
        """
        try:
            segmented_df.to_csv(filename, index=False, encoding='utf-8')
            print(f"✅ RFM 分析結果已匯出至 {filename}")
        except Exception as e:
            print(f"❌ 匯出失敗 Export failed: {e}")

def main():
    """主函數 - 示範用法"""
    from data_loader import DataLoader
    from data_cleaner import DataCleaner
    
    # 載入和清理資料
    loader = DataLoader('data.csv')
    df = loader.load_data()
    
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean_all()
    
    # 建立 RFM 計算器
    rfm_calc = RFMCalculator(cleaned_df)
    
    # 計算 RFM 指標
    rfm_df = rfm_calc.calculate_rfm()
    
    # 顯示 RFM 摘要
    rfm_calc.print_rfm_summary()
    
    # 計算 RFM 分數
    rfm_scores = rfm_calc.calculate_rfm_scores()
    
    # 進行客戶分群
    segmented_customers = rfm_calc.segment_customers(rfm_scores)
    
    # 顯示分群摘要
    rfm_calc.print_segment_summary(segmented_customers)
    
    # 計算客戶終身價值
    clv_results = rfm_calc.calculate_customer_lifetime_value(segmented_customers)
    
    # 匯出結果
    rfm_calc.export_rfm_results(clv_results)
    
    return clv_results

if __name__ == "__main__":
    results = main()
