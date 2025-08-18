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
- **⚡ Static Values Analysis**: Comprehensive parametric analysis of pipe-soil interactions with 2,275+ combinations per soil layer ⭐ **NEW**
- **🔧 Stress Assessment**: Automated determination of whether configurations exceed allowable stress limits
- **📈 Comprehensive Reporting**: Executive summaries, visualization plots, priority classifications with timelines and costs
- **⚡ Scalable Workflow**: From small studies (10 configs) to large parametric analyses (1000+ configs)
- **🔄 Intelligent Fallbacks**: Graceful degradation when software unavailable with robust error handling
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
   - Hidden Excel automation with robust connection management
   - No visible Excel windows
   - Automatic fallback to mock results if Excel unavailable

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

**⚡ Static Values Parametric Analysis:**
```bash
# Fast parametric analysis (RECOMMENDED - 2,275 combinations per soil layer)
python efficient_static_values_calculator.py

# Basic parameter combinations (static values only)
python static_values_iterator.py

# Enhanced Excel integration (requires Excel)
python enhanced_static_values_iterator.py

# Extract soil springs parameter combinations (9,000 total)
python soil_springs_extractor.py
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

**Slope Analysis Results** (saved to `analysis_results/`):
- **CSV files**: Comprehensive decision matrices and recommendations
- **Statistical plots**: Factor of Safety distributions and priority analysis  
- **Slope geometry plots**: Detailed visualizations showing slope profiles, soil layers, failure surfaces, and pipeline locations
- **Executive summary**: Management report with key findings and action items

**Static Values Analysis Results** ⭐ **NEW** (saved to `efficient_static_values_output/`):
- **`Stiff_Fat_Clay_calculations.csv`**: 2,275 parameter combinations with stress analysis
- **`Stiff_Lean_Clay_calculations.csv`**: Complete analysis for lean clay conditions
- **`Dense_Silty_Sand_Clayey_Sand_calculations.csv`**: Sandy soil parametric analysis
- **Key Features**: DOC (1-25 ft) and Length (10-100 ft) in 1-foot increments
- **Stress Assessment**: Clear "Does Not Exceed" vs "Exceeds" allowable stress determination
- **Engineering Standards**: Based on API RP 1111 and geotechnical engineering principles

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
- **PGD Orientations: Parallel AND Perpendicular to slope** ⭐ **NEW**

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

### **🎯 System Intelligence & Error Handling:**

The system automatically detects available capabilities and handles errors gracefully:
- ✅ **PyGeoStudio Available**: Uses real GeoStudio analysis
- ⚠️ **PyGeoStudio Missing**: Falls back to CLI or simulation
- 🔧 **No GeoStudio**: Uses intelligent engineering-based calculations
- 📋 **Excel Unavailable**: Provides mock results based on engineering principles
- 🛡️ **Connection Issues**: Robust error handling prevents workflow failures

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

## 🔬 Static Values Analysis Details ⭐ **NEW**

### **Parametric Analysis Scope:**
- **Total Configurations**: 2,275 parameter combinations per soil layer
- **Pipe DOC Range**: 1-25 feet in 1-foot increments (25 values)
- **Pipe Length Range**: 10-100 feet in 1-foot increments (91 values)
- **Soil Layers**: 3 distinct soil types (Stiff Fat Clay, Stiff Lean Clay, Dense Silty Sand/Clayey Sand)
- **Total Analysis**: 6,825 configurations across all soil types

### **CSV Output Format:**
Each CSV file contains the following columns (matching Excel Soil Springs_2024.xlsx layout):

**📋 Input Parameters** (Excel cells B3:B9):
- `Pipe OD (in)`: Pipe outer diameter (16 inches - static)
- `Pipe wt (in)`: Wall thickness (0.375 inches - static)  
- `Pipe SMYS (psi)`: Specified minimum yield strength (X-42 - static)
- `Pipe DOC (ft)`: Depth of cover (1-25 ft - variable)
- `Length of Pipe in PGD (ft)`: Length in permanent ground deformation zone (10-100 ft - variable)
- `Pipe Coating`: Surface coating type (Rough Steel - static)
- `Internal Pressure (psi)`: Operating pressure (1500 psi - static)

**🌍 Soil Parameters** (Excel cells E3:E6):
- `Soil Friction Angle (φ degrees)`: Internal friction angle (varies by soil type)
- `Soil Cohesion (c, psf)`: Cohesive strength (varies by soil type)
- `Soil Effective Unit Weight (γ', psf)`: Effective unit weight (varies by soil type)
- `PGD Path (perpendicular/parallel to pipe)`: Loading orientation (Parallel - static)

**⚙️ Calculated Results** (Excel cells B13:B17):
- `Longitudinal Force (lb/ft)`: Soil resistance force per unit length
- `Axial Stress (psi)`: Calculated axial stress in pipe wall
- `Remaining Allowable Stress (psi)`: Available stress capacity before failure
- `Allowable Pipe Length in PGD (ft)`: Maximum safe length for current conditions
- `Exceeds Allowable`: **Critical determination: "Does Not Exceed" or "Exceeds"**

### **Engineering Calculations:**
The analysis uses advanced soil springs formulas based on:
- **API RP 1111**: Recommended Practice for Design, Construction, and Inspection of Offshore Hydrocarbon Pipelines
- **Geotechnical Standards**: Passive earth pressure theory, soil-structure interaction
- **Pipeline Stress Analysis**: Combined axial and hoop stress calculations
- **Safety Factors**: Industry-standard allowable stress criteria (72% of SMYS)

### **Stress Assessment Logic:**
- **"Does Not Exceed"**: Total applied stress ≤ Allowable stress (Safe operation)
- **"Exceeds"**: Total applied stress > Allowable stress (Requires engineering attention)
- **Conservative Approach**: Combines axial stress from soil loading with hoop stress from internal pressure

### **Example Results by Soil Type:**

**Stiff Fat Clay (CH)**:
- Friction Angle: 26°, Cohesion: 100 psf, Unit Weight: 120 pcf
- Example: DOC=1ft, Length=10ft → Axial Stress=258 psi → "Does Not Exceed"
- Example: DOC=25ft, Length=100ft → Axial Stress=34,547 psi → "Exceeds"

**Dense Silty Sand/Clayey Sand (SM/SC)**:
- Friction Angle: 35°, Cohesion: 100 psf, Unit Weight: 120 pcf
- Higher friction angle results in increased soil resistance
- More configurations likely to exceed allowable stress limits

### **Using the Results:**
1. **Filter for "Exceeds" cases**: Focus on configurations requiring design modifications
2. **Analyze DOC vs Length trends**: Identify safe operating envelopes  
3. **Compare soil types**: Understand soil-dependent risk factors
4. **Engineering Decision**: Use results for pipeline route planning and design optimization

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

# Test static values parametric analysis (FAST)
python efficient_static_values_calculator.py

# Test soil springs parameter extraction
python soil_springs_extractor.py
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
├── soil_springs_extractor.py        # ⭐ Headless soil springs extraction
├── static_values_iterator.py        # 📊 Static values parameter combinations
├── enhanced_static_values_iterator.py # 🧮 Enhanced Excel integration
├── efficient_static_values_calculator.py # ⚡ Fast parametric analysis
├── Static Values.xlsx               # 📋 Pipe and soil assumptions
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
├── test_output/                      # Test results directory (empty after cleanup)
├── static_values_output/             # 📈 Static values basic output
├── enhanced_static_values_output/    # 🧮 Enhanced Excel calculations
├── efficient_static_values_output/   # ⚡ Fast parametric analysis results
├── system_config.json               # System capabilities config
├── PARAMETER_INPUT_GUIDE.md          # 📖 User guide for parameters
└── project_parameters_template.*     # 📋 Template files (created)
```

**🧹 Recent Cleanup:** Removed 8 temporary test directories and 33 unused files to streamline the repository.

## Limitations & Future Enhancements

### Current Capabilities & Limitations:

**✅ Fully Operational:**
- **PyGeoStudio Integration**: Direct .gsz file manipulation (recommended approach)
- **Excel Headless Processing**: Background Excel calculations with robust connection management
- **Advanced Visualizations**: Detailed slope geometry plots with failure surfaces and pipeline locations
- **Intelligent Fallbacks**: Realistic simulations when software unavailable with graceful error handling
- **Scalable Analysis**: From 10 to 1000+ configurations
- **Enhanced Reliability**: Automatic fallbacks prevent workflow failures

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

## Troubleshooting & Common Issues

### **System automatically handles common issues:**

**❌ "xlwings not available" errors:**
- ✅ **Auto-fixed**: System installs xlwings automatically via setup_environment.py
- ✅ **Fallback**: Uses mock results if Excel integration fails

**❌ "Excel OLE connection errors":**
- ✅ **Auto-fixed**: Enhanced connection management with proper cleanup
- ✅ **Fallback**: Provides engineering-based mock calculations when Excel unavailable

**❌ "PyGeoStudio not found":**
- ✅ **Auto-fallback**: Uses GeoStudio CLI or intelligent simulation
- ✅ **Recommendation**: Install PyGeoStudio for best results: `pip install PyGeoStudio`

**❌ "GeoStudio executable not found":**
- ✅ **Auto-fallback**: Uses mock interface with realistic engineering calculations
- ✅ **Note**: Results still meaningful for preliminary analysis

### **Expected behavior:**
- System will complete analysis even if software dependencies are missing
- Mock results are based on engineering principles and provide meaningful insights
- Check console output for capability detection and fallback notifications

## Support & Documentation

- See `CLAUDE.md` for detailed technical documentation
- Check `executive_summary.txt` in results for analysis-specific findings
- Review individual CSV files for detailed configuration data
- Examine `analysis_summary_plots.png` for visual insights
- Run `python setup_environment.py` to check system capabilities

## License

MIT License - See LICENSE file for details.