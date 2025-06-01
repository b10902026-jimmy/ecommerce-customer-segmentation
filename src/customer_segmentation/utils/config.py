"""
配置管理模組 - Configuration Management Module

提供專案的配置管理功能，支援從檔案、環境變數等來源載入配置。
"""

from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    """
    專案配置類別
    
    使用 Pydantic 進行配置驗證和管理，支援從環境變數載入配置。
    """
    
    # 專案基本設定
    project_name: str = Field(default="Customer Segmentation Analysis", env="PROJECT_NAME")
    version: str = Field(default="1.0.0", env="VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # 資料路徑設定
    data_dir: Path = Field(default=Path("data"), env="DATA_DIR")
    raw_data_dir: Path = Field(default=Path("data/raw"), env="RAW_DATA_DIR")
    processed_data_dir: Path = Field(default=Path("data/processed"), env="PROCESSED_DATA_DIR")
    results_dir: Path = Field(default=Path("data/results"), env="RESULTS_DIR")
    
    # 預設資料檔案
    default_data_file: str = Field(default="data.csv", env="DEFAULT_DATA_FILE")
    
    # RFM 分析設定
    rfm_bins: int = Field(default=5, env="RFM_BINS", description="RFM 分數的分組數量")
    analysis_date: Optional[str] = Field(default=None, env="ANALYSIS_DATE", description="分析日期 (YYYY-MM-DD)")
    
    # 視覺化設定
    figure_size: tuple = Field(default=(12, 8), env="FIGURE_SIZE")
    dpi: int = Field(default=300, env="DPI")
    style: str = Field(default="seaborn-v0_8", env="PLOT_STYLE")
    
    # 輸出設定
    output_format: str = Field(default="csv", env="OUTPUT_FORMAT", description="輸出格式: csv, excel, json")
    encoding: str = Field(default="utf-8", env="ENCODING")
    
    # 日誌設定
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # 效能設定
    chunk_size: int = Field(default=10000, env="CHUNK_SIZE", description="大檔案處理的分塊大小")
    n_jobs: int = Field(default=-1, env="N_JOBS", description="並行處理的工作數量")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 確保目錄存在
        self.create_directories()
    
    def create_directories(self) -> None:
        """建立必要的目錄"""
        directories = [
            self.data_dir,
            self.raw_data_dir,
            self.processed_data_dir,
            self.results_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_data_path(self, filename: str, data_type: str = "raw") -> Path:
        """
        獲取資料檔案的完整路徑
        
        Args:
            filename: 檔案名稱
            data_type: 資料類型 ('raw', 'processed', 'results')
            
        Returns:
            Path: 檔案的完整路徑
        """
        if data_type == "raw":
            return self.raw_data_dir / filename
        elif data_type == "processed":
            return self.processed_data_dir / filename
        elif data_type == "results":
            return self.results_dir / filename
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    
    def to_dict(self) -> Dict[str, Any]:
        """將配置轉換為字典"""
        return self.dict()
    
    @classmethod
    def from_file(cls, config_file: Path) -> "Config":
        """從配置檔案載入配置"""
        if config_file.suffix == ".json":
            import json
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        elif config_file.suffix in [".yml", ".yaml"]:
            import yaml
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config file format: {config_file.suffix}")
        
        return cls(**config_data)


# 全域配置實例
config = Config()


def get_config() -> Config:
    """獲取全域配置實例"""
    return config


def update_config(**kwargs) -> None:
    """更新全域配置"""
    global config
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            raise ValueError(f"Unknown config key: {key}")
