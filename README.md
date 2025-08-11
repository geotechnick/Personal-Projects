# Personal-Projects

## EMPCO Automated Slope Stability Analysis System

This repository contains a **production-ready** automated geotechnical engineering analysis system that determines which slope configurations require detailed pipeline soil springs analysis. The system integrates **true headless GeoStudio analysis** via PyGeoStudio with pipeline stress calculations to create comprehensive decision matrices for engineering assessment.

> **🔥 Key Innovation**: Uses PyGeoStudio for direct .gsz file manipulation - **no GeoStudio GUI required** for real slope stability analysis!

## Overview

The **EMPCO (Energy Management and Pipeline Consulting Operations)** project automates the traditionally manual process of:
1. Running slope stability analyses for various configurations
2. Determining which slopes require detailed soil springs analysis  
3. Calculating pipeline stresses for critical configurations
4. Generating decision matrices with engineering recommendations

## Key Features

- **🏗️ True GeoStudio Integration**: Direct .gsz file manipulation via PyGeoStudio - **actual slope stability analysis without GUI**
- **📊 Automated Parametric Analysis**: Tests hundreds of slope configurations varying angle (15-45°), height (20-100 ft), and soil properties  
- **🎯 Decision Matrix Generation**: Automatically determines which configurations need detailed analysis based on Factor of Safety thresholds
- **📋 Excel Integration**: Leverages existing `Soil Springs_2024.xlsx` calculations for pipeline analysis in background mode
- **📈 Comprehensive Reporting**: Executive summaries, visualization plots, priority classifications with timelines and costs
- **⚡ Scalable Workflow**: From small studies (10 configs) to large parametric analyses (1000+ configs)
- **🔄 Intelligent Fallbacks**: Graceful degradation when software unavailable
- **📊 Advanced Visualizations**: Detailed slope geometry plots with soil layers, failure surfaces, and pipeline locations

## Quick Start

### Prerequisites & Installation

**🚀 Automatic Setup (Recommended):**
```bash
cd EMPCO
python setup_environment.py
```

**Manual Installation:**
```bash
# Core dependencies
pip install xlwings pandas matplotlib seaborn numpy openpyxl

# PyGeoStudio for true GeoStudio integration (HIGHLY RECOMMENDED)
pip install PyGeoStudio
```

**🎯 Analysis Capability Hierarchy:**
1. **PyGeoStudio Integration** ⭐ **BEST** ⭐
   - Direct .gsz file manipulation
   - **Real GeoStudio analysis without GUI**
   - Actual Factor of Safety calculations
   - Production-ready for engineering use

2. **GeoStudio CLI Fallback**
   - Uses GeoStudio command-line if installed
   - Requires GeoStudio software

3. **Intelligent Simulation**
   - Realistic engineering-based calculations
   - No external software required

4. **Excel Background Processing**
   - Hidden Excel automation
   - No visible Excel windows

### Basic Usage

**🎯 Quick Demo (10 slope configurations):**
```bash
cd EMPCO
python automated_decision_workflow.py --limit 10
```

**⚡ Production Analysis (100+ configurations):**
```bash
python automated_decision_workflow.py --limit 200
```

**🔧 Advanced Options:**
```bash
# Custom output directory
python automated_decision_workflow.py --output "my_analysis_results" --limit 50

# Skip plots for faster execution
python automated_decision_workflow.py --no-plots --limit 100

# Check system capabilities
python setup_environment.py
```

**📊 View Results:**
Results are automatically saved to `analysis_results/` directory with:
- **CSV files**: Comprehensive decision matrices and recommendations
- **Statistical plots**: Factor of Safety distributions and priority analysis  
- **Slope geometry plots**: Detailed visualizations showing slope profiles, soil layers, failure surfaces, and pipeline locations
- **Executive summary**: Management report with key findings and action items

## 📋 Parameter Input Methods

Users can specify slope, soil, and pipeline parameters using **5 flexible methods**:

### **1. Configuration Files (Recommended)**
```bash
# Create template files first
python automated_decision_workflow.py --create-templates

# Use JSON configuration
python automated_decision_workflow.py --config-json "my_project.json"

# Use YAML configuration  
python automated_decision_workflow.py --config-yaml "my_project.yaml"

# Use Excel configuration
python automated_decision_workflow.py --config-excel "my_project.xlsx"
```

