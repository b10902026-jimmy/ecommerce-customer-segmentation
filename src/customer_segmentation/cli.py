"""
命令列介面 - Command Line Interface

提供現代化的 CLI 介面，使用 Click 和 Rich 進行美化。
"""

from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from customer_segmentation.pipeline import CustomerSegmentationPipeline
from customer_segmentation.utils.config import get_config
from customer_segmentation.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


def print_banner():
    """顯示程式橫幅"""
    banner = """
🛍️  客戶分群分析系統
   Customer Segmentation Analysis System
   
   基於 RFM 模型的客戶分群分析工具
   RFM-based Customer Segmentation Analysis Tool
    """
    
    console.print(Panel(banner, style="bold blue", padding=(1, 2)))


@click.group()
@click.version_option(version="1.0.0")
@click.option('--debug', is_flag=True, help='啟用除錯模式 Enable debug mode')
@click.option('--config-file', type=click.Path(exists=True), help='配置檔案路徑 Config file path')
def cli(debug: bool, config_file: Optional[str]):
    """
    🛍️ 客戶分群分析系統 Customer Segmentation Analysis System
    
    基於 RFM (Recency, Frequency, Monetary) 模型的客戶分群分析工具。
    """
    if debug:
        console.print("🔧 除錯模式已啟用 Debug mode enabled", style="yellow")
    
    if config_file:
        console.print(f"📄 載入配置檔案 Loading config from: {config_file}", style="blue")


@cli.command()
@click.argument('data_file', type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(), help='輸出目錄 Output directory')
@click.option('--remove-outliers', is_flag=True, help='移除異常值 Remove outliers')
@click.option('--rfm-bins', default=5, help='RFM 分數分組數 RFM score bins')
@click.option('--analysis-date', help='分析日期 Analysis date (YYYY-MM-DD)')
@click.option('--no-plots', is_flag=True, help='不生成圖表 Skip plot generation')
@click.option('--quick', is_flag=True, help='快速分析模式 Quick analysis mode')
def analyze(
    data_file: str,
    output_dir: Optional[str],
    remove_outliers: bool,
    rfm_bins: int,
    analysis_date: Optional[str],
    no_plots: bool,
    quick: bool
):
    """
    執行客戶分群分析 Run customer segmentation analysis
    
    DATA_FILE: 輸入的 CSV 資料檔案路徑 Input CSV data file path
    """
    print_banner()
    
    console.print(f"📂 分析資料檔案 Analyzing data file: [bold]{data_file}[/bold]")
    
    # 建立管道
    config_override = {}
    if output_dir:
        config_override['results_dir'] = Path(output_dir)
    
    pipeline = CustomerSegmentationPipeline(config_override)
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            if quick:
                # 快速分析模式
                task = progress.add_task("🚀 執行快速分析 Running quick analysis...", total=None)
                
                pipeline.load_data(data_file)
                pipeline.clean_data(remove_outliers=remove_outliers)
                pipeline.calculate_rfm(analysis_date=analysis_date)
                pipeline.segment_customers(rfm_bins=rfm_bins)
                
                # 只匯出基本結果
                exported_files = pipeline.export_results()
                
                progress.update(task, description="✅ 快速分析完成 Quick analysis completed")
                
            else:
                # 完整分析模式
                task = progress.add_task("🔄 執行完整分析 Running full analysis...", total=None)
                
                results = pipeline.run_full_analysis(
                    file_path=data_file,
                    remove_outliers=remove_outliers,
                    rfm_bins=rfm_bins,
                    analysis_date=analysis_date,
                    create_plots=not no_plots,
                    export_results=True
                )
                
                # 確保圖表保存到 plots 目錄
                if not no_plots:
                    plots_dir = Path('plots')
                    plots_dir.mkdir(parents=True, exist_ok=True)
                    console.print(f"📁 圖表已保存到 Charts saved to: [bold]{plots_dir.absolute()}[/bold]")
                
                progress.update(task, description="✅ 完整分析完成 Full analysis completed")
                exported_files = results.get('exported_files', {})
        
        # 顯示結果摘要
        display_results_summary(pipeline, exported_files)
        
    except Exception as e:
        console.print(f"❌ 分析失敗 Analysis failed: {e}", style="bold red")
        raise click.ClickException(str(e))


