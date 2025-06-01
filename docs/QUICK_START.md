# 🚀 快速開始指南
# Quick Start Guide

這份指南將幫助你快速使用客戶分群分析系統的新功能。

---

## 📋 目錄 Table of Contents

1. [快速圖表重新生成](#快速圖表重新生成)
2. [CLI 工具使用](#cli-工具使用)
3. [互動式圖表](#互動式圖表)
4. [完整分析流程](#完整分析流程)
5. [常見問題](#常見問題)

---

## 🎨 快速圖表重新生成

### 方法一：使用 CLI 工具（推薦）

```bash
# 重新生成所有圖表
customer-seg plots --all

# 重新生成特定類型的圖表
customer-seg plots --type rfm
customer-seg plots --type segments
customer-seg plots --type correlation

# 包含互動式圖表
customer-seg plots --all --interactive
```

### 方法二：使用專用腳本

```bash
# 重新生成所有圖表
python scripts/regenerate_plots.py

# 重新生成特定類型
python scripts/regenerate_plots.py --type rfm

# 指定資料檔案
python scripts/regenerate_plots.py data/raw/data.csv --all
```

### 方法三：使用現有的分析腳本

```bash
# 快速模式（只生成基本圖表）
python scripts/run_analysis.py --quick
```

---

## 🛠️ CLI 工具使用

### 安裝和設置

```bash
# 執行設置腳本
bash scripts/setup.sh

# 啟動環境（如果使用 conda）
conda activate customer-segmentation
```

### 主要命令

#### 1. 完整分析流程
```bash
# 一鍵執行完整分析（推薦）
customer-seg full-pipeline data/raw/data.csv

# 包含所有步驟：資料分析 + 圖表生成 + 報告檢查
```

#### 2. 快速圖表生成
```bash
# 重新生成所有圖表
customer-seg plots --all

# 生成特定圖表
customer-seg plots --type segments

# 自動尋找資料檔案
customer-seg plots --all  # 會自動找到 data/raw/data.csv
```

#### 3. 報告管理
```bash
# 檢查報告狀態
customer-seg report

# 同時更新圖表和報告
customer-seg report --update-plots
```

#### 4. 互動式圖表
```bash
# 顯示使用說明
customer-seg interactive

# 自動開啟瀏覽器
customer-seg interactive --open-browser
```

#### 5. 其他實用工具
```bash
# 驗證資料檔案
customer-seg validate data/raw/data.csv

# 查看系統資訊
customer-seg info

# 基本分析
customer-seg analyze data/raw/data.csv
```

---

## 🌐 互動式圖表

### 查看互動式圖表

1. **使用 CLI 工具**：
   ```bash
   customer-seg interactive --open-browser
   ```

2. **手動開啟**：
   - 在瀏覽器中開啟：`plots/interactive_rfm_plot.html`
   - 或使用本地伺服器：
     ```bash
     python -m http.server 8000
     # 然後訪問：http://localhost:8000/plots/interactive_rfm_plot.html
     ```

### 互動式圖表功能

| 功能 | 操作方式 |
|------|----------|
| 🔍 縮放探索 | 滑鼠滾輪縮放，拖拽移動 |
| 🎯 懸停資訊 | 滑鼠懸停顯示客戶詳細資訊 |
| 🎨 分群篩選 | 點擊圖例隱藏/顯示群體 |
| 📊 多維度展示 | 同時展示 R、F、M 三個維度 |
| 💡 即時篩選 | 可按客戶群體進行篩選 |

---

## 🔄 完整分析流程

### 一鍵執行（最簡單）

```bash
# 執行完整分析流程
customer-seg full-pipeline data/raw/data.csv
```

這個命令會：
1. ✅ 執行資料分析
2. ✅ 生成所有圖表（包含互動式）
3. ✅ 檢查報告狀態
4. ✅ 顯示結果摘要
5. ✅ 提供下一步指引

### 分步執行

```bash
# 步驟 1: 執行分析
customer-seg analyze data/raw/data.csv

# 步驟 2: 生成圖表
customer-seg plots --all --interactive

# 步驟 3: 更新報告
customer-seg report

# 步驟 4: 查看互動式圖表
customer-seg interactive --open-browser
```

---

## 📊 生成的圖表類型

| 圖表名稱 | 檔案名稱 | 說明 |
|----------|----------|------|
| RFM 分布圖 | `rfm_distributions.png` | 展示 R、F、M 三個指標的分布 |
| 客戶分群圖 | `customer_segments.png` | 展示各客戶群體的特徵 |
| RFM 相關性圖 | `rfm_correlation.png` | 展示指標間的相關性 |
| 地理分析圖 | `geographic_analysis.png` | 展示客戶地理分布 |
| 時間序列圖 | `time_series_analysis.png` | 展示時間趨勢 |
| 互動式圖表 | `interactive_rfm_plot.html` | 可互動的 RFM 分析圖 |

---

## ❓ 常見問題

### Q1: 如何快速重新生成圖表？

**A**: 使用以下任一方法：
```bash
# 方法 1: CLI 工具（推薦）
customer-seg plots --all

# 方法 2: 專用腳本
python scripts/regenerate_plots.py

# 方法 3: 完整流程
customer-seg full-pipeline data/raw/data.csv
```

### Q2: 找不到資料檔案怎麼辦？

**A**: 系統會自動尋找以下位置的資料檔案：
- `data/raw/data.csv`
- `data.csv`
- `data/results/cleaned_data.csv`

如果都找不到，請手動指定：
```bash
customer-seg plots /path/to/your/data.csv --all
```

### Q3: 如何只生成特定類型的圖表？

**A**: 使用 `--type` 參數：
```bash
customer-seg plots --type rfm          # 只生成 RFM 分布圖
customer-seg plots --type segments     # 只生成客戶分群圖
customer-seg plots --type interactive  # 只生成互動式圖表
```

### Q4: 互動式圖表無法開啟？

**A**: 嘗試以下解決方案：
1. 確認圖表已生成：`ls plots/interactive_rfm_plot.html`
2. 使用 CLI 工具：`customer-seg interactive --open-browser`
3. 使用本地伺服器：
   ```bash
   python -m http.server 8000
   # 訪問：http://localhost:8000/plots/interactive_rfm_plot.html
   ```

### Q5: 如何更新報告中的圖表？

**A**: 報告已經整合了所有圖表，只需確保圖表檔案存在：
```bash
# 重新生成圖表
customer-seg plots --all

# 檢查報告狀態
customer-seg report
```

### Q6: 如何查看所有可用的命令？

**A**: 使用幫助命令：
```bash
customer-seg --help              # 查看所有命令
customer-seg plots --help        # 查看 plots 命令選項
customer-seg interactive --help  # 查看 interactive 命令選項
```

---

## 🎯 推薦工作流程

### 日常使用

```bash
# 1. 快速重新生成所有圖表
customer-seg plots --all

# 2. 查看互動式圖表
customer-seg interactive --open-browser

# 3. 檢查報告
open docs/class_report.md  # macOS
xdg-open docs/class_report.md  # Linux
```

### 完整分析

```bash
# 1. 執行完整分析流程
customer-seg full-pipeline data/raw/data.csv

# 2. 查看結果
customer-seg interactive --open-browser
```

### 問題排除

```bash
# 1. 驗證資料
customer-seg validate data/raw/data.csv

# 2. 查看系統資訊
customer-seg info

# 3. 重新設置環境
bash scripts/setup.sh
```

---

## 📞 需要幫助？

- 📖 查看完整文檔：`README.md`
- 🔧 查看系統資訊：`customer-seg info`
- 📊 查看分析報告：`docs/class_report.md`
- 🌐 查看互動式圖表：`customer-seg interactive`

---

**最後更新**：2025年5月31日  
**版本**：1.0.0
