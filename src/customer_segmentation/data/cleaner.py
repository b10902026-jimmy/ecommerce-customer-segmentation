"""
資料清理模組 - Data Cleaner Module
負責清理和前處理資料
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class DataCleaner:
    """資料清理器類別"""
    
    def __init__(self, df: pd.DataFrame):
        """
        初始化資料清理器
        
        Args:
            df (pd.DataFrame): 原始資料框
        """
        self.original_df = df.copy()
        self.df = df.copy()
        self.cleaning_log = []
        self.cleaning_log.append(f"原始資料 Original data: {len(self.df):,} records")
        
    def convert_date_format(self, date_column: str = 'InvoiceDate') -> pd.DataFrame:
        """
        轉換日期格式
        
        Args:
            date_column (str): 日期欄位名稱
            
        Returns:
            pd.DataFrame: 處理後的資料框
        """
        print(f"📅 轉換日期格式 Converting date format for {date_column}...")
        
        try:
            self.df[date_column] = pd.to_datetime(self.df[date_column])
            print(f"✅ 日期轉換完成 Date conversion completed")
            print(f"日期範圍 Date range: {self.df[date_column].min()} to {self.df[date_column].max()}")
        except Exception as e:
            print(f"❌ 日期轉換失敗 Date conversion failed: {e}")
            raise
            
        return self.df
    
    def remove_cancelled_transactions(self, invoice_column: str = 'InvoiceNo') -> pd.DataFrame:
        """
        移除取消交易（發票號碼以 'C' 開頭）
        
        Args:
            invoice_column (str): 發票號碼欄位名稱
            
        Returns:
            pd.DataFrame: 處理後的資料框
        """
        print("❌ 移除取消交易 Removing cancelled transactions...")
        
        before_count = len(self.df)
        self.df = self.df[~self.df[invoice_column].astype(str).str.startswith('C')]
        after_count = len(self.df)
        removed_count = before_count - after_count
        
        print(f"移除取消交易 Removed cancelled transactions: {removed_count:,}")
        self.cleaning_log.append(f"移除取消交易 Removed cancelled: {removed_count:,} records")
        print(f"剩餘資料 Remaining data: {after_count:,}")
        
        return self.df
    
    def remove_invalid_records(self, quantity_column: str = 'Quantity', 
                             price_column: str = 'UnitPrice') -> pd.DataFrame:
        """
        移除無效記錄（負數量、零數量、零價格、負價格）
        
        Args:
            quantity_column (str): 數量欄位名稱
            price_column (str): 價格欄位名稱
            
        Returns:
            pd.DataFrame: 處理後的資料框
        """
        print("🚫 移除無效記錄 Removing invalid records...")
        
        before_count = len(self.df)
        
        # 移除負數量或零數量
        self.df = self.df[self.df[quantity_column] > 0]
        
        # 移除零價格或負價格
        self.df = self.df[self.df[price_column] > 0]
        
        after_count = len(self.df)
        removed_count = before_count - after_count
        
        print(f"移除無效記錄 Removed invalid records: {removed_count:,}")
        self.cleaning_log.append(f"移除無效記錄 Removed invalid: {removed_count:,} records")
        print(f"剩餘資料 Remaining data: {after_count:,}")
        
        return self.df
    
    def handle_missing_customer_id(self, customer_column: str = 'CustomerID', 
                                 action: str = 'remove') -> pd.DataFrame:
        """
        處理缺失的客戶ID
        
        Args:
            customer_column (str): 客戶ID欄位名稱
            action (str): 處理方式 ('remove' 或 'fill')
            
        Returns:
            pd.DataFrame: 處理後的資料框
        """
        print("👤 處理缺失的客戶ID Handling missing CustomerID...")
        
        before_count = len(self.df)
        missing_count = self.df[customer_column].isnull().sum()
        
        print(f"缺失客戶ID記錄 Missing CustomerID records: {missing_count:,}")
        
        if action == 'remove':
            # 移除缺失客戶ID的記錄（RFM分析需要客戶ID）
            self.df = self.df.dropna(subset=[customer_column])
            after_count = len(self.df)
            removed_count = before_count - after_count
            
            print(f"移除缺失客戶ID記錄 Removed missing CustomerID records: {removed_count:,}")
            self.cleaning_log.append(f"移除缺失客戶ID Removed missing CustomerID: {removed_count:,} records")
            
        elif action == 'fill':
            # 用特殊值填充缺失的客戶ID
            self.df[customer_column] = self.df[customer_column].fillna(-1)
            print(f"用 -1 填充缺失的客戶ID Filled missing CustomerID with -1")
            self.cleaning_log.append(f"填充缺失客戶ID Filled missing CustomerID: {missing_count:,} records")
        
        print(f"剩餘資料 Remaining data: {len(self.df):,}")
        
        return self.df
    
    def create_total_price_column(self, quantity_column: str = 'Quantity',
                                price_column: str = 'UnitPrice',
                                total_column: str = 'TotalPrice') -> pd.DataFrame:
        """
        建立總價欄位
        
        Args:
            quantity_column (str): 數量欄位名稱
            price_column (str): 單價欄位名稱
            total_column (str): 總價欄位名稱
            
        Returns:
            pd.DataFrame: 處理後的資料框
        """
        print("💰 建立總價欄位 Creating total price column...")
        
        self.df[total_column] = self.df[quantity_column] * self.df[price_column]
        
        print(f"✅ 總價欄位建立完成 Total price column created")
        print(f"總價範圍 Total price range: ${self.df[total_column].min():.2f} to ${self.df[total_column].max():.2f}")
        
        return self.df
    
    def remove_duplicates(self) -> pd.DataFrame:
        """
        移除重複記錄
        
        Returns:
            pd.DataFrame: 處理後的資料框
        """
        print("🔄 移除重複記錄 Removing duplicate records...")
        
        before_count = len(self.df)
        self.df = self.df.drop_duplicates()
        after_count = len(self.df)
        removed_count = before_count - after_count
        
        print(f"移除重複記錄 Removed duplicate records: {removed_count:,}")
        self.cleaning_log.append(f"移除重複記錄 Removed duplicates: {removed_count:,} records")
        print(f"最終資料筆數 Final data count: {after_count:,}")
        
        return self.df
    
    def detect_outliers(self, columns: List[str] = None) -> Dict[str, Dict]:
        """
        檢測異常值
        
        Args:
            columns (List[str]): 要檢查的欄位列表
            
        Returns:
            Dict[str, Dict]: 異常值統計
        """
        if columns is None:
            columns = ['Quantity', 'UnitPrice', 'TotalPrice']
            
        outliers_info = {}
        
        print("🔍 異常值檢測 Outlier Detection")
        print("=" * 50)
        
        for col in columns:
            if col in self.df.columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                outlier_count = len(outliers)
                outlier_percentage = (outlier_count / len(self.df)) * 100
                
                outliers_info[col] = {
                    'count': outlier_count,
                    'percentage': outlier_percentage,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound,
                    'Q1': Q1,
                    'Q3': Q3,
                    'IQR': IQR
                }
                
                print(f"{col} 異常值: {outlier_count:,} ({outlier_percentage:.2f}%)")
                print(f"  正常範圍: {lower_bound:.2f} - {upper_bound:.2f}")
        
        return outliers_info
    
    def clean_all(self, remove_outliers: bool = False, outlier_threshold: float = 0.95) -> pd.DataFrame:
        """
        執行完整的資料清理流程
        
        Args:
            remove_outliers (bool): 是否移除異常值
            outlier_threshold (float): 異常值閾值（分位數）
            
        Returns:
            pd.DataFrame: 清理後的資料框
        """
        print("🧹 開始完整資料清理流程 Starting complete data cleaning process...")
        print("=" * 60)
        
        # 1. 轉換日期格式
        self.convert_date_format()
        
        # 2. 移除取消交易
        self.remove_cancelled_transactions()
        
        # 3. 移除無效記錄
        self.remove_invalid_records()
        
        # 4. 處理缺失的客戶ID
        self.handle_missing_customer_id()
        
        # 5. 建立總價欄位
        self.create_total_price_column()
        
        # 6. 移除重複記錄
        self.remove_duplicates()
        
        # 7. 可選：移除異常值
        if remove_outliers:
            self.remove_extreme_outliers(threshold=outlier_threshold)
        
        return self.df
    
    def remove_extreme_outliers(self, columns: List[str] = None, threshold: float = 0.95) -> pd.DataFrame:
        """
        移除極端異常值
        
        Args:
            columns (List[str]): 要處理的欄位
            threshold (float): 分位數閾值
            
        Returns:
            pd.DataFrame: 處理後的資料框
        """
        if columns is None:
            columns = ['Quantity', 'UnitPrice', 'TotalPrice']
            
        print(f"🎯 移除極端異常值 Removing extreme outliers (>{threshold*100}% quantile)...")
        
        before_count = len(self.df)
        
        for col in columns:
            if col in self.df.columns:
                upper_limit = self.df[col].quantile(threshold)
                self.df = self.df[self.df[col] <= upper_limit]
        
        after_count = len(self.df)
        removed_count = before_count - after_count
        
        print(f"移除極端異常值 Removed extreme outliers: {removed_count:,}")
        self.cleaning_log.append(f"移除極端異常值 Removed extreme outliers: {removed_count:,} records")
        
        return self.df
    
    def get_cleaning_summary(self) -> Dict:
        """
        獲取清理摘要
        
        Returns:
            Dict: 清理摘要資訊
        """
        summary = {
            'original_count': len(self.original_df),
            'final_count': len(self.df),
            'removed_count': len(self.original_df) - len(self.df),
            'removal_rate': ((len(self.original_df) - len(self.df)) / len(self.original_df)) * 100,
            'retention_rate': (len(self.df) / len(self.original_df)) * 100,
            'cleaning_steps': self.cleaning_log
        }
        
        return summary
    
    def print_cleaning_summary(self) -> None:
        """列印清理摘要"""
        print("\n📋 資料清理摘要 Data Cleaning Summary")
        print("=" * 60)
        
        for log in self.cleaning_log:
            print(f"• {log}")
        
        summary = self.get_cleaning_summary()
        print(f"\n📊 清理效果 Cleaning Results:")
        print(f"原始資料 Original: {summary['original_count']:,} records")
        print(f"清理後資料 Cleaned: {summary['final_count']:,} records")
        print(f"移除比例 Removal rate: {summary['removal_rate']:.2f}%")
        print(f"保留比例 Retention rate: {summary['retention_rate']:.2f}%")
    
    def get_cleaned_data_overview(self) -> None:
        """顯示清理後資料概覽"""
        print("\n👀 清理後資料概覽 Cleaned Data Overview")
        print("=" * 50)
        print(f"資料形狀 Data shape: {self.df.shape}")
        
        if 'CustomerID' in self.df.columns:
            print(f"獨立客戶數 Unique customers: {self.df['CustomerID'].nunique():,}")
        if 'StockCode' in self.df.columns:
            print(f"獨立產品數 Unique products: {self.df['StockCode'].nunique():,}")
        if 'Country' in self.df.columns:
            print(f"獨立國家數 Unique countries: {self.df['Country'].nunique():,}")
        if 'InvoiceDate' in self.df.columns:
            print(f"交易日期範圍 Date range: {self.df['InvoiceDate'].min().date()} to {self.df['InvoiceDate'].max().date()}")

def main():
    """主函數 - 示範用法"""
    from data_loader import DataLoader
    
    # 載入資料
    loader = DataLoader('data.csv')
    df = loader.load_data()
    
    # 建立清理器
    cleaner = DataCleaner(df)
    
    # 執行完整清理
    cleaned_df = cleaner.clean_all()
    
    # 顯示清理摘要
    cleaner.print_cleaning_summary()
    cleaner.get_cleaned_data_overview()
    
    # 檢測異常值
    outliers = cleaner.detect_outliers()
    
    return cleaned_df

if __name__ == "__main__":
    cleaned_data = main()