@cli.command()
@click.argument('data_file', type=click.Path(exists=True))
def validate(data_file: str):
    """
    驗證資料檔案格式 Validate data file format
    
    DATA_FILE: 要驗證的 CSV 資料檔案 CSV data file to validate
    """
    console.print(f"🔍 驗證資料檔案 Validating data file: [bold]{data_file}[/bold]")
    
    try:
        from customer_segmentation.data.loader import DataLoader
        
        loader = DataLoader(data_file)
        df = loader.load_data()
        
        # 檢查必要欄位
        required_columns = [
            'InvoiceNo', 'StockCode', 'Description', 'Quantity',
            'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'
        ]
        
        # 建立驗證結果表格
        table = Table(title="資料驗證結果 Data Validation Results")
        table.add_column("檢查項目 Check Item", style="cyan")
        table.add_column("狀態 Status", style="green")
        table.add_column("詳細資訊 Details")
        
        # 檔案基本資訊
        table.add_row("檔案大小 File Size", "✅", f"{df.shape[0]:,} 行 rows, {df.shape[1]} 列 columns")
        
        # 欄位檢查
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            table.add_row("必要欄位 Required Columns", "❌", f"缺少 Missing: {missing_columns}")
        else:
            table.add_row("必要欄位 Required Columns", "✅", "所有必要欄位都存在 All required columns present")
        
        # 資料品質檢查
        missing_values = df.isnull().sum().sum()
        if missing_values > 0:
            table.add_row("缺失值 Missing Values", "⚠️", f"{missing_values:,} 個缺失值 missing values")
        else:
            table.add_row("缺失值 Missing Values", "✅", "無缺失值 No missing values")
        
        # 重複值檢查
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            table.add_row("重複記錄 Duplicates", "⚠️", f"{duplicates:,} 個重複記錄 duplicate records")
        else:
            table.add_row("重複記錄 Duplicates", "✅", "無重複記錄 No duplicate records")
        
        console.print(table)
        
        if missing_columns:
            console.print("❌ 資料驗證失敗 Data validation failed", style="bold red")
        else:
            console.print("✅ 資料驗證通過 Data validation passed", style="bold green")
            
    except Exception as e:
        console.print(f"❌ 驗證過程發生錯誤 Validation error: {e}", style="bold red")
        raise click.ClickException(str(e))


@cli.command()
def info():
    """顯示系統資訊 Show system information"""
    config = get_config()
    
    # 建立系統資訊表格
    table = Table(title="系統資訊 System Information")
    table.add_column("項目 Item", style="cyan")
    table.add_column("值 Value", style="green")
    
    table.add_row("專案名稱 Project Name", config.project_name)
    table.add_row("版本 Version", config.version)
    table.add_row("資料目錄 Data Directory", str(config.data_dir))
    table.add_row("結果目錄 Results Directory", str(config.results_dir))
    table.add_row("預設 RFM 分組 Default RFM Bins", str(config.rfm_bins))
    table.add_row("日誌級別 Log Level", config.log_level)
    
    console.print(table)


@cli.command()
@click.argument('data_file', type=click.Path(exists=True), required=False)
@click.option('--all', is_flag=True, help='重新生成所有圖表 Regenerate all plots')
@click.option('--type', 'plot_type', 
              type=click.Choice(['rfm', 'segments', 'correlation', 'geographic', 'timeseries', 'interactive']),
              help='指定圖表類型 Specify plot type')
