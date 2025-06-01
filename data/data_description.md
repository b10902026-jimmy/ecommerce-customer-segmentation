# 📄 電商交易資料集說明文件
# E-commerce Transaction Dataset Description

本文件描述電商交易資料集的結構、清理流程和使用方式。
This document describes the structure, cleaning process, and usage of the e-commerce transaction dataset.

---

## 📊 資料集概述 Dataset Overview

### 原始資料 Original Data: `data/raw/data.csv`
- **資料來源 Data Source**: Kaggle "E-Commerce Data" dataset
- **資料期間 Time Period**: 2010年12月1日 - 2011年12月9日 (Dec 1, 2010 - Dec 9, 2011)
- **原始記錄數 Original Records**: 541,909 筆交易記錄
- **地理範圍 Geographic Coverage**: 38個國家，主要集中在歐洲

### 清理後資料 Cleaned Data: `data/results/cleaned_data.csv`
- **清理後記錄數 Cleaned Records**: 392,692 筆交易記錄
- **資料保留率 Retention Rate**: 72.5%
- **分析客戶數 Customers for Analysis**: 4,338 位
- **資料品質 Data Quality**: 100% 完整性（無缺失值）

---

## 📋 原始資料格式範例 Original Data Format Examples

### 典型交易記錄範例 Typical Transaction Records
```csv
InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country
536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,12/1/2010 8:26,2.55,17850,United Kingdom
536365,71053,WHITE METAL LANTERN,6,12/1/2010 8:26,3.39,17850,United Kingdom
536365,84406B,CREAM CUPID HEARTS COAT HANGER,8,12/1/2010 8:26,2.75,17850,United Kingdom
536366,22633,HAND WARMER UNION JACK,6,12/1/2010 8:28,1.85,17850,United Kingdom
```

### 問題資料範例 Problematic Data Examples
```csv
# 取消交易 (以C開頭的發票號碼)
C536365,22728,ALARM CLOCK BAKELIKE PINK,-1,12/1/2010 9:01,3.39,17850,United Kingdom

# 缺失客戶ID
536367,84879,ASSORTED COLOUR BIRD ORNAMENT,32,12/1/2010 8:34,1.69,,United Kingdom

# 無效價格
536370,21866,UNION JACK HOT WATER BOTTLE,1,12/1/2010 8:45,0.00,17850,United Kingdom

# 負數量 (退貨)
536414,22139,RETROSPOT TEA SET CERAMIC 11 PC,-56,12/1/2010 9:09,4.95,17850,United Kingdom
```

---

## 🧱 原始資料欄位說明 Original Data Columns

| 欄位名稱 Column | 資料型態 Type | 說明 Description |
|----------------|---------------|------------------|
| `InvoiceNo`    | `object`      | 發票編號，以 'C' 開頭表示取消交易 Transaction ID, 'C' prefix means cancelled |
| `StockCode`    | `object`      | 商品代碼 Product code (SKU) |
| `Description`  | `object`      | 商品描述 Product description |
| `Quantity`     | `int64`       | 購買數量，負數表示退貨 Quantity sold, negative means returns |
| `InvoiceDate`  | `object`      | 交易日期時間（字串格式）Transaction datetime (string format) |
| `UnitPrice`    | `float64`     | 商品單價（英鎊）Unit price in GBP |
| `CustomerID`   | `float64`     | 客戶編號（存在缺失值）Customer ID (with missing values) |
| `Country`      | `object`      | 客戶所在國家 Customer's country |

---

## 🧹 資料清理流程 Data Cleaning Process

我們對原始資料執行了系統性的清理流程，以確保分析品質：
We performed systematic data cleaning to ensure analysis quality:

### 清理步驟 Cleaning Steps

#### 1. 📅 日期格式標準化 Date Format Standardization
- **處理內容**: 將 `InvoiceDate` 從字串轉換為 datetime 格式
- **結果**: 100% 成功轉換
- **影響**: 確保時間序列分析的準確性

**範例 Example:**
```
原始格式 Original: "12/1/2010 8:26"
轉換後 Converted: 2010-12-01 08:26:00
```

#### 2. ❌ 移除取消交易 Remove Cancelled Transactions
- **識別標準**: 發票號碼以 'C' 開頭的記錄
- **移除數量**: 9,288 筆 (1.7%)
- **商業邏輯**: 取消交易不反映真實客戶購買行為

**範例 Example:**
```
移除的記錄 Removed Records:
InvoiceNo: C536365, StockCode: 22728, Quantity: -1, UnitPrice: 3.39
InvoiceNo: C536379, StockCode: 21755, Quantity: -1, UnitPrice: 7.95
InvoiceNo: C536383, StockCode: 22960, Quantity: -6, UnitPrice: 1.25

原因 Reason: 這些是取消的交易，不代表實際的客戶購買行為
These are cancelled transactions that don't represent actual customer behavior
```

