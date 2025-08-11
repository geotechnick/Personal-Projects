# Parameter Input Guide

## How Users Specify Slope, Soil, and Pipeline Parameters

The EMPCO system provides **5 flexible methods** for users to specify their analysis parameters, from simple command-line overrides to detailed Excel configuration files.

## 🚀 Quick Start - Parameter Input Methods

### Method 1: Create Template Files (Recommended First Step)
```bash
# Create template configuration files
python automated_decision_workflow.py --create-templates
```
This creates:
- `project_parameters_template.json`
- `project_parameters_template.yaml`
- `project_parameters_template.xlsx`

### Method 2: Use Configuration Files

**JSON Configuration:**
```bash
python automated_decision_workflow.py --config-json "my_project.json"
```

**YAML Configuration:**
```bash
python automated_decision_workflow.py --config-yaml "my_project.yaml"
```

**Excel Configuration:**
```bash
python automated_decision_workflow.py --config-excel "my_project.xlsx"
```

### Method 3: Interactive Input
```bash
python automated_decision_workflow.py --interactive
```
Prompts for all parameters with defaults shown in brackets.

### Method 4: Command Line Overrides
```bash
# Quick parameter changes
python automated_decision_workflow.py --angles "25,30,35" --heights "40,60,80" --project-name "My Analysis"
```

### Method 5: Default Parameters
```bash
# Use built-in defaults (good for testing)
python automated_decision_workflow.py --limit 10
```

## 📊 Parameter Categories

### 🏔️ **Slope Parameters**
- **Slope Angles**: List of slope angles in degrees (e.g., [25, 30, 35, 40])
- **Slope Heights**: List of slope heights in feet (e.g., [30, 50, 75, 100])
- **Groundwater Ratios**: Groundwater depth as ratio of slope height (e.g., [0.6, 0.8])

### 🌍 **Soil Parameters**
Each soil scenario contains multiple layers with:
- **Layer Name**: Descriptive name (e.g., "Soft Clay", "Dense Sand")
- **Unit Weight**: Soil unit weight in pcf (e.g., 115)
- **Cohesion Total**: Total stress cohesion in psf (e.g., 150)
- **Cohesion Effective**: Effective stress cohesion in psf (e.g., 75)
- **Friction Angle**: Effective friction angle in degrees (e.g., 18)
- **Thickness**: Layer thickness in feet (e.g., 15)

### 🔧 **Pipeline Parameters**
- **Pipeline Sizes**: List of [Outside Diameter, Wall Thickness] in inches
- **Pipeline Grades**: Material grades (e.g., ["X-60", "X-65", "X-70"])
- **Depths of Cover**: Burial depths in feet (e.g., [6, 8, 10, 12])
- **Internal Pressures**: Operating pressures in psi (e.g., [1200, 1440])
- **PGD Lengths**: Permanent ground deformation lengths in feet (e.g., [10, 20, 30])

## 📋 Configuration File Examples

### Simple JSON Example:
```json
{
  "project_name": "Site Alpha Analysis",
  "slope_angles": [30, 35, 40],
  "slope_heights": [40, 60, 80],
  "soil_scenarios": [
    {
      "name": "Conservative Soil",
      "layers": [
        {
          "name": "Weak Clay",
          "unit_weight": 115,
          "cohesion_total": 100,
          "cohesion_effective": 50,
          "friction_angle": 15,
          "thickness": 20
        }
      ]
    }
  ],
  "pipeline_sizes": [[20, 0.5], [24, 0.5]]
}
```

### YAML Example:
```yaml
project_name: "Quick Assessment"
slope_angles: [30, 35, 40]
slope_heights: [40, 60, 80]
pipeline_sizes:
  - [20, 0.5]    # 20" OD, 0.5" wall
  - [24, 0.5]    # 24" OD, 0.5" wall
```

## 📊 Excel Configuration Format

The Excel template contains multiple sheets:

**Sheet: Project_Info**
| Parameter | Value |
|-----------|-------|
| Project Name | Site Alpha Analysis |
| Description | Comprehensive slope analysis |

