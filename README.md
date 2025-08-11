# Personal-Projects

## EMPCO Automated Slope Stability Analysis System

This repository contains an automated geotechnical engineering analysis system that determines which slope configurations require detailed pipeline soil springs analysis. The system integrates slope stability analysis with pipeline stress calculations to create comprehensive decision matrices for engineering assessment.

## Overview

The **EMPCO (Energy Management and Pipeline Consulting Operations)** project automates the traditionally manual process of:
1. Running slope stability analyses for various configurations
2. Determining which slopes require detailed soil springs analysis  
3. Calculating pipeline stresses for critical configurations
4. Generating decision matrices with engineering recommendations

## Key Features

- **Automated Parametric Analysis**: Tests hundreds of slope configurations varying angle (15-45°), height (20-100 ft), and soil properties
- **Decision Matrix Generation**: Automatically determines which configurations need detailed analysis based on Factor of Safety thresholds
- **Excel Integration**: Leverages existing `Soil Springs_2024.xlsx` calculations for pipeline analysis
- **Comprehensive Reporting**: Executive summaries, visualization plots, priority classifications with timelines and costs
- **Scalable Workflow**: From small studies (10 configs) to large parametric analyses (1000+ configs)

## Quick Start

### Prerequisites
```bash
pip install xlwings pandas matplotlib seaborn numpy openpyxl
```

**Enhanced GeoStudio Integration (Recommended):**
```bash
pip install PyGeoStudio
```

**Headless Operation Modes:**
1. **PyGeoStudio (Best)**: Direct .gsz file manipulation, no GeoStudio GUI needed
2. **GeoStudio CLI**: Command-line interface if GeoStudio installed
3. **Intelligent Simulation**: Realistic placeholders when GeoStudio unavailable
4. **Excel Background**: Hidden Excel processing with no visible windows

### Basic Usage
```bash
# Navigate to EMPCO directory
cd EMPCO

# Run automated analysis (demo with 10 configurations)
python automated_decision_workflow.py --limit 10

# View results in the analysis_results/ directory
```

### Full Parametric Study
```bash
# Run comprehensive analysis (hundreds of configurations)
python automated_decision_workflow.py --limit 200

# Custom output directory
python automated_decision_workflow.py --output "my_analysis_results"

# Skip plots generation for faster execution
python automated_decision_workflow.py --no-plots
```

## Understanding the Results

### Key Output Files:
- **`slope_stability_decision_matrix.csv`**: Initial slope analysis showing which configurations need detailed review
- **`comprehensive_decision_matrix.csv`**: Full analysis including pipeline stress calculations
- **`executive_summary.txt`**: Executive summary with key findings and recommendations
- **`analysis_summary_plots.png`**: Visualization plots showing Factor of Safety distributions and priorities
- **`configuration_recommendations.csv`**: Specific action items with timelines and cost estimates

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

### Analysis Workflow:
1. **Configuration Generation**: Creates parametric matrix of slope configurations
2. **Slope Stability Analysis**: Calculates Factor of Safety for each configuration
3. **Decision Logic**: Determines which configurations require detailed analysis (FoS < 1.5)
4. **Pipeline Integration**: For critical configurations, runs soil springs analysis with various pipeline sizes
5. **Results Generation**: Creates comprehensive decision matrices and engineering recommendations

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
├── automated_decision_workflow.py    # Main workflow orchestrator
├── slope_stability_automation.py     # Slope analysis engine
├── soil_springs_integration.py       # Excel integration
├── read_soil_springs.py             # Formula extraction utility
├── Soil Springs_2024.xlsx           # Pipeline analysis spreadsheet
├── Slope Template/                   # GeoStudio templates
│   └── uncompressed/SlopeTemplate.xml
├── analysis_results/                 # Output directory (created)
└── Technical Documentation/          # PDFs and manuals
```

## Limitations & Future Enhancements

### Current Capabilities & Limitations:

**✅ Fully Operational:**
- **PyGeoStudio Integration**: Direct .gsz file manipulation (recommended approach)
- **Excel Headless Processing**: Background Excel calculations with no GUI
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