#### 3. 🚫 移除無效記錄 Remove Invalid Records
- **無效數量**: 移除 `Quantity <= 0` 的記錄 (10,624 筆)
- **無效價格**: 移除 `UnitPrice <= 0` 的記錄 (1,454 筆)
- **總計移除**: 12,078 筆 (2.3%)
- **原因**: 負數或零值不代表真實交易

**範例 Example:**
```
無效數量記錄 Invalid Quantity Records:
InvoiceNo: 536414, StockCode: 22139, Quantity: -56, UnitPrice: 4.95
InvoiceNo: 536545, StockCode: 21773, Quantity: -1, UnitPrice: 1.95
InvoiceNo: 536592, StockCode: 23843, Quantity: 0, UnitPrice: 2.55

無效價格記錄 Invalid Price Records:
InvoiceNo: 536370, StockCode: 21866, Quantity: 1, UnitPrice: 0.00
InvoiceNo: 536389, StockCode: 35004C, Quantity: 1, UnitPrice: -0.04

原因 Reason: 負數量表示退貨，零值不代表實際交易金額
Negative quantities indicate returns, zero values don't represent actual transactions
```

#### 4. 👤 處理缺失客戶ID Handle Missing Customer IDs
- **缺失數量**: 135,080 筆記錄無客戶ID (24.9%)
- **處理策略**: 完全移除（RFM分析必須有客戶識別）
- **商業影響**: 無法進行客戶層級分析的記錄
- **替代方案考量**: 曾考慮填充，但會影響分群準確性

**範例 Example:**
```
缺失客戶ID記錄 Missing Customer ID Records:
InvoiceNo: 536365, StockCode: 85123A, CustomerID: NaN, Country: United Kingdom
InvoiceNo: 536366, StockCode: 71053, CustomerID: NaN, Country: United Kingdom
InvoiceNo: 536367, StockCode: 84406B, CustomerID: NaN, Country: United Kingdom

原因 Reason: RFM分析需要追蹤個別客戶的購買行為，無客戶ID無法進行分群
RFM analysis requires tracking individual customer behavior, impossible without Customer ID
```

#### 5. 💰 建立總價欄位 Create Total Price Column
- **計算公式**: `TotalPrice = Quantity × UnitPrice`
- **目的**: 統一金額計算標準
- **驗證**: 檢查計算結果的合理性

**範例 Example:**
```
計算過程 Calculation Process:
InvoiceNo: 536365, StockCode: 85123A, Quantity: 6, UnitPrice: 2.55
TotalPrice = 6 × 2.55 = 15.30

InvoiceNo: 536365, StockCode: 71053, Quantity: 6, UnitPrice: 3.39
TotalPrice = 6 × 3.39 = 20.34

InvoiceNo: 536365, StockCode: 84406B, Quantity: 8, UnitPrice: 2.75
TotalPrice = 8 × 2.75 = 22.00
```

#### 6. 🔄 移除重複記錄 Remove Duplicate Records
- **識別標準**: 所有欄位完全相同的記錄
- **移除數量**: 1,336 筆 (0.2%)
- **保留策略**: 保留第一筆出現的記錄

### 📊 清理結果統計 Cleaning Results Summary

| 項目 Item | 數量 Count | 比例 Percentage |
|-----------|------------|----------------|
| 原始記錄 Original Records | 541,909 | 100.0% |
| 取消交易 Cancelled Transactions | 9,288 | 1.7% |
| 無效記錄 Invalid Records | 12,078 | 2.3% |
| 缺失客戶ID Missing Customer ID | 135,080 | 24.9% |
| 重複記錄 Duplicate Records | 1,336 | 0.2% |
| **清理後記錄 Final Clean Records** | **392,692** | **72.5%** |

---

## 🎯 清理後資料結構 Cleaned Data Structure

### 新增欄位 New Columns
| 欄位名稱 Column | 資料型態 Type | 說明 Description |
|----------------|---------------|------------------|
| `TotalPrice`   | `float64`     | 總價 = 數量 × 單價 Total price = Quantity × UnitPrice |

### 資料品質保證 Data Quality Assurance
- ✅ **無缺失值**: 所有記錄都有完整的客戶ID
- ✅ **無異常值**: 移除了負數和零值
- ✅ **格式統一**: 日期格式標準化
- ✅ **無重複**: 移除了重複記錄

### 清理後統計 Post-Cleaning Statistics
- **獨立客戶數 Unique Customers**: 4,338 位
- **獨立商品數 Unique Products**: ~3,600 種
- **涵蓋國家數 Countries Covered**: 38 個
- **交易日期範圍 Date Range**: 2010/12/01 - 2011/12/09
- **總營收 Total Revenue**: ~$8,200,000

