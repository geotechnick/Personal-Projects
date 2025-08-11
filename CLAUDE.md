# CLAUDE.md - Personal Projects

## Project Overview
This repository contains geotechnical engineering tools and analysis resources, primarily focused on the EMPCO (Energy Management and Pipeline Consulting Operations) project. The project includes tools for soil spring analysis, bank stability assessment, and slope stability evaluation.

## Project Structure
```
/workspaces/Personal-Projects/
├── EMPCO/                                    # Main engineering project directory
│   ├── *.pdf                                # Technical manuals and procedures
│   ├── *.docx                               # Documentation and reports
│   ├── *.xlsx                               # Engineering calculation spreadsheets
│   ├── read_soil_springs.py                 # Python utility for Excel formula extraction
│   ├── slope_stability_automation.py        # Automated slope stability analysis
│   ├── soil_springs_integration.py          # Integration with soil springs analysis
│   ├── automated_decision_workflow.py       # Complete automated workflow
│   ├── Slope Template/                      # GeoStudio slope analysis templates
│   │   ├── SlopeTemplate.gsz                # GeoStudio project file
│   │   └── uncompressed/                    # Uncompressed XML data
│   │       └── SlopeTemplate.xml            # XML template for automation
│   └── *.txt                                # Analysis outputs and explanations
├── README.md                                # Project description
└── LICENSE                                  # MIT License

```

## Key Components

### 1. Soil Springs Analysis (`EMPCO/`)
- **Primary Tool**: `Soil Springs_2024.xlsx`
- **Purpose**: Calculate soil spring properties for pipeline analysis under Permanent Ground Deformation (PGD)
- **Sheets**:
  - `Input&Summary`: User input parameters and results summary
  - `Calcs`: Detailed engineering calculations
- **Key Parameters**:
  - Pipe properties (OD, wall thickness, SMYS, DOC)
  - Soil properties (friction angle, cohesion, unit weight)
  - PGD characteristics (parallel/perpendicular to pipe)

### 2. Automated Analysis System
- **Primary Files**: 
  - `slope_stability_automation.py`: Automated slope stability analysis engine
  - `soil_springs_integration.py`: Integration with soil springs calculations
  - `automated_decision_workflow.py`: Complete automated workflow orchestrator
- **Purpose**: Generate decision matrices for slope configurations requiring detailed analysis
- **Key Features**:
  - Parametric slope stability analysis (varies angle, height, soil properties)
  - Integration with existing soil springs Excel calculations
  - Automated decision matrix generation
  - Priority-based recommendations
  - Executive summary and visualization reports

### 3. Python Utilities
- **File**: `read_soil_springs.py`
- **Purpose**: Extract Excel formulas and values programmatically
- **Dependencies**: `xlwings` library
- **Usage**: Automated extraction of calculation formulas for documentation

### 4. GeoStudio Analysis Templates
- **File**: `Slope Template/SlopeTemplate.gsz`
- **Software**: GeoStudio SLOPE/W
- **Analysis Types**: 
  - Total Stress analysis (Spencer method)
  - Effective Stress analysis
- **Purpose**: Bank stability and slope stability assessments
- **XML Template**: `SlopeTemplate.xml` for automated parameter modification

### 5. Technical Documentation
- Bank Stability Assessment Manual (Draft WCP)
- VIV Evaluation Procedure
- Geohazards Manual and Appendices
- ASCE Pipeline Standards

## Engineering Context

### Soil Springs Calculations
The Excel tool calculates:
- Longitudinal/Transverse forces on pipelines
- Axial/Bending stresses
- Allowable pipe lengths in PGD zones
- Factor of Safety assessments

### Automated Analysis Workflow
The new automated system provides a comprehensive workflow:

1. **Slope Configuration Generation**: Parametric generation of slope configurations varying:
   - Slope angles (15° to 45°)
   - Slope heights (20 to 100 feet)
   - Soil strength scenarios (weak, medium, strong)
   - Groundwater conditions

2. **Slope Stability Analysis**: Automated GeoStudio SLOPE/W analysis for each configuration:
   - Total stress analysis (Spencer method)
   - Effective stress analysis
   - Factor of Safety calculation
   - Critical slip surface identification

3. **Decision Matrix Creation**: Determine which configurations require detailed analysis:
   - FoS < 1.5: Requires detailed analysis
   - FoS 1.5-2.0: Conditional detailed analysis
   - FoS > 2.0: Standard monitoring