### **2. Interactive Input**
```bash
python automated_decision_workflow.py --interactive
```

### **3. Command Line Overrides**
```bash
python automated_decision_workflow.py --angles "25,30,35" --heights "40,60,80" --project-name "Site Alpha"
```

### **4. Example Parameter Categories:**

**🏔️ Slope Parameters:**
- Angles: 15-45 degrees
- Heights: 20-100 feet
- Groundwater ratios: 0.5-0.9

**🌍 Soil Parameters:**
- Unit weight: 110-140 pcf
- Cohesion: 50-500 psf  
- Friction angle: 15-40 degrees

**🔧 Pipeline Parameters:**
- Sizes: 16"-36" diameter
- Grades: X-52 to X-70
- Pressures: 1000-1600 psi

### **5. Template Files Generated:**
- `project_parameters_template.json`
- `project_parameters_template.yaml`
- `project_parameters_template.xlsx`

See **`PARAMETER_INPUT_GUIDE.md`** for detailed configuration examples and engineering guidance.

## PyGeoStudio Integration Details

### **🏗️ What PyGeoStudio Enables:**

- **Direct .gsz Manipulation**: Read/modify GeoStudio files in Python without GUI
- **True Slope Analysis**: Actual Factor of Safety calculations using GeoStudio's engine
- **Parametric Automation**: Programmatically vary slope geometry and materials
- **Real Results Extraction**: Get actual critical slip surfaces and safety factors
- **Production Ready**: Suitable for engineering consulting and large-scale studies

### **🔄 Workflow with PyGeoStudio:**

1. **Load Template**: `model = pgs.load_gsz("SlopeTemplate.gsz")`
2. **Modify Parameters**: Update slope angle, height, soil properties programmatically
3. **Run Analysis**: `results = model.solve()` - actual GeoStudio computation
4. **Extract Results**: Get real Factor of Safety values and slip surface data
5. **Decision Matrix**: Use actual results to determine analysis requirements

### **🎯 System Intelligence:**

The system automatically detects available capabilities:
- ✅ **PyGeoStudio Available**: Uses real GeoStudio analysis
- ⚠️ **PyGeoStudio Missing**: Falls back to CLI or simulation
- 🔧 **No GeoStudio**: Uses intelligent engineering-based calculations

## Understanding the Results

### Key Output Files:

**📊 Analysis Results:**
- **`slope_stability_decision_matrix.csv`**: Initial slope analysis showing which configurations need detailed review
- **`comprehensive_decision_matrix.csv`**: Full analysis including pipeline stress calculations
- **`configuration_recommendations.csv`**: Specific action items with timelines and cost estimates

**📈 Statistical Visualizations:**
- **`analysis_summary_plots.png`**: Factor of Safety distributions and priority analysis
- **`decision_matrix_heatmap.png`**: Priority heatmap for pipeline sizes vs slope conditions

**🏔️ Slope Geometry Visualizations:**
- **`slope_configurations_comparison.png`**: Side-by-side comparison of critical slopes
- **`slope_geometry_*.png`**: Individual detailed plots for each critical configuration showing:
  - Accurate slope profile with dimensions and angles
  - Soil layer stratification with engineering properties
  - Critical failure surface visualization
  - Pipeline location and cross-section details
  - Groundwater table representation
  - Comprehensive engineering annotations
- **`geometry_data_*.json`**: Complete geometric parameters and analysis data in JSON format
- **`slope_geometry_plots_index.txt`**: Complete catalog of all generated visualizations

**📋 Reports:**
- **`executive_summary.txt`**: Executive summary with key findings and recommendations

### Priority Classifications:
- **Critical (1)**: FoS < 1.0 or pipeline stress exceeds allowable - Immediate action (0-7 days)
- **High (2)**: FoS < 1.2 - Short-term action (1-4 weeks)
- **Medium (3)**: FoS < 1.5 - Medium-term review (1-3 months)
- **Low (4)**: FoS > 1.5 - Long-term monitoring (6-12 months)

## System Architecture