@click.option('--output-dir', '-o', default='plots', help='輸出目錄 Output directory')
@click.option('--interactive', is_flag=True, help='同時生成互動式圖表 Also generate interactive plots')
def plots(data_file: Optional[str], all: bool, plot_type: Optional[str], output_dir: str, interactive: bool):
    """
    快速重新生成圖表 Quickly regenerate plots
    
    DATA_FILE: 資料檔案路徑（可選，會自動尋找） Data file path (optional, will auto-detect)
    """
    print_banner()
    
    # 自動尋找資料檔案
    if not data_file:
        possible_paths = [
            Path('data/raw/data.csv'),
            Path('data.csv'),
            Path('data/results/cleaned_data.csv')
        ]
        
        for path in possible_paths:
            if path.exists():
                data_file = str(path)
                break
        
        if not data_file:
            console.print("❌ 找不到資料檔案，請指定檔案路徑 Data file not found, please specify file path", style="bold red")
            raise click.ClickException("Data file not found")
    
    console.print(f"📊 重新生成圖表 Regenerating plots from: [bold]{data_file}[/bold]")
    console.print(f"📁 輸出目錄 Output directory: [bold]{output_dir}[/bold]")
    
    try:
        # 建立輸出目錄
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            if all or not plot_type:
                # 生成所有圖表
                task = progress.add_task("🎨 生成所有圖表 Generating all plots...", total=None)
                
                # 快速載入資料並生成圖表
                pipeline = CustomerSegmentationPipeline()
                pipeline.load_data(data_file)
                pipeline.clean_data()
                pipeline.calculate_rfm()
                pipeline.segment_customers()
                
                # 生成所有圖表
                from customer_segmentation.visualization.visualizer import DataVisualizer
                visualizer = DataVisualizer()
                
                plot_files = {
                    'RFM 分布圖': visualizer.plot_rfm_distributions(pipeline.rfm_data, save_path=output_path),
                    '客戶分群圖': visualizer.plot_customer_segments(pipeline.segmented_data, save_path=output_path),
                    'RFM 相關性圖': visualizer.plot_rfm_correlation(pipeline.rfm_data, save_path=output_path),
                    '地理分析圖': visualizer.plot_geographic_analysis(pipeline.cleaned_data, save_path=output_path),
                    '時間序列圖': visualizer.plot_time_series_analysis(pipeline.cleaned_data, save_path=output_path)
                }
                
                if interactive:
                    plot_files['互動式圖表'] = visualizer.create_interactive_rfm_plot(
                        pipeline.rfm_data, save_path=output_path
                    )
                
                progress.update(task, description="✅ 所有圖表生成完成 All plots generated")
                
            else:
                # 生成指定類型的圖表
                task = progress.add_task(f"🎨 生成 {plot_type} 圖表 Generating {plot_type} plot...", total=None)
                
                pipeline = CustomerSegmentationPipeline()
                pipeline.load_data(data_file)
                pipeline.clean_data()
                pipeline.calculate_rfm()
                pipeline.segment_customers()
                
                from customer_segmentation.visualization.visualizer import DataVisualizer
                visualizer = DataVisualizer()
                
                plot_files = {}
                if plot_type == 'rfm':
                    plot_files['RFM 分布圖'] = visualizer.plot_rfm_distributions(pipeline.rfm_data, save_path=output_path)
                elif plot_type == 'segments':
                    plot_files['客戶分群圖'] = visualizer.plot_customer_segments(pipeline.segmented_data, save_path=output_path)
                elif plot_type == 'correlation':
                    plot_files['RFM 相關性圖'] = visualizer.plot_rfm_correlation(pipeline.rfm_data, save_path=output_path)
                elif plot_type == 'geographic':
                    plot_files['地理分析圖'] = visualizer.plot_geographic_analysis(pipeline.cleaned_data, save_path=output_path)
                elif plot_type == 'timeseries':
                    plot_files['時間序列圖'] = visualizer.plot_time_series_analysis(pipeline.cleaned_data, save_path=output_path)
                elif plot_type == 'interactive':
                    plot_files['互動式圖表'] = visualizer.create_interactive_rfm_plot(
                        pipeline.rfm_data, save_path=output_path
                    )
                
                progress.update(task, description=f"✅ {plot_type} 圖表生成完成 {plot_type} plot generated")
        
        # 顯示生成的圖表
        if plot_files:
            files_table = Table(title="📊 生成的圖表 Generated Plots")
            files_table.add_column("圖表類型 Plot Type", style="cyan")
            files_table.add_column("檔案路徑 File Path", style="green")
            
            for plot_name, file_path in plot_files.items():
                if file_path:
                    files_table.add_row(plot_name, str(file_path))
            
            console.print(files_table)
        
        console.print(f"✅ 圖表生成完成！Charts generated successfully! 📁 {output_path.absolute()}", style="bold green")
        
    except Exception as e:
        console.print(f"❌ 圖表生成失敗 Plot generation failed: {e}", style="bold red")
        raise click.ClickException(str(e))