4. **Soil Springs Integration**: For configurations requiring detailed analysis:
   - Generate pipeline configuration matrix
   - Run automated soil springs calculations
   - Calculate pipeline stresses and allowable lengths
   - Identify configurations exceeding allowable limits

5. **Results and Recommendations**: Generate comprehensive outputs:
   - Priority-based decision matrix
   - Executive summary report
   - Visualization plots and heatmaps
   - Specific recommendations with timelines and cost estimates

### Traditional Manual Workflow
1. Input pipe specifications (diameter, wall thickness, material grade)
2. Define soil properties (φ, c, γ')
3. Specify PGD characteristics
4. Review calculated forces and stresses
5. Verify against allowable limits

## Development Guidelines

### Python Development
- Use `xlwings` for Excel integration
- Follow PEP 8 style guidelines
- Include proper error handling for file operations
- Document engineering formulas and assumptions

### Excel Tool Modifications
- Maintain formula integrity when updating calculations
- Use consistent units throughout (inches for pipe, psf for soil)
- Include validation checks for input ranges
- Update summary outputs automatically

### File Management
- Keep original PDF manuals for reference
- Version control Excel files when formulas change
- Export calculation results to text for documentation
- Backup GeoStudio template files before modifications

## Common Commands

### Python Environment Setup
```bash
pip install xlwings pandas openpyxl matplotlib seaborn numpy
```

### Automated Analysis Execution
```bash
# Run complete automated analysis workflow (limited configurations for demo)
python automated_decision_workflow.py --limit 10

# Run with custom paths and output directory
python automated_decision_workflow.py --template "Slope Template/uncompressed/SlopeTemplate.xml" --excel "Soil Springs_2024.xlsx" --output "my_results"

# Run without generating plots
python automated_decision_workflow.py --no-plots
```

### Individual Module Usage
```bash
# Run slope stability analysis only
python slope_stability_automation.py

# Extract Excel formulas for documentation
python read_soil_springs.py

# Test soil springs integration
python soil_springs_integration.py
```

### Analysis Outputs
After running the automated workflow, check the output directory for:
- `slope_stability_decision_matrix.csv`: Initial slope analysis results
- `comprehensive_decision_matrix.csv`: Integrated results with pipeline analysis
- `executive_summary.txt`: Executive summary report
- `analysis_summary_plots.png`: Visualization plots
- `configuration_recommendations.csv`: Specific recommendations with timelines

### Manual Testing and Validation
- Open `Soil Springs_2024.xlsx`
- Verify input ranges on `Input&Summary` sheet
- Check calculation results on `Calcs` sheet
- Cross-reference automated results with manual calculations

## Engineering Standards Referenced
- ASCE Guidelines for Pipeline Design
- API 5L Pipeline Specifications
- Geotechnical Engineering Standards
- Bank Stability Assessment Procedures

## Automation Architecture

### Key Classes and Functions
- `SlopeStabilityAnalyzer`: Main class for automating GeoStudio slope analysis
- `GeoStudioXMLHandler`: Handles XML template manipulation for parameter updates
- `SoilSpringsAnalyzer`: Automates Excel-based soil springs calculations
- `IntegratedAnalysisEngine`: Combines slope stability and pipeline analysis
- `AutomatedDecisionWorkflow`: Complete workflow orchestrator with reporting

### Integration Points
1. **XML Template Modification**: Updates GeoStudio template with slope geometry and material properties
2. **Excel Automation**: Uses `xlwings` to update soil springs calculations programmatically  
3. **Results Processing**: Combines Factor of Safety results with pipeline stress analysis
4. **Decision Logic**: Implements engineering thresholds for determining analysis requirements

### Current Limitations
- GeoStudio execution is currently mocked (placeholder function)
- Real implementation requires GeoStudio command-line interface
- Limited to simplified slope geometries in current version
- Excel file must be available and formatted as expected

### Future Enhancements
- Direct GeoStudio API integration
- More complex slope geometry handling
- Database integration for configuration storage
- Web-based dashboard for results visualization
- Machine learning for improved decision thresholds

## Notes for AI Assistant
- This is a geotechnical engineering project focused on pipeline analysis
- The project now includes comprehensive automation for slope stability analysis
- Excel files contain complex engineering formulas - handle with care
- GeoStudio files require specialized software for viewing/editing
- The automated system generates decision matrices to prioritize which slopes need detailed analysis
- All calculations should follow established engineering standards
- Maintain accuracy when working with technical specifications
- The automation system is designed to scale from small studies to large parametric analyses