### Core Components:
1. **`slope_stability_automation.py`**: GeoStudio XML template manipulation and slope analysis
2. **`soil_springs_integration.py`**: Integration with Excel-based soil springs calculations  
3. **`automated_decision_workflow.py`**: Complete workflow orchestrator with reporting
4. **`slope_geometry_visualizer.py`**: Advanced slope geometry visualization system ⭐ **NEW**

### Analysis Workflow:
1. **Configuration Generation**: Creates parametric matrix of slope configurations
2. **Slope Stability Analysis**: Calculates Factor of Safety for each configuration
3. **Decision Logic**: Determines which configurations require detailed analysis (FoS < 1.5)
4. **Pipeline Integration**: For critical configurations, runs soil springs analysis with various pipeline sizes
5. **Visualization Generation**: Creates detailed slope geometry plots for critical configurations ⭐ **NEW**
6. **Results Generation**: Creates comprehensive decision matrices and engineering recommendations

## Manual Validation

### Verify Results Against Manual Calculations:
1. Open `Soil Springs_2024.xlsx`
2. Compare automated inputs/outputs with manual calculations
3. Cross-reference Factor of Safety calculations with GeoStudio results
4. Validate decision matrix logic against engineering judgment

### Individual Module Testing:
```bash
# Test slope stability analysis only
python slope_stability_automation.py

# Test Excel integration
python soil_springs_integration.py

# Extract formulas for documentation  
python read_soil_springs.py
```

## Engineering Standards

The system follows established engineering practices:
- **ASCE Guidelines** for pipeline design
- **API 5L** pipeline specifications  
- **Geotechnical Engineering Standards** for slope stability
- **Factor of Safety thresholds** per industry practice

## File Structure

```
EMPCO/
├── automated_decision_workflow.py    # 🎯 Main workflow orchestrator
├── slope_stability_automation.py     # Slope analysis engine  
├── pygeostudio_interface.py         # ⭐ PyGeoStudio integration
├── soil_springs_integration.py       # Excel integration
├── headless_excel_analyzer.py        # Headless Excel processing
├── geostudio_cli_interface.py        # GeoStudio CLI fallback
├── slope_geometry_visualizer.py      # ⭐ Advanced slope geometry visualization
├── parameter_input_system.py         # 📋 User parameter input system
├── setup_environment.py              # 🚀 Automatic setup utility
├── read_soil_springs.py             # Formula extraction utility
├── Soil Springs_2024.xlsx           # Pipeline analysis spreadsheet
├── Slope Template/                   # GeoStudio templates
│   ├── SlopeTemplate.gsz            # ⭐ Main template for PyGeoStudio
│   └── uncompressed/SlopeTemplate.xml # XML fallback
├── examples/                         # 📁 Example configuration files
│   ├── example_project_config.json  # Complete project example
│   ├── simple_config.yaml           # Minimal configuration
│   └── README.md                     # Examples documentation
├── references/                       # 📚 Reference documents and manuals
├── analysis_results/                 # 📊 Output directory (created)
├── system_config.json               # System capabilities config
├── PARAMETER_INPUT_GUIDE.md          # 📖 User guide for parameters
└── project_parameters_template.*     # 📋 Template files (created)
```

## Limitations & Future Enhancements

### Current Capabilities & Limitations:

**✅ Fully Operational:**
- **PyGeoStudio Integration**: Direct .gsz file manipulation (recommended approach)
- **Excel Headless Processing**: Background Excel calculations with no GUI
- **Advanced Visualizations**: Detailed slope geometry plots with failure surfaces and pipeline locations
- **Intelligent Fallbacks**: Realistic simulations when software unavailable
- **Scalable Analysis**: From 10 to 1000+ configurations

**⚠️ Limitations:**
- Complex slope geometries (benches, multi-stage) require template customization
- PyGeoStudio installation needed for true GeoStudio integration
- Some GeoStudio features may require specific versions

### Planned Enhancements:
- Direct GeoStudio API integration
- Complex slope geometry support (benches, multi-layer slopes)
- Database storage for configuration management
- Web dashboard for results visualization
- Machine learning for improved decision thresholds

## Support & Documentation

- See `CLAUDE.md` for detailed technical documentation
- Check `executive_summary.txt` in results for analysis-specific findings
- Review individual CSV files for detailed configuration data
- Examine `analysis_summary_plots.png` for visual insights

## License

MIT License - See LICENSE file for details.