@cli.command()
@click.option('--update-plots', is_flag=True, help='同時更新圖表 Also update plots')
@click.option('--template', help='指定報告模板 Specify report template')
@click.option('--output', default='docs/class_report.md', help='輸出檔案路徑 Output file path')
def report(update_plots: bool, template: Optional[str], output: str):
    """
    更新分析報告 Update analysis report
    
    整合最新的圖表到報告中 Integrate latest plots into report
    """
    console.print("📊 更新分析報告 Updating analysis report...")
    
    try:
        if update_plots:
            console.print("🎨 首先更新圖表 First updating plots...")
            # 呼叫 plots 命令來更新圖表
            from click.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(plots, ['--all'])
            if result.exit_code != 0:
                console.print("⚠️ 圖表更新失敗，繼續報告更新 Plot update failed, continuing with report update", style="yellow")
        
        # 檢查報告檔案是否存在
        report_path = Path(output)
        if not report_path.exists():
            console.print(f"❌ 報告檔案不存在 Report file not found: {report_path}", style="bold red")
            raise click.ClickException(f"Report file not found: {report_path}")
        
        # 檢查圖表檔案
        plots_dir = Path('plots')
        if not plots_dir.exists():
            console.print("⚠️ plots 目錄不存在，請先生成圖表 plots directory not found, please generate plots first", style="yellow")
            return
        
        # 驗證圖表檔案是否存在
        expected_plots = [
            'geographic_analysis.png',
            'rfm_distributions.png', 
            'customer_segments.png',
            'rfm_correlation.png',
            'time_series_analysis.png',
            'interactive_rfm_plot.html'
        ]
        
        missing_plots = []
        for plot_file in expected_plots:
            if not (plots_dir / plot_file).exists():
                missing_plots.append(plot_file)
        
        if missing_plots:
            console.print(f"⚠️ 缺少圖表檔案 Missing plot files: {missing_plots}", style="yellow")
            console.print("💡 建議執行: customer-seg plots --all", style="blue")
        
        console.print(f"✅ 報告已是最新版本 Report is up to date: [bold]{report_path.absolute()}[/bold]", style="bold green")
        console.print("📊 報告包含以下圖表 Report includes the following plots:")
        
        for plot_file in expected_plots:
            if (plots_dir / plot_file).exists():
                console.print(f"  ✅ {plot_file}")
            else:
                console.print(f"  ❌ {plot_file} (缺少 missing)")
        
    except Exception as e:
        console.print(f"❌ 報告更新失敗 Report update failed: {e}", style="bold red")
        raise click.ClickException(str(e))


