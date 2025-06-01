#!/usr/bin/env python3
"""
快速圖表重新生成腳本 - Quick Plot Regeneration Script

專門用於快速重新生成所有分析圖表，無需重新執行完整分析。
"""

import sys
import argparse
from pathlib import Path

# 添加 src 目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from customer_segmentation.pipeline import CustomerSegmentationPipeline
from customer_segmentation.visualization.visualizer import DataVisualizer
from customer_segmentation.utils.logger import get_logger

logger = get_logger(__name__)


def print_banner():
    """顯示程式橫幅"""
    print("=" * 60)
    print("🎨 快速圖表重新生成工具")
    print("   Quick Plot Regeneration Tool")
    print("=" * 60)


def regenerate_all_plots(data_file: Path, output_dir: Path = None, interactive: bool = True):
    """
    重新生成所有圖表
    
    Args:
        data_file: 資料檔案路徑
        output_dir: 輸出目錄，預設為 plots/
        interactive: 是否生成互動式圖表
    """
    if output_dir is None:
        output_dir = project_root / "plots"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"📊 開始重新生成圖表 Starting plot regeneration")
    logger.info(f"📂 資料檔案 Data file: {data_file}")
    logger.info(f"📁 輸出目錄 Output directory: {output_dir}")
    
    try:
        # 快速載入資料並計算 RFM
        logger.info("🔄 載入資料並計算 RFM Loading data and calculating RFM...")
        pipeline = CustomerSegmentationPipeline()
        pipeline.load_data(data_file)
        pipeline.clean_data()
        pipeline.calculate_rfm()
        pipeline.segment_customers()
        
        # 建立視覺化器
        visualizer = DataVisualizer()
        
        # 生成所有圖表
        plot_files = {}
        
        logger.info("🎨 生成 RFM 分布圖 Generating RFM distributions plot...")
        plot_files['rfm_distributions'] = visualizer.plot_rfm_distributions(
            pipeline.rfm_data, save_path=output_dir
        )
        
        logger.info("🎨 生成客戶分群圖 Generating customer segments plot...")
        plot_files['customer_segments'] = visualizer.plot_customer_segments(
            pipeline.segmented_data, save_path=output_dir
        )
        
        logger.info("🎨 生成 RFM 相關性圖 Generating RFM correlation plot...")
        plot_files['rfm_correlation'] = visualizer.plot_rfm_correlation(
            pipeline.rfm_data, save_path=output_dir
        )
        
        logger.info("🎨 生成地理分析圖 Generating geographic analysis plot...")
        plot_files['geographic_analysis'] = visualizer.plot_geographic_analysis(
            pipeline.cleaned_data, save_path=output_dir
        )
        
        logger.info("🎨 生成時間序列圖 Generating time series plot...")
        plot_files['time_series_analysis'] = visualizer.plot_time_series_analysis(
            pipeline.cleaned_data, save_path=output_dir
        )
        
        if interactive:
            logger.info("🌐 生成互動式圖表 Generating interactive plot...")
            plot_files['interactive_rfm'] = visualizer.create_interactive_rfm_plot(
                pipeline.rfm_data, pipeline.segmented_data, save_path=output_dir
            )
        
        # 顯示結果
        logger.info("✅ 圖表生成完成！Plot generation completed!")
        logger.info("📊 生成的圖表 Generated plots:")
        
        for plot_name, file_path in plot_files.items():
            if file_path and file_path.exists():
                logger.info(f"  ✅ {plot_name}: {file_path}")
            else:
                logger.warning(f"  ❌ {plot_name}: 生成失敗 Generation failed")
        
        return plot_files
        
    except Exception as e:
        logger.error(f"❌ 圖表生成失敗 Plot generation failed: {e}")
        raise


