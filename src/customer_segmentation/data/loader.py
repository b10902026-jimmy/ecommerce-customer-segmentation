"""
資料載入模組 - Data Loader Module
負責載入和基本檢查 CSV 資料檔案
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional

class DataLoader:
    """資料載入器類別"""
    
    def __init__(self, file_path: str = 'data.csv'):
        """
        初始化資料載入器
        
        Args:
            file_path (str): CSV 檔案路徑
        """
        self.file_path = file_path
        self.df = None
        
    def load_data(self, encoding: str = 'utf-8') -> pd.DataFrame:
        """
        載入 CSV 資料檔案
        
        Args:
            encoding (str): 檔案編碼格式
            
        Returns:
            pd.DataFrame: 載入的資料框
        """
        print(f"🔄 載入資料中... Loading data from {self.file_path}")
        
        try:
            self.df = pd.read_csv(self.file_path, encoding=encoding)
            print(f"✅ 資料載入成功！Data loaded successfully!")
            print(f"📊 資料形狀 Data shape: {self.df.shape}")
            
        except UnicodeDecodeError:
            print(f"❌ UTF-8 編碼失敗，嘗試 latin-1 編碼...")
            try:
                self.df = pd.read_csv(self.file_path, encoding='latin-1')
                print(f"✅ 使用 latin-1 編碼載入成功！")
            except Exception as e:
                print(f"❌ 載入失敗 Loading failed: {e}")
                raise
                
        except Exception as e:
            print(f"❌ 載入失敗 Loading failed: {e}")
            raise
            
        return self.df
    
    def get_basic_info(self) -> dict:
        """
        獲取資料基本資訊
        
        Returns:
            dict: 包含基本資訊的字典
        """
        if self.df is None:
            raise ValueError("請先載入資料 Please load data first")
            
        info = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': dict(self.df.dtypes),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
            'missing_values': dict(self.df.isnull().sum()),
            'duplicates': self.df.duplicated().sum()
        }
        
        return info
    
    def print_basic_info(self) -> None:
        """列印資料基本資訊"""
        if self.df is None:
            raise ValueError("請先載入資料 Please load data first")
            
        print("\n📋 資料基本資訊 Basic Data Information")
        print("=" * 50)
        print(f"資料筆數 Number of records: {self.df.shape[0]:,}")
        print(f"欄位數量 Number of columns: {self.df.shape[1]}")
        print(f"記憶體使用 Memory usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print("\n📊 資料型態 Data Types:")
        for col, dtype in self.df.dtypes.items():
            print(f"  {col}: {dtype}")
            
        print("\n🔍 缺失值統計 Missing Values:")
        missing = self.df.isnull().sum()
        for col, count in missing.items():
            if count > 0:
                percentage = (count / len(self.df)) * 100
                print(f"  {col}: {count:,} ({percentage:.2f}%)")
        
        if missing.sum() == 0:
            print("  ✅ 沒有缺失值 No missing values")
            
        duplicates = self.df.duplicated().sum()
        print(f"\n🔄 重複記錄 Duplicate records: {duplicates:,} ({duplicates/len(self.df)*100:.2f}%)")
    
    def preview_data(self, n_rows: int = 5) -> None:
        """
        預覽資料
        
        Args:
            n_rows (int): 要顯示的行數
        """
        if self.df is None:
            raise ValueError("請先載入資料 Please load data first")
            
        print(f"\n👀 前 {n_rows} 筆資料 First {n_rows} records:")
        print(self.df.head(n_rows).to_string())
        
        print(f"\n👀 後 {n_rows} 筆資料 Last {n_rows} records:")
        print(self.df.tail(n_rows).to_string())
    
    def get_statistical_summary(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        獲取統計摘要
        
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: 數值欄位和文字欄位的統計摘要
        """
        if self.df is None:
            raise ValueError("請先載入資料 Please load data first")
            
        numerical_summary = self.df.describe()
        categorical_summary = self.df.describe(include=['object'])
        
        return numerical_summary, categorical_summary
    
    def validate_columns(self, required_columns: list) -> bool:
        """
        驗證必要欄位是否存在
        
        Args:
            required_columns (list): 必要欄位列表
            
        Returns:
            bool: 是否包含所有必要欄位
        """
        if self.df is None:
            raise ValueError("請先載入資料 Please load data first")
            
        missing_columns = set(required_columns) - set(self.df.columns)
        
        if missing_columns:
            print(f"❌ 缺少必要欄位 Missing required columns: {missing_columns}")
            return False
        else:
            print(f"✅ 所有必要欄位都存在 All required columns present")
            return True

def main():
    """主函數 - 示範用法"""
    # 建立資料載入器
    loader = DataLoader('data.csv')
    
    # 載入資料
    df = loader.load_data()
    
    # 顯示基本資訊
    loader.print_basic_info()
    
    # 預覽資料
    loader.preview_data()
    
    # 驗證必要欄位
    required_cols = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 
                    'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
    loader.validate_columns(required_cols)
    
    # 獲取統計摘要
    num_summary, cat_summary = loader.get_statistical_summary()
    print("\n📊 數值欄位統計摘要 Numerical Summary:")
    print(num_summary.to_string())
    
    print("\n📊 文字欄位統計摘要 Categorical Summary:")
    print(cat_summary.to_string())

if __name__ == "__main__":
    main()
