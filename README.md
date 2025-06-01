# 🛍️ 客戶分群分析系統 Customer Segmentation Analysis System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/Poetry-1.2+-green.svg)](https://python-poetry.org/)
[![Conda](https://img.shields.io/badge/Conda-Latest-orange.svg)](https://docs.conda.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

這是一個現代化的客戶分群分析系統，使用 RFM (Recency, Frequency, Monetary) 模型來分析客戶行為並進行分群，專為團隊協作和科學計算優化。

## 📋 專案概述 Project Overview

本專案針對電商交易資料進行客戶分群分析，幫助企業：
- 🌟 識別高價值客戶 (Champions)
- ⚠️ 發現潛在流失客戶 (At-risk customers)
- 🆕 分析新客戶行為 (New customers)
- 💎 維護忠實客戶關係 (Loyal customers)

## 🏗️ 現代化架構 Modern Architecture

### 模組化設計
```
📦 Customer Segmentation System
├── 📁 src/customer_segmentation/     # 主要套件
│   ├── 📁 data/                      # 資料處理模組
│   │   ├── 📄 loader.py              # 資料載入器
│   │   └── 📄 cleaner.py             # 資料清理器
│   ├── 📁 analysis/                  # 分析模組
│   │   └── 📄 rfm_calculator.py      # RFM 計算器
│   ├── 📁 visualization/             # 視覺化模組
│   │   └── 📄 visualizer.py          # 資料視覺化器
│   ├── 📁 utils/                     # 工具模組
│   │   ├── 📄 config.py              # 配置管理
│   │   └── 📄 logger.py              # 日誌系統
│   ├── 📄 pipeline.py                # 分析管道
│   └── 📄 cli.py                     # 命令列介面
├── 📁 data/                          # 資料目錄
│   ├── 📁 raw/                       # 原始資料
│   ├── 📁 processed/                 # 處理後資料
│   └── 📁 results/                   # 分析結果
├── 📁 notebooks/                     # Jupyter notebooks
├── 📁 scripts/                       # 執行腳本
├── 📁 docs/                          # 文件
├── 📄 environment.yml                # Conda 環境配置
├── 📄 pyproject.toml                 # Poetry 專案配置
└── 📄 README.md                      # 說明文件
```

## 🚀 快速開始 Quick Start

### 1. 環境設置 Environment Setup

#### 使用 Conda + Poetry (推薦)
```bash
# 建立 Conda 環境
conda env create -f environment.yml

# 啟動環境
conda activate customer-segmentation

# 安裝 Poetry 依賴
poetry install

# 或者只安裝生產依賴
poetry install --only main
```

#### 僅使用 Poetry
```bash
# 安裝所有依賴
poetry install

# 啟動虛擬環境
poetry shell
```

### 2. 資料準備 Data Preparation
```bash
# 將您的資料檔案放入 data/raw/ 目錄
cp your_data.csv data/raw/data.csv
```

### 3. 執行分析 Run Analysis

#### 🔥 推薦使用方式 (新功能)
```bash
# 一鍵完整分析流程（推薦）
customer-seg full-pipeline data/raw/data.csv

# 快速重新生成所有圖表
customer-seg plots --all

# 查看互動式圖表
customer-seg interactive --open-browser

# 更新報告
customer-seg report --update-plots
```

#### 使用 CLI 介面
```bash
# 完整分析
customer-seg analyze data/raw/data.csv

# 快速分析
customer-seg analyze data/raw/data.csv --quick

# 自訂輸出目錄
customer-seg analyze data/raw/data.csv -o custom_output/

# 驗證資料格式
customer-seg validate data/raw/data.csv

# 顯示系統資訊
customer-seg info
```

#### 使用 Python 腳本
```bash
# 完整分析
python scripts/run_analysis.py

# 快速分析
python scripts/run_analysis.py --quick
```

#### 使用 Python API
```python
from customer_segmentation import CustomerSegmentationPipeline

# 建立分析管道
pipeline = CustomerSegmentationPipeline()

# 執行完整分析
results = pipeline.run_full_analysis('data/raw/data.csv')

# 或者逐步執行
pipeline.load_data('data/raw/data.csv')
pipeline.clean_data()
pipeline.calculate_rfm()
pipeline.segment_customers()
pipeline.create_visualizations()
pipeline.export_results()
```

## 🆕 新功能亮點 New Features

### 🎨 快速圖表重新生成
```bash
# 重新生成所有圖表（無需重新分析）
customer-seg plots --all

# 生成特定類型圖表
customer-seg plots --type rfm
customer-seg plots --type segments
customer-seg plots --type correlation
customer-seg plots --type geographic
customer-seg plots --type timeseries
customer-seg plots --type interactive

# 包含互動式圖表
customer-seg plots --all --interactive
```

### 🌐 互動式圖表體驗
```bash
# 查看互動式圖表使用說明
customer-seg interactive

# 自動開啟瀏覽器查看
customer-seg interactive --open-browser
```

### 🚀 一鍵完整流程
```bash
# 執行完整分析流程（分析+圖表+報告）
customer-seg full-pipeline data/raw/data.csv

# 包含詳細的進度顯示和結果摘要
```

### 📊 智能報告管理
```bash
# 檢查報告和圖表狀態
customer-seg report

# 同時更新圖表和報告
customer-seg report --update-plots
```

### 🛠️ 便利腳本工具
```bash
# 使用專用腳本快速重新生成圖表
python scripts/regenerate_plots.py

# 支援多種參數選項
python scripts/regenerate_plots.py --type rfm --output-dir custom_plots/
```

## 📚 詳細使用說明 Detailed Usage

### CLI 命令參考 CLI Command Reference

```bash
# 🔥 新增命令
customer-seg full-pipeline DATA_FILE     # 完整分析流程
customer-seg plots [OPTIONS]             # 快速圖表生成
customer-seg interactive [OPTIONS]       # 互動式圖表
customer-seg report [OPTIONS]            # 報告管理

# 原有命令
customer-seg analyze [OPTIONS] DATA_FILE # 基本分析
customer-seg validate DATA_FILE           # 驗證資料格式
customer-seg info                         # 顯示系統資訊

# analyze 命令選項:
  -o, --output-dir PATH     輸出目錄
  --remove-outliers         移除異常值
  --rfm-bins INTEGER        RFM 分數分組數 (預設: 5)
  --analysis-date TEXT      分析日期 (YYYY-MM-DD)
  --no-plots               不生成圖表
  --quick                  快速分析模式

# plots 命令選項:
  --all                    重新生成所有圖表
  --type CHOICE            指定圖表類型
  --output-dir PATH        輸出目錄
  --interactive            同時生成互動式圖表

# interactive 命令選項:
  --open-browser           自動開啟瀏覽器

# report 命令選項:
  --update-plots           同時更新圖表
  --output PATH            輸出檔案路徑
```

### 配置管理 Configuration Management

系統支援多種配置方式：

#### 環境變數
```bash
export DATA_DIR="custom_data"
export RFM_BINS=3
export LOG_LEVEL="DEBUG"
```

#### 配置檔案 (.env)
```env
PROJECT_NAME="My Customer Analysis"
DEBUG=true
RFM_BINS=5
OUTPUT_FORMAT=excel
```

#### 程式碼配置
```python
from customer_segmentation.utils.config import update_config

update_config(
    rfm_bins=3,
    remove_outliers=True,
    log_level="DEBUG"
)
```

## 📊 資料格式要求 Data Format Requirements

### 必要欄位 Required Columns
| 欄位名稱 | 資料型態 | 說明 |
|---------|---------|------|
| InvoiceNo | 文字 | 發票編號 |
| StockCode | 文字 | 商品代碼 |
| Description | 文字 | 商品描述 |
| Quantity | 整數 | 購買數量 |
| InvoiceDate | 日期時間 | 交易日期 |
| UnitPrice | 浮點數 | 商品單價 |
| CustomerID | 整數 | 客戶編號 |
| Country | 文字 | 客戶國家 |

### 資料品質要求
- ✅ 無重複記錄
- ✅ CustomerID 不可為空（RFM 分析必需）
- ✅ Quantity > 0（排除退貨記錄）
- ✅ UnitPrice > 0（排除無效價格）
- ✅ InvoiceDate 格式正確

## 🎯 RFM 模型說明 RFM Model Explanation

### RFM 指標定義
- **Recency (R)**: 最近一次購買距今天數
  - 數值越小 = 客戶越活躍
- **Frequency (F)**: 購買頻率（交易次數）
  - 數值越大 = 客戶越忠誠
- **Monetary (M)**: 購買金額總和
  - 數值越大 = 客戶價值越高

### 客戶分群定義
| 分群名稱 | 特徵 | 行銷策略 |
|---------|------|---------|
| **Champions** | 高 R + 高 F + 高 M | VIP 服務，推薦高價值產品 |
| **Loyal Customers** | 中高 R + 高 F + 中高 M | 忠誠度獎勵，維持關係 |
| **Potential Loyalists** | 中高 R + 中 F + 中 M | 提升購買頻率活動 |
| **New Customers** | 高 R + 低 F + 低 M | 歡迎活動，引導深度使用 |
| **At Risk** | 低 R + 高 F + 高 M | 主動聯繫，特別優惠挽回 |
| **Cannot Lose Them** | 極低 R + 高 F + 高 M | 緊急挽回，個人化服務 |
| **Hibernating** | 低 R + 低 F + 低 M | 重新激活活動，限時優惠 |

## 📈 輸出結果 Output Results

### 生成檔案
1. **customer_segmentation_results.csv** - 完整分析結果
2. **cleaned_data.csv** - 清理後的原始資料
3. **rfm_data.csv** - RFM 指標資料
4. **segment_summary.csv** - 分群摘要統計

### 視覺化圖表
- 📊 資料品質概覽圖
- 📈 RFM 分布分析圖
- 🔗 RFM 相關性熱力圖
- 👥 客戶分群分析圖
- 📅 時間序列分析圖
- 🌍 地理分析圖

## 🔧 開發指南 Development Guide

### 開發環境設置
```bash
# 安裝開發依賴
poetry install --with dev

# 安裝 pre-commit hooks
pre-commit install

# 執行代碼格式化
black src/
isort src/

# 執行代碼檢查
flake8 src/
mypy src/
```

### 專案結構說明
- **src/customer_segmentation/**: 主要套件代碼
- **data/**: 資料檔案目錄
- **notebooks/**: Jupyter notebook 範例
- **scripts/**: 執行腳本
- **docs/**: 專案文件

### 擴展功能
系統採用模組化設計，易於擴展：

```python
# 自訂分析器
from customer_segmentation.analysis.rfm_calculator import RFMCalculator

class CustomRFMCalculator(RFMCalculator):
    def custom_segmentation_logic(self):
        # 實現自訂分群邏輯
        pass

# 自訂視覺化
from customer_segmentation.visualization.visualizer import DataVisualizer

class CustomVisualizer(DataVisualizer):
    def plot_custom_chart(self):
        # 實現自訂圖表
        pass
```

## 🚨 常見問題 Troubleshooting

### 1. 環境問題
```bash
# Conda 環境衝突
conda clean --all
conda env remove -n customer-segmentation
conda env create -f environment.yml

# Poetry 依賴問題
poetry cache clear --all pypi
poetry install --no-cache
```

### 2. 資料問題
```bash
# 驗證資料格式
customer-seg validate your_data.csv

# 檢查資料編碼
file -I your_data.csv
```

### 3. 記憶體問題
```bash
# 使用快速分析模式
customer-seg analyze data.csv --quick

# 或設定較小的分塊大小
export CHUNK_SIZE=5000
```

## 📞 技術支援 Technical Support

### 系統需求
- **Python**: 3.9+
- **記憶體**: 8GB+ (推薦)
- **儲存空間**: 2GB+
- **作業系統**: Windows, macOS, Linux

### 依賴管理
- **Conda**: 科學計算套件管理
- **Poetry**: Python 套件和虛擬環境管理
- **核心套件**: pandas, numpy, scikit-learn, matplotlib, seaborn, plotly

### 效能優化
- 大型資料集: 使用 `--quick` 模式
- 記憶體限制: 調整 `CHUNK_SIZE` 環境變數
- 並行處理: 設定 `N_JOBS` 環境變數

## 🤝 團隊協作 Team Collaboration

### Git 工作流程
```bash
# 克隆專案
git clone <repository-url>
cd customer-segmentation

# 建立功能分支
git checkout -b feature/new-analysis

# 提交變更
git add .
git commit -m "Add new analysis feature"

# 推送到遠端
git push origin feature/new-analysis
```

### 代碼品質
- 使用 **Black** 進行代碼格式化
- 使用 **isort** 整理 import
- 使用 **flake8** 進行代碼檢查
- 使用 **mypy** 進行類型檢查

### 文件協作
- 使用 **MkDocs** 生成文件
- 支援 **Jupyter Notebook** 協作
- 提供 **CLI** 和 **API** 兩種使用方式

## 📝 更新日誌 Changelog

### v1.0.0 (2024-05-31)
- ✅ 現代化模組架構
- ✅ Conda + Poetry 混合管理
- ✅ CLI 介面和 Rich 美化輸出
- ✅ 配置管理和日誌系統
- ✅ 完整的 RFM 分析管道
- ✅ 豐富的視覺化功能
- ✅ 團隊協作優化

## 📄 授權 License

本專案採用 MIT 授權條款。

---

**🎯 專案目標**: 為組員 A 的客戶分群分析提供現代化、模組化的分析工具，支援團隊協作和後續的機器學習分群演算法應用。

**👥 適用對象**: 資料科學團隊、業務分析師、產品經理、行銷團隊

**🔗 相關資源**: 
- [RFM 分析指南](docs/rfm_guide.md)
- [API 文件](docs/api_reference.md)
- [範例 Notebook](notebooks/example_analysis.ipynb)
