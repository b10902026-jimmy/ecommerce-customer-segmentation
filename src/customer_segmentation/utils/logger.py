"""
日誌系統模組 - Logging System Module

提供現代化的日誌功能，使用 loguru 進行美化輸出和靈活配置。
"""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger
from rich.console import Console
from rich.logging import RichHandler

from customer_segmentation.utils.config import get_config


def setup_logger(
    level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "1 week",
    format_string: Optional[str] = None,
    enable_rich: bool = True
) -> None:
    """
    設置日誌系統
    
    Args:
        level: 日誌級別 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日誌檔案路徑，None 表示不寫入檔案
        rotation: 日誌輪轉設定
        retention: 日誌保留時間
        format_string: 自訂格式字串
        enable_rich: 是否啟用 Rich 美化輸出
    """
    config = get_config()
    
    # 移除預設的 handler
    logger.remove()
    
    # 設定格式
    if format_string is None:
        if enable_rich:
            format_string = (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )
        else:
            format_string = (
                "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                "{name}:{function}:{line} | {message}"
            )
    
    # 控制台輸出
    if enable_rich:
        # 使用 Rich 進行美化輸出
        console = Console()
        logger.add(
            lambda msg: console.print(msg, end=""),
            level=level,
            format=format_string,
            colorize=True,
            backtrace=True,
            diagnose=True
        )
    else:
        # 標準輸出
        logger.add(
            sys.stdout,
            level=level,
            format=format_string,
            colorize=True,
            backtrace=True,
            diagnose=True
        )
    
    # 檔案輸出
    if log_file or config.log_file:
        log_path = Path(log_file or config.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_path,
            level=level,
            format=format_string,
            rotation=rotation,
            retention=retention,
            compression="zip",
            backtrace=True,
            diagnose=True,
            encoding="utf-8"
        )
        logger.info(f"日誌檔案設定完成 Log file configured: {log_path}")


def get_logger(name: str = None):
    """
    獲取日誌器實例
    
    Args:
        name: 日誌器名稱，通常使用 __name__
        
    Returns:
        logger: 日誌器實例
    """
    if name:
        return logger.bind(name=name)
    return logger


class LoggerMixin:
    """
    日誌混入類別
    
    為其他類別提供日誌功能的混入類別。
    """
    
    @property
    def logger(self):
        """獲取類別專用的日誌器"""
        return get_logger(self.__class__.__name__)


def log_execution_time(func):
    """
    裝飾器：記錄函數執行時間
    
    Args:
        func: 要裝飾的函數
        
    Returns:
        wrapper: 包裝後的函數
    """
    import time
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"開始執行 Starting execution: {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(
                f"執行完成 Execution completed: {func.__name__} "
                f"(耗時 Time: {execution_time:.2f}s)"
            )
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"執行失敗 Execution failed: {func.__name__} "
                f"(耗時 Time: {execution_time:.2f}s) - {str(e)}"
            )
            raise
    
    return wrapper


def log_dataframe_info(df, name: str = "DataFrame"):
    """
    記錄 DataFrame 的基本資訊
    
    Args:
        df: pandas DataFrame
        name: DataFrame 名稱
    """
    logger.info(f"{name} 資訊 Info:")
    logger.info(f"  形狀 Shape: {df.shape}")
    logger.info(f"  記憶體使用 Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        logger.warning(f"  缺失值 Missing values: {missing_count}")
    else:
        logger.info("  ✅ 無缺失值 No missing values")


# 初始化日誌系統
def init_logging():
    """初始化日誌系統"""
    config = get_config()
    setup_logger(
        level=config.log_level,
        log_file=config.log_file,
        enable_rich=not config.debug  # 在 debug 模式下使用簡單輸出
    )
    
    logger.info("🚀 客戶分群分析系統啟動 Customer Segmentation Analysis System Started")
    logger.info(f"📊 專案版本 Project Version: {config.version}")
    logger.info(f"🔧 除錯模式 Debug Mode: {config.debug}")


# 自動初始化
if __name__ != "__main__":
    init_logging()