**Sheet: Slope_Parameters**
| Slope_Angles_deg | Slope_Heights_ft |
|------------------|------------------|
| 25 | 30 |
| 30 | 50 |
| 35 | 75 |

**Sheet: Soil_Parameters**
| Scenario | Layer_Name | Unit_Weight_pcf | Cohesion_Total_psf | Cohesion_Effective_psf | Friction_Angle_deg | Thickness_ft |
|----------|------------|-----------------|-------------------|----------------------|-------------------|--------------|
| River Valley | Soft Clay | 110 | 150 | 75 | 18 | 15 |
| River Valley | Dense Sand | 125 | 0 | 0 | 32 | 25 |

## 🎯 Typical Usage Workflows

### Engineering Consultant Workflow:
1. **Initial Setup**: `python automated_decision_workflow.py --create-templates`
2. **Project Configuration**: Edit `project_parameters_template.xlsx` with project-specific values
3. **Run Analysis**: `python automated_decision_workflow.py --config-excel "my_project.xlsx"`
4. **Review Results**: Check `analysis_results/` directory

### Quick Assessment Workflow:
1. **Command Line**: `python automated_decision_workflow.py --angles "25,30,35" --heights "40,60" --limit 20`
2. **Review Results**: Check executive summary

### Research/Parametric Study Workflow:
1. **Create JSON Config**: Define extensive parameter ranges in JSON file
2. **Large Analysis**: `python automated_decision_workflow.py --config-json "parametric_study.json" --limit 500`
3. **Analyze Trends**: Use comprehensive CSV outputs for further analysis

## 🔧 Parameter Validation

The system automatically validates:
- ✅ **Slope angles**: 0-90 degrees (practical range 10-60°)
- ✅ **Soil properties**: Realistic engineering values
- ✅ **Pipeline specs**: Standard industry sizes and grades
- ✅ **Unit consistency**: All parameters in consistent units

## 💡 Tips for Parameter Selection

### **Slope Angles**:
- **Gentle slopes**: 15-25° (stable, minimal analysis needed)
- **Moderate slopes**: 25-35° (typical analysis range)
- **Steep slopes**: 35-45° (critical, detailed analysis required)

### **Soil Strength**:
- **Weak soils**: φ=15-20°, c=50-150 psf (high risk)
- **Medium soils**: φ=25-30°, c=100-300 psf (moderate risk)
- **Strong soils**: φ=30-40°, c=200-500 psf (low risk)

### **Pipeline Considerations**:
- **Small diameter**: 16-20" (lower stress, less critical)
- **Large diameter**: 24-36" (higher stress, more critical)
- **High pressure**: >1200 psi (increased risk)

## 🚀 Advanced Usage

### Custom Soil Scenarios:
Create site-specific soil profiles based on geotechnical investigation:
```json
{
  "name": "Site Investigation Results",
  "layers": [
    {"name": "Fill", "unit_weight": 100, "friction_angle": 12, "thickness": 5},
    {"name": "Organic Clay", "unit_weight": 95, "friction_angle": 8, "thickness": 10},
    {"name": "Glacial Till", "unit_weight": 135, "friction_angle": 35, "thickness": 40}
  ]
}
```

### Groundwater Scenarios:
```json
"groundwater_ratios": [0.3, 0.5, 0.7, 0.9]
```
- 0.3 = High groundwater (30% of slope height)
- 0.9 = Low groundwater (90% of slope height)

## 📖 Example Files

Check the `examples/` directory for:
- `example_project_config.json`: Complete project example
- `simple_config.yaml`: Minimal configuration
- Template files created with `--create-templates`

## 🆘 Troubleshooting

**Common Issues:**
- **File not found**: Use absolute paths or ensure files are in correct directory
- **Invalid JSON**: Check JSON syntax with online validator
- **Missing parameters**: System will use defaults for missing values
- **Large configurations**: Use `--limit` parameter to test before full run

**Getting Help:**
```bash
python automated_decision_workflow.py --help
python parameter_input_system.py --help
```