# Parameter Input Examples

This directory contains example configuration files showing how to specify slope, soil, and pipeline parameters for analysis.

## Example Files:

### **`example_project_config.json`**
- **Purpose**: Complete project configuration with multiple soil scenarios
- **Use Case**: Engineering consulting projects with detailed site conditions
- **Parameters**: 4 slope angles, 4 heights, 3 soil scenarios, multiple pipeline configurations

**Run with:**
```bash
python automated_decision_workflow.py --config-json "examples/example_project_config.json" --limit 20
```

### **`simple_config.yaml`** 
- **Purpose**: Minimal configuration for quick assessments
- **Use Case**: Preliminary studies or proof-of-concept analysis
- **Parameters**: 3 slope angles, 3 heights, 2 soil scenarios, basic pipeline specs

**Run with:**
```bash  
python automated_decision_workflow.py --config-yaml "examples/simple_config.yaml"
```

## Quick Test Commands:

```bash
# Test with example JSON config
cd /workspaces/Personal-Projects/EMPCO
python automated_decision_workflow.py --config-json "examples/example_project_config.json" --limit 10

# Test with simple YAML config  
python automated_decision_workflow.py --config-yaml "examples/simple_config.yaml" --limit 5

# Create your own templates
python automated_decision_workflow.py --create-templates
```

## Parameter Ranges in Examples:

| Parameter | Example Config | Simple Config |
|-----------|----------------|---------------|
| Slope Angles | 25°, 30°, 35°, 40° | 30°, 35°, 40° |
| Slope Heights | 30, 50, 75, 100 ft | 40, 60, 80 ft |
| Soil Scenarios | 3 (River Valley, Upland, Rocky) | 2 (Conservative, Typical) |
| Pipeline Sizes | 20", 24", 30" | 20", 24" |

## Customizing Examples:

1. **Copy example file**: `cp examples/simple_config.yaml my_project.yaml`
2. **Edit parameters**: Modify angles, heights, soil properties as needed
3. **Run analysis**: `python automated_decision_workflow.py --config-yaml "my_project.yaml"`
4. **Review results**: Check `analysis_results/` directory