@cli.command()
def list_commands():
    """
    顯示所有可用命令 Show all available commands
    
    列出系統中所有可用的命令及其功能說明
    List all available commands and their descriptions
    """
    print_banner()
    
    # 建立命令列表表格
    commands_table = Table(title="📋 可用命令列表 Available Commands")
    commands_table.add_column("命令 Command", style="cyan", width=20)
    commands_table.add_column("功能說明 Description", style="green", width=50)
    commands_table.add_column("範例 Example", style="yellow", width=40)
    
    # 添加所有命令
    commands_data = [
        (
            "analyze",
            "執行客戶分群分析\nRun customer segmentation analysis",
            "customer-seg analyze data.csv"
        ),
        (
            "validate", 
            "驗證資料檔案格式\nValidate data file format",
            "customer-seg validate data.csv"
        ),
        (
            "info",
            "顯示系統資訊\nShow system information",
            "customer-seg info"
        ),
        (
            "plots",
            "快速重新生成圖表\nQuickly regenerate plots",
            "customer-seg plots --all"
        ),
        (
            "report",
            "更新分析報告\nUpdate analysis report",
            "customer-seg report --update-plots"
        ),
        (
            "interactive",
            "顯示互動式圖表使用說明\nShow interactive plot usage",
            "customer-seg interactive --open-browser"
        ),
        (
            "full-pipeline",
            "執行完整分析流程\nRun complete analysis pipeline",
            "customer-seg full-pipeline data.csv"
        ),
        (
            "list-commands",
            "顯示所有可用命令\nShow all available commands",
            "customer-seg list-commands"
        )
    ]
    
    for command, description, example in commands_data:
        commands_table.add_row(command, description, example)
    
    console.print(commands_table)
    
    # 顯示常用選項
    options_table = Table(title="⚙️ 常用選項 Common Options")
    options_table.add_column("選項 Option", style="cyan", width=25)
    options_table.add_column("說明 Description", style="green", width=55)
    
    common_options = [
        ("--help, -h", "顯示命令幫助 Show command help"),
        ("--version", "顯示版本資訊 Show version information"),
        ("--debug", "啟用除錯模式 Enable debug mode"),
        ("--output-dir, -o", "指定輸出目錄 Specify output directory"),
        ("--config-file", "指定配置檔案 Specify config file"),
        ("--remove-outliers", "移除異常值 Remove outliers"),
        ("--rfm-bins", "設定 RFM 分組數 Set RFM bins count"),
        ("--analysis-date", "指定分析日期 Specify analysis date"),
        ("--no-plots", "跳過圖表生成 Skip plot generation"),
        ("--quick", "快速分析模式 Quick analysis mode")
    ]
    
    for option, description in common_options:
        options_table.add_row(option, description)
    
    console.print(options_table)
    
    # 顯示使用提示
    console.print("\n💡 使用提示 Usage Tips:", style="bold blue")
    console.print("1. 🔍 查看特定命令幫助 Get help for specific command: [bold]customer-seg [COMMAND] --help[/bold]")
    console.print("2. 🚀 快速開始 Quick start: [bold]customer-seg analyze data.csv[/bold]")
    console.print("3. 📊 完整流程 Complete pipeline: [bold]customer-seg full-pipeline data.csv[/bold]")
    console.print("4. 🎨 只生成圖表 Generate plots only: [bold]customer-seg plots --all[/bold]")
    console.print("5. ✅ 驗證資料 Validate data: [bold]customer-seg validate data.csv[/bold]")
    
    console.print("\n📚 更多資訊 More Information:")
    console.print("• 📖 快速指南 Quick Guide: [bold]docs/QUICK_START.md[/bold]")
    console.print("• 📊 分析報告 Analysis Report: [bold]docs/class_report.md[/bold]")
    console.print("• 🌐 專案首頁 Project Home: [bold]README.md[/bold]")


@cli.command()
@click.option('--open-browser', is_flag=True, help='自動開啟瀏覽器 Auto open browser')
def interactive(open_browser: bool):
    """
    顯示互動式圖表使用說明 Show interactive plot usage instructions
    """
    console.print(Panel(
        "🌐 互動式 RFM 分析圖表使用指南\n"
        "Interactive RFM Analysis Plot Usage Guide",
        style="bold blue", padding=(1, 2)
    ))
    
    # 檢查互動式圖表是否存在
    interactive_plot = Path('plots/interactive_rfm_plot.html')
    
    if interactive_plot.exists():
        console.print(f"✅ 互動式圖表已找到 Interactive plot found: [bold]{interactive_plot.absolute()}[/bold]")
        
        # 使用說明
        instructions_table = Table(title="📖 使用說明 Usage Instructions")
        instructions_table.add_column("功能 Feature", style="cyan")
        instructions_table.add_column("操作方式 How to Use", style="green")
        
        instructions_table.add_row("🔍 縮放探索", "滑鼠滾輪縮放，拖拽移動 Mouse wheel to zoom, drag to move")
        instructions_table.add_row("🎯 懸停資訊", "滑鼠懸停顯示客戶詳細資訊 Hover to show customer details")
        instructions_table.add_row("🎨 分群篩選", "點擊圖例隱藏/顯示群體 Click legend to hide/show segments")
        instructions_table.add_row("📊 多維度展示", "同時展示 R、F、M 三個維度 Shows R, F, M dimensions")
        instructions_table.add_row("💡 即時篩選", "可按客戶群體進行篩選 Filter by customer segments")
        
        console.print(instructions_table)
        
        # 開啟方式
        console.print("\n🚀 開啟方式 How to Open:")
        console.print(f"1. 瀏覽器開啟 Open in browser: [bold]file://{interactive_plot.absolute()}[/bold]")
        console.print("2. 或執行 Or run: [bold]python -m http.server 8000[/bold] 然後訪問 then visit [bold]http://localhost:8000/plots/interactive_rfm_plot.html[/bold]")
        
        if open_browser:
            try:
                import webbrowser
                webbrowser.open(f"file://{interactive_plot.absolute()}")
                console.print("🌐 已自動開啟瀏覽器 Browser opened automatically", style="bold green")
            except Exception as e:
                console.print(f"⚠️ 無法自動開啟瀏覽器 Cannot auto-open browser: {e}", style="yellow")
        
    else:
        console.print("❌ 互動式圖表不存在 Interactive plot not found", style="bold red")
        console.print("💡 請先生成圖表 Please generate plots first: [bold]customer-seg plots --interactive[/bold]")