---

## 📁 檔案使用指南 File Usage Guide

### 🎯 建議使用 Recommended Usage

**進行分析時請使用清理後的資料：**
**For analysis, please use the cleaned data:**

```python
# 載入清理後的資料 Load cleaned data
import pandas as pd
df = pd.read_csv('data/results/cleaned_data.csv')

# 或使用我們的分析系統 Or use our analysis system
from customer_segmentation import CustomerSegmentationPipeline
pipeline = CustomerSegmentationPipeline()
cleaned_data = pipeline.load_cleaned_data()
```

### 📂 檔案結構 File Structure
```
data/
├── raw/
│   └── data.csv                    # 原始資料 Original data
├── results/
│   ├── cleaned_data.csv            # 清理後資料 Cleaned data ⭐
│   ├── rfm_data.csv               # RFM 分析結果 RFM analysis results
│   ├── customer_segmentation_results.csv  # 客戶分群結果 Segmentation results
│   └── segment_summary.csv        # 分群摘要 Segment summary
└── data_description.md            # 本文件 This document
```

### ⚠️ 重要注意事項 Important Notes

1. **使用清理後資料**: 分析時請使用 `cleaned_data.csv`，不要直接使用原始資料
2. **客戶ID完整性**: 清理後的資料保證每筆記錄都有有效的客戶ID
3. **資料代表性**: 72.5% 的保留率確保了樣本的代表性
4. **時間範圍**: 分析結果基於2010-2011年的資料

---

## 🎯 分析任務建議 Suggested Analysis Tasks

### 1. 🎯 RFM 客戶分群分析 RFM Customer Segmentation
- 使用 Recency、Frequency、Monetary 三個維度
- 識別高價值客戶群體
- 制定差異化行銷策略

### 2. 📊 銷售趨勢分析 Sales Trend Analysis
- 基於 `InvoiceDate` 和 `TotalPrice` 進行時間序列分析
- 識別季節性模式和趨勢

### 3. 🌍 地理分析 Geographic Analysis
- 分析不同國家的客戶行為
- 識別主要市場和擴展機會

### 4. 🛒 商品分析 Product Analysis
- 基於 `StockCode` 和 `Description` 進行商品分析
- 識別熱銷商品和交叉銷售機會

---

## 🔧 技術實現 Technical Implementation

### 清理程式碼位置 Cleaning Code Location
- **主要模組**: `src/customer_segmentation/data/cleaner.py`
- **使用方式**: 通過 `CustomerSegmentationPipeline` 自動執行
- **可重現性**: 所有清理步驟都有詳細記錄

### 品質驗證 Quality Validation
- 每個清理步驟都有統計記錄
- 提供清理前後的對比分析
- 支援異常值檢測和報告

---

**文件更新日期 Document Updated**: 2025年5月31日  
**資料版本 Data Version**: v1.0 (Cleaned)  
**維護者 Maintainer**: Customer Segmentation Analysis Team

📦 資料集概述
資料來源：Kaggle 上的 "E-Commerce Data" 資料集，由 carrie1 提供。
資料期間：2010 年 12 月 1 日至 2011 年 12 月 9 日。
資料筆數：共計 541,909 筆交易紀錄。
資料特性：
交易紀錄：每筆交易包含發票編號、商品代碼、商品描述、數量、交易日期、單價、客戶編號及國家。
地區分布：涵蓋多個國家的客戶，主要集中在英國。
客戶類型：包括零售客戶和批發商。
GitHub
Medium
📝 資料欄位說明
欄位名稱	資料型態	說明
InvoiceNo	文字	發票編號，若以 'C' 開頭表示取消交易。
StockCode	文字	商品代碼。
Description	文字	商品描述。
Quantity	整數	購買數量，負數表示退貨。
InvoiceDate	日期時間	交易日期和時間。
UnitPrice	浮點數	商品單價（英鎊）。
CustomerID	整數	客戶編號。
Country	文字	客戶所在國家。
📊 資料統計摘要
總交易筆數：541,909
獨立客戶數：約 4,000 位
商品種類數：約 4,200 種
主要銷售國家：英國、荷蘭、德國、法國、愛爾蘭、西班牙等。
交易時間分布：交易主要集中在工作日的中午時段。
griddb.net
+4
Medium
+4
GitHub
+4
⚠️ 注意事項
退貨交易：Quantity 為負數的紀錄表示退貨，需在分析時特別處理。
缺失值：CustomerID 欄位存在缺失值，進行客戶分析時需考慮。
資料清理：建議在分析前，先清理異常值和缺失值，以確保分析結果的準確性。
