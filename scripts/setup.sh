#!/bin/bash

# 🛍️ 客戶分群分析系統快速設置腳本
# Customer Segmentation Analysis System Quick Setup Script

set -e  # 遇到錯誤時停止執行

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 函數：打印帶顏色的訊息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🛍️  $1${NC}"
}

# 檢查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 主函數
main() {
    print_header "客戶分群分析系統 - 快速設置"
    print_header "Customer Segmentation Analysis System - Quick Setup"
    echo ""
    
    # 檢查 Python 版本
    print_info "檢查 Python 版本 Checking Python version..."
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python 版本 Python version: $PYTHON_VERSION"
    else
        print_error "Python 3 未安裝 Python 3 not found"
        exit 1
    fi
    
    # 檢查 Conda
    print_info "檢查 Conda 環境 Checking Conda environment..."
    if command_exists conda; then
        print_success "Conda 已安裝 Conda is installed"
        
        # 建立 Conda 環境
        print_info "建立 Conda 環境 Creating Conda environment..."
        if conda env list | grep -q "customer-segmentation"; then
            print_warning "環境已存在，跳過建立 Environment exists, skipping creation"
        else
            conda env create -f environment.yml
            print_success "Conda 環境建立完成 Conda environment created"
        fi
        
        # 啟動環境並安裝 Poetry 依賴
        print_info "啟動環境並安裝依賴 Activating environment and installing dependencies..."
        eval "$(conda shell.bash hook)"
        conda activate customer-segmentation
        
        # 檢查 Poetry
        if command_exists poetry; then
            print_success "Poetry 已安裝 Poetry is installed"
            poetry install
            print_success "Poetry 依賴安裝完成 Poetry dependencies installed"
        else
            print_warning "Poetry 未找到，使用 pip 安裝依賴 Poetry not found, using pip"
            pip install -r requirements.txt
        fi
        
    else
        print_warning "Conda 未安裝，使用 Poetry 或 pip Conda not found, using Poetry or pip"
        
        # 檢查 Poetry
        if command_exists poetry; then
            print_success "Poetry 已安裝 Poetry is installed"
            poetry install
            print_success "Poetry 依賴安裝完成 Poetry dependencies installed"
        else
            print_warning "Poetry 未安裝，使用 pip Poetry not installed, using pip"
            pip install -r requirements.txt
            print_success "Pip 依賴安裝完成 Pip dependencies installed"
        fi
    fi
    
    # 建立必要目錄
    print_info "建立專案目錄 Creating project directories..."
    mkdir -p data/{raw,processed,results}
    mkdir -p logs
    mkdir -p plots
    print_success "目錄建立完成 Directories created"
    
    # 檢查資料檔案
    print_info "檢查資料檔案 Checking data files..."
    if [ -f "data.csv" ]; then
        print_info "發現資料檔案，移動到 data/raw/ Found data file, moving to data/raw/"
        cp data.csv data/raw/
        print_success "資料檔案已移動 Data file moved"
    elif [ -f "data/raw/data.csv" ]; then
        print_success "資料檔案已存在於正確位置 Data file exists in correct location"
    else
        print_warning "未找到資料檔案 data.csv，請手動放入 data/raw/ 目錄"
        print_warning "Data file data.csv not found, please manually place it in data/raw/ directory"
    fi
    
    # 設置執行權限
    print_info "設置執行權限 Setting execution permissions..."
    chmod +x scripts/*.py 2>/dev/null || true
    chmod +x scripts/*.sh 2>/dev/null || true
    print_success "執行權限設置完成 Execution permissions set"
    
    # 測試安裝
    print_info "測試安裝 Testing installation..."
    if command_exists conda && conda env list | grep -q "customer-segmentation"; then
        eval "$(conda shell.bash hook)"
        conda activate customer-segmentation
    fi
    
    # 測試 Python 導入
    python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    # 測試基本模組導入
    import customer_segmentation
    print('✅ 基本套件導入成功 Basic package import successful')
    
    # 測試核心模組
    from customer_segmentation.data.loader import DataLoader
    from customer_segmentation.data.cleaner import DataCleaner
    print('✅ 資料模組導入成功 Data modules import successful')
    
    # 測試分析模組
    from customer_segmentation.analysis.rfm_calculator import RFMCalculator
    print('✅ 分析模組導入成功 Analysis modules import successful')
    
    # 測試視覺化模組
    from customer_segmentation.visualization.visualizer import DataVisualizer
    print('✅ 視覺化模組導入成功 Visualization modules import successful')
    
    # 測試工具模組
    from customer_segmentation.utils.config import get_config
    from customer_segmentation.utils.logger import get_logger
    print('✅ 工具模組導入成功 Utility modules import successful')
    
    # 最後測試主要管道類別
    from customer_segmentation.pipeline import CustomerSegmentationPipeline
    print('✅ 主要管道類別導入成功 Main pipeline class import successful')
    
    print('🎉 所有套件導入測試通過 All package import tests passed')
except ImportError as e:
    print(f'❌ 套件導入失敗 Package import failed: {e}')
    print('💡 請檢查依賴是否正確安裝 Please check if dependencies are properly installed')
    sys.exit(1)
except Exception as e:
    print(f'❌ 測試過程發生錯誤 Error during testing: {e}')
    sys.exit(1)
" || {
        print_error "套件測試失敗 Package test failed"
        print_warning "這可能是因為缺少某些依賴套件 This might be due to missing dependencies"
        print_info "請嘗試重新安裝依賴 Please try reinstalling dependencies:"
        if command_exists conda; then
            echo "  conda activate customer-segmentation"
            echo "  poetry install"
        else
            echo "  poetry install"
        fi
        exit 1
    }
    
    print_success "安裝測試通過 Installation test passed"
    
    # 顯示使用說明
    echo ""
    print_header "🚀 設置完成！Setup Complete!"
    echo ""
    print_info "現在您可以使用以下方式開始分析 Now you can start analysis using:"
    echo ""
    echo "🔥 推薦使用方式 Recommended Usage:"
    echo "1. 一鍵完整分析 One-click full analysis:"
    if command_exists conda; then
        echo "   conda activate customer-segmentation"
    fi
    echo "   customer-seg full-pipeline data/raw/data.csv"
    echo ""
    echo "2. 快速重新生成圖表 Quick plot regeneration:"
    echo "   customer-seg plots --all"
    echo ""
    echo "3. 查看互動式圖表 View interactive plots:"
    echo "   customer-seg interactive --open-browser"
    echo ""
    echo "📊 其他分析選項 Other Analysis Options:"
    echo "4. 基本分析 Basic analysis:"
    echo "   customer-seg analyze data/raw/data.csv"
    echo ""
    echo "5. 使用 Python 腳本 Using Python script:"
    echo "   python scripts/run_analysis.py"
    echo ""
    echo "6. 使用 Jupyter Notebook:"
    echo "   jupyter lab notebooks/customer_segmentation_report.ipynb"
    echo ""
    echo "🛠️ 實用工具 Utility Commands:"
    echo "7. 驗證資料 Validate data:"
    echo "   customer-seg validate data/raw/data.csv"
    echo ""
    echo "8. 更新報告 Update report:"
    echo "   customer-seg report --update-plots"
    echo ""
    echo "9. 系統資訊 System info:"
    echo "   customer-seg info"
    echo ""
    print_info "更多使用說明請參考 README.md For more usage instructions, see README.md"
    
    # 檢查是否有資料檔案
    if [ ! -f "data/raw/data.csv" ]; then
        echo ""
        print_warning "⚠️  請記得將您的資料檔案放入 data/raw/data.csv"
        print_warning "⚠️  Please remember to place your data file at data/raw/data.csv"
    fi
}

# 執行主函數
main "$@"