@cli.command()
@click.argument('data_file', type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(), help='輸出目錄 Output directory')
@click.option('--rfm-bins', default=5, help='RFM 分數分組數 RFM score bins')
@click.option('--analysis-date', help='分析日期 Analysis date (YYYY-MM-DD)')
@click.option('--skip-report', is_flag=True, help='跳過報告更新 Skip report update')
def full_pipeline(data_file: str, output_dir: Optional[str], rfm_bins: int, analysis_date: Optional[str], skip_report: bool):
    """
    執行完整分析流程 Run complete analysis pipeline
    
    包含：資料分析 + 圖表生成 + 報告更新 + 使用說明
    Includes: Data analysis + Plot generation + Report update + Usage instructions
    
    DATA_FILE: 輸入的 CSV 資料檔案路徑 Input CSV data file path
    """
    print_banner()
    
    console.print(f"🚀 執行完整分析流程 Running complete analysis pipeline")
    console.print(f"📂 資料檔案 Data file: [bold]{data_file}[/bold]")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # 步驟 1: 執行完整分析
            task1 = progress.add_task("📊 執行資料分析 Running data analysis...", total=None)
            
            config_override = {}
            if output_dir:
                config_override['results_dir'] = Path(output_dir)
            
            pipeline = CustomerSegmentationPipeline(config_override)
            
            results = pipeline.run_full_analysis(
                file_path=data_file,
                remove_outliers=False,
                rfm_bins=rfm_bins,
                analysis_date=analysis_date,
                create_plots=True,
                export_results=True
            )
            
            progress.update(task1, description="✅ 資料分析完成 Data analysis completed")
            
            # 步驟 2: 生成所有圖表
            task2 = progress.add_task("🎨 生成圖表 Generating plots...", total=None)
            
            plots_dir = Path('plots')
            plots_dir.mkdir(parents=True, exist_ok=True)
            
            from customer_segmentation.visualization.visualizer import DataVisualizer
            visualizer = DataVisualizer()
            
            plot_files = {
                'RFM 分布圖': visualizer.plot_rfm_distributions(pipeline.rfm_data, save_path=plots_dir),
                '客戶分群圖': visualizer.plot_customer_segments(pipeline.segmented_data, save_path=plots_dir),
                'RFM 相關性圖': visualizer.plot_rfm_correlation(pipeline.rfm_data, save_path=plots_dir),
                '地理分析圖': visualizer.plot_geographic_analysis(pipeline.cleaned_data, save_path=plots_dir),
                '時間序列圖': visualizer.plot_time_series_analysis(pipeline.cleaned_data, save_path=plots_dir),
                '互動式圖表': visualizer.create_interactive_rfm_plot(
                    pipeline.rfm_data, save_path=plots_dir
                )
            }
            
            progress.update(task2, description="✅ 圖表生成完成 Plot generation completed")
            
            # 步驟 3: 更新報告（如果需要）
            if not skip_report:
                task3 = progress.add_task("📝 檢查報告 Checking report...", total=None)
                
                report_path = Path('docs/class_report.md')
                if report_path.exists():
                    progress.update(task3, description="✅ 報告已是最新 Report is up to date")
                else:
                    progress.update(task3, description="⚠️ 報告檔案不存在 Report file not found")
        
        # 顯示完整結果摘要
        display_results_summary(pipeline, results.get('exported_files', {}))
        
        # 顯示生成的圖表
        if plot_files:
            files_table = Table(title="📊 生成的圖表 Generated Plots")
            files_table.add_column("圖表類型 Plot Type", style="cyan")
            files_table.add_column("檔案路徑 File Path", style="green")
            
            for plot_name, file_path in plot_files.items():
                if file_path:
                    files_table.add_row(plot_name, str(file_path))
            
            console.print(files_table)
        
        # 顯示下一步指引
        console.print("\n🎯 下一步 Next Steps:", style="bold blue")
        console.print("1. 📊 查看報告 View report: [bold]docs/class_report.md[/bold]")
        console.print("2. 🌐 查看互動式圖表 View interactive plot: [bold]customer-seg interactive --open-browser[/bold]")
        console.print("3. 🔄 重新生成圖表 Regenerate plots: [bold]customer-seg plots --all[/bold]")
        
        console.print("\n✅ 完整分析流程執行完成！Complete analysis pipeline finished!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ 完整流程執行失敗 Complete pipeline failed: {e}", style="bold red")
        raise click.ClickException(str(e))