def regenerate_specific_plot(data_file: Path, plot_type: str, output_dir: Path = None):
    """
    重新生成特定類型的圖表
    
    Args:
        data_file: 資料檔案路徑
        plot_type: 圖表類型
        output_dir: 輸出目錄
    """
    if output_dir is None:
        output_dir = project_root / "plots"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"🎨 重新生成 {plot_type} 圖表 Regenerating {plot_type} plot")
    
    try:
        # 載入資料
        pipeline = CustomerSegmentationPipeline()
        pipeline.load_data(data_file)
        pipeline.clean_data()
        pipeline.calculate_rfm()
        pipeline.segment_customers()
        
        # 建立視覺化器
        visualizer = DataVisualizer()
        
        # 根據類型生成圖表
        if plot_type == 'rfm':
            file_path = visualizer.plot_rfm_distributions(pipeline.rfm_data, save_path=output_dir)
        elif plot_type == 'segments':
            file_path = visualizer.plot_customer_segments(pipeline.segmented_data, save_path=output_dir)
        elif plot_type == 'correlation':
            file_path = visualizer.plot_rfm_correlation(pipeline.rfm_data, save_path=output_dir)
        elif plot_type == 'geographic':
            file_path = visualizer.plot_geographic_analysis(pipeline.cleaned_data, save_path=output_dir)
        elif plot_type == 'timeseries':
            file_path = visualizer.plot_time_series_analysis(pipeline.cleaned_data, save_path=output_dir)
        elif plot_type == 'interactive':
            file_path = visualizer.create_interactive_rfm_plot(
                pipeline.rfm_data, pipeline.segmented_data, save_path=output_dir
            )
        else:
            raise ValueError(f"不支援的圖表類型 Unsupported plot type: {plot_type}")
        
        if file_path and file_path.exists():
            logger.info(f"✅ {plot_type} 圖表生成完成 {plot_type} plot generated: {file_path}")
        else:
            logger.error(f"❌ {plot_type} 圖表生成失敗 {plot_type} plot generation failed")
        
        return file_path
        
    except Exception as e:
        logger.error(f"❌ {plot_type} 圖表生成失敗 {plot_type} plot generation failed: {e}")
        raise


def auto_find_data_file():
    """自動尋找資料檔案"""
    possible_paths = [
        project_root / "data" / "raw" / "data.csv",
        project_root / "data.csv",
        project_root / "data" / "results" / "cleaned_data.csv"
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None


def main():
    """主函數"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="快速重新生成分析圖表 Quick plot regeneration tool"
    )
    parser.add_argument(
        'data_file', 
        nargs='?',
        help='資料檔案路徑（可選，會自動尋找） Data file path (optional, will auto-detect)'
    )
    parser.add_argument(
        '--type', 
        choices=['rfm', 'segments', 'correlation', 'geographic', 'timeseries', 'interactive'],
        help='指定圖表類型 Specify plot type'
    )
    parser.add_argument(
        '--output-dir', '-o',
        type=Path,
        default=project_root / "plots",
        help='輸出目錄 Output directory'
    )
    parser.add_argument(
        '--no-interactive',
        action='store_true',
        help='不生成互動式圖表 Skip interactive plot generation'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='重新生成所有圖表 Regenerate all plots'
    )
    
    args = parser.parse_args()
    
    # 尋找資料檔案
    if args.data_file:
        data_file = Path(args.data_file)
        if not data_file.exists():
            logger.error(f"❌ 資料檔案不存在 Data file not found: {data_file}")
            sys.exit(1)
    else:
        data_file = auto_find_data_file()
        if not data_file:
            logger.error("❌ 找不到資料檔案，請指定檔案路徑 Data file not found, please specify file path")
            sys.exit(1)
        logger.info(f"🔍 自動找到資料檔案 Auto-detected data file: {data_file}")
    
    try:
        if args.type:
            # 生成特定類型的圖表
            regenerate_specific_plot(data_file, args.type, args.output_dir)
        else:
            # 生成所有圖表
            regenerate_all_plots(
                data_file, 
                args.output_dir, 
                interactive=not args.no_interactive
            )
        
        # 顯示使用說明
        print("\n" + "=" * 60)
        print("🎯 下一步 Next Steps:")
        print("1. 📊 查看報告 View report: docs/class_report.md")
        print("2. 🌐 查看互動式圖表 View interactive plot:")
        print("   python -c \"import webbrowser; webbrowser.open('plots/interactive_rfm_plot.html')\"")
        print("3. 🔄 使用 CLI 工具 Use CLI tool: customer-seg interactive --open-browser")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ 執行失敗 Execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