def display_results_summary(pipeline: CustomerSegmentationPipeline, exported_files: dict):
    """顯示分析結果摘要"""
    try:
        summary = pipeline.generate_analysis_summary()
        insights = pipeline.get_business_insights()
        
        # 資料概覽表格
        overview_table = Table(title="📊 資料概覽 Data Overview")
        overview_table.add_column("指標 Metric", style="cyan")
        overview_table.add_column("數值 Value", style="green")
        
        data_overview = summary['data_overview']
        overview_table.add_row("原始記錄數 Original Records", f"{data_overview['original_records']:,}")
        overview_table.add_row("清理後記錄數 Cleaned Records", f"{data_overview['cleaned_records']:,}")
        overview_table.add_row("資料保留率 Retention Rate", f"{data_overview['retention_rate']:.1f}%")
        overview_table.add_row("分析客戶數 Customers Analyzed", f"{data_overview['customers_analyzed']:,}")
        
        console.print(overview_table)
        
        # RFM 統計表格
        rfm_table = Table(title="🎯 RFM 統計 RFM Statistics")
        rfm_table.add_column("指標 Metric", style="cyan")
        rfm_table.add_column("平均值 Average", style="green")
        
        rfm_stats = summary['rfm_statistics']
        rfm_table.add_row("Recency (天 Days)", f"{rfm_stats['avg_recency']:.1f}")
        rfm_table.add_row("Frequency (次 Times)", f"{rfm_stats['avg_frequency']:.1f}")
        rfm_table.add_row("Monetary ($)", f"${rfm_stats['avg_monetary']:,.2f}")
        rfm_table.add_row("總營收 Total Revenue", f"${rfm_stats['total_revenue']:,.2f}")
        
        console.print(rfm_table)
        
        # 分群結果
        segmentation = summary['segmentation_results']
        console.print(f"👥 客戶分群數量 Customer Segments: [bold]{segmentation['total_segments']}[/bold]")
        
        # 業務洞察
        if 'champions' in insights:
            champions = insights['champions']
            console.print(
                f"🌟 Champions 客戶: [bold]{champions['count']}[/bold] 位 "
                f"({champions['percentage']:.1f}%), "
                f"貢獻營收 Revenue: [bold]${champions['revenue_contribution']:,.2f}[/bold]"
            )
        
        # 匯出檔案列表
        if exported_files:
            files_table = Table(title="📁 匯出檔案 Exported Files")
            files_table.add_column("檔案類型 File Type", style="cyan")
            files_table.add_column("檔案路徑 File Path", style="green")
            
            for file_type, file_path in exported_files.items():
                files_table.add_row(file_type, str(file_path))
            
            console.print(files_table)
        
    except Exception as e:
        console.print(f"⚠️ 無法顯示結果摘要 Cannot display results summary: {e}", style="yellow")


def main():
    """主入口點"""
    cli()


if __name__ == "__main__":
    main()
