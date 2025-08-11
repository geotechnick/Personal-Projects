#!/usr/bin/env python3
"""
Parameter Input System
Provides multiple ways for users to specify slope, soil, and pipeline parameters.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import pandas as pd
from dataclasses import dataclass, asdict
import argparse

from slope_stability_automation import SlopeGeometry, SoilLayer, SlopeConfiguration
from soil_springs_integration import PipelineConfiguration


@dataclass
class ProjectParameters:
    """Complete project parameters for analysis"""
    project_name: str
    description: str
    slope_angles: List[float]  # degrees
    slope_heights: List[float]  # feet
    soil_scenarios: List[Dict[str, Any]]  # List of soil layer definitions
    pipeline_sizes: List[Tuple[float, float]]  # (OD, wall_thickness)
    pipeline_grades: List[str]  # Material grades
    depths_of_cover: List[float]  # feet
    internal_pressures: List[float]  # psi
    pgd_lengths: List[float]  # feet
    groundwater_ratios: List[float]  # ratio of slope height


class ParameterInputManager:
    """Manages multiple parameter input methods"""
    
    def __init__(self):
        self.default_parameters = self._create_default_parameters()
    
    def _create_default_parameters(self) -> ProjectParameters:
        """Create default parameter set"""
        return ProjectParameters(
            project_name="EMPCO Default Analysis",
            description="Standard parametric slope stability analysis",
            slope_angles=[15, 20, 25, 30, 35, 40, 45],
            slope_heights=[20, 30, 40, 50, 60, 80, 100],
            soil_scenarios=[
                {
                    "name": "Weak Soil Scenario",
                    "layers": [
                        {"name": "Weak Clay", "unit_weight": 115, "cohesion_total": 100, 
                         "cohesion_effective": 50, "friction_angle": 15, "thickness": 20},
                        {"name": "Medium Soil", "unit_weight": 120, "cohesion_total": 200, 
                         "cohesion_effective": 100, "friction_angle": 25, "thickness": 30}
                    ]
                },
                {
                    "name": "Medium Soil Scenario", 
                    "layers": [
                        {"name": "Medium Clay", "unit_weight": 120, "cohesion_total": 200,
                         "cohesion_effective": 100, "friction_angle": 25, "thickness": 20},
                        {"name": "Dense Soil", "unit_weight": 125, "cohesion_total": 400,
                         "cohesion_effective": 200, "friction_angle": 35, "thickness": 30}
                    ]
                },
                {
                    "name": "Strong Soil Scenario",
                    "layers": [
                        {"name": "Dense Clay", "unit_weight": 125, "cohesion_total": 400,
                         "cohesion_effective": 200, "friction_angle": 35, "thickness": 20},
                        {"name": "Rock", "unit_weight": 130, "cohesion_total": 1000,
                         "cohesion_effective": 500, "friction_angle": 40, "thickness": 30}
                    ]
                }
            ],
            pipeline_sizes=[(16, 0.375), (20, 0.5), (24, 0.5), (30, 0.625), (36, 0.75)],
            pipeline_grades=["X-52", "X-60", "X-65", "X-70"],
            depths_of_cover=[4, 6, 8, 10, 12, 15],
            internal_pressures=[1000, 1200, 1440, 1600],
            pgd_lengths=[5, 10, 15, 20, 30, 50],
            groundwater_ratios=[0.5, 0.7, 0.9]  # GW depth as ratio of slope height
        )
    
    # Method 1: JSON Configuration File
    def save_parameters_to_json(self, parameters: ProjectParameters, file_path: str):
        """Save parameters to JSON configuration file"""
        with open(file_path, 'w') as f:
            json.dump(asdict(parameters), f, indent=2)
        print(f"Parameters saved to {file_path}")
    
    def load_parameters_from_json(self, file_path: str) -> ProjectParameters:
        """Load parameters from JSON file"""
        if not Path(file_path).exists():
            print(f"File not found: {file_path}, using defaults")
            return self.default_parameters
            
        with open(file_path, 'r') as f:
            data = json.load(f)
        return ProjectParameters(**data)
    
    # Method 2: YAML Configuration File  
    def save_parameters_to_yaml(self, parameters: ProjectParameters, file_path: str):
        """Save parameters to YAML configuration file"""
        try:
            with open(file_path, 'w') as f:
                yaml.dump(asdict(parameters), f, default_flow_style=False, indent=2)
            print(f"Parameters saved to {file_path}")
        except ImportError:
            print("PyYAML not installed. Install with: pip install PyYAML")
    
    def load_parameters_from_yaml(self, file_path: str) -> ProjectParameters:
        """Load parameters from YAML file"""
        try:
            if not Path(file_path).exists():
                print(f"File not found: {file_path}, using defaults")
                return self.default_parameters
                
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            return ProjectParameters(**data)
        except ImportError:
            print("PyYAML not installed. Install with: pip install PyYAML")
            return self.default_parameters
    
    # Method 3: Excel Parameter File
    def save_parameters_to_excel(self, parameters: ProjectParameters, file_path: str):
        """Save parameters to Excel file with multiple sheets"""
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            
            # Project info
            project_df = pd.DataFrame({
                'Parameter': ['Project Name', 'Description'],
                'Value': [parameters.project_name, parameters.description]
            })
            project_df.to_excel(writer, sheet_name='Project_Info', index=False)
            
            # Slope parameters
            slope_df = pd.DataFrame({
                'Slope_Angles_deg': parameters.slope_angles,
                'Slope_Heights_ft': parameters.slope_heights + [None] * (len(parameters.slope_angles) - len(parameters.slope_heights))
            })
            slope_df.to_excel(writer, sheet_name='Slope_Parameters', index=False)
            
            # Soil scenarios
            soil_data = []
            for i, scenario in enumerate(parameters.soil_scenarios):
                for j, layer in enumerate(scenario['layers']):
                    soil_data.append({
                        'Scenario': scenario['name'],
                        'Layer_Name': layer['name'],
                        'Unit_Weight_pcf': layer['unit_weight'],
                        'Cohesion_Total_psf': layer['cohesion_total'],
                        'Cohesion_Effective_psf': layer['cohesion_effective'],
                        'Friction_Angle_deg': layer['friction_angle'],
                        'Thickness_ft': layer['thickness']
                    })
            
            soil_df = pd.DataFrame(soil_data)
            soil_df.to_excel(writer, sheet_name='Soil_Parameters', index=False)
            
            # Pipeline parameters
            pipeline_data = []
            for size in parameters.pipeline_sizes:
                pipeline_data.append({
                    'Outside_Diameter_in': size[0],
                    'Wall_Thickness_in': size[1]
                })
            
            pipeline_df = pd.DataFrame(pipeline_data)
            pipeline_df['Grades'] = parameters.pipeline_grades + [None] * (len(pipeline_df) - len(parameters.pipeline_grades))
            pipeline_df.to_excel(writer, sheet_name='Pipeline_Sizes', index=False)
            
            # Other parameters
            other_df = pd.DataFrame({
                'Depths_of_Cover_ft': parameters.depths_of_cover,
                'Internal_Pressures_psi': parameters.internal_pressures + [None] * (len(parameters.depths_of_cover) - len(parameters.internal_pressures)),
                'PGD_Lengths_ft': parameters.pgd_lengths + [None] * (len(parameters.depths_of_cover) - len(parameters.pgd_lengths)),
                'Groundwater_Ratios': parameters.groundwater_ratios + [None] * (len(parameters.depths_of_cover) - len(parameters.groundwater_ratios))
            })
            other_df.to_excel(writer, sheet_name='Other_Parameters', index=False)
        
        print(f"Parameters saved to Excel file: {file_path}")
    
    def load_parameters_from_excel(self, file_path: str) -> ProjectParameters:
        """Load parameters from Excel file"""
        if not Path(file_path).exists():
            print(f"File not found: {file_path}, using defaults")
            return self.default_parameters
        
        try:
            # Read each sheet
            project_df = pd.read_excel(file_path, sheet_name='Project_Info')
            slope_df = pd.read_excel(file_path, sheet_name='Slope_Parameters')
            soil_df = pd.read_excel(file_path, sheet_name='Soil_Parameters')
            pipeline_df = pd.read_excel(file_path, sheet_name='Pipeline_Sizes')
            other_df = pd.read_excel(file_path, sheet_name='Other_Parameters')
            
            # Extract project info
            project_info = dict(zip(project_df['Parameter'], project_df['Value']))
            
            # Extract slope parameters
            slope_angles = slope_df['Slope_Angles_deg'].dropna().tolist()
            slope_heights = slope_df['Slope_Heights_ft'].dropna().tolist()
            
            # Extract soil scenarios
            soil_scenarios = []
            for scenario_name in soil_df['Scenario'].unique():
                scenario_data = soil_df[soil_df['Scenario'] == scenario_name]
                layers = []
                for _, row in scenario_data.iterrows():
                    layers.append({
                        'name': row['Layer_Name'],
                        'unit_weight': row['Unit_Weight_pcf'],
                        'cohesion_total': row['Cohesion_Total_psf'],
                        'cohesion_effective': row['Cohesion_Effective_psf'],
                        'friction_angle': row['Friction_Angle_deg'],
                        'thickness': row['Thickness_ft']
                    })
                soil_scenarios.append({
                    'name': scenario_name,
                    'layers': layers
                })
            
            # Extract pipeline parameters
            pipeline_sizes = list(zip(pipeline_df['Outside_Diameter_in'], pipeline_df['Wall_Thickness_in']))
            pipeline_grades = pipeline_df['Grades'].dropna().tolist()
            
            # Extract other parameters
            depths_of_cover = other_df['Depths_of_Cover_ft'].dropna().tolist()
            internal_pressures = other_df['Internal_Pressures_psi'].dropna().tolist()
            pgd_lengths = other_df['PGD_Lengths_ft'].dropna().tolist()
            groundwater_ratios = other_df['Groundwater_Ratios'].dropna().tolist()
            
            return ProjectParameters(
                project_name=project_info.get('Project Name', 'Loaded from Excel'),
                description=project_info.get('Description', 'Parameters loaded from Excel file'),
                slope_angles=slope_angles,
                slope_heights=slope_heights,
                soil_scenarios=soil_scenarios,
                pipeline_sizes=pipeline_sizes,
                pipeline_grades=pipeline_grades,
                depths_of_cover=depths_of_cover,
                internal_pressures=internal_pressures,
                pgd_lengths=pgd_lengths,
                groundwater_ratios=groundwater_ratios
            )
            
        except Exception as e:
            print(f"Error loading Excel file: {e}, using defaults")
            return self.default_parameters
    
    # Method 4: Interactive Command Line Input
    def get_parameters_interactive(self) -> ProjectParameters:
        """Interactive command-line parameter input"""
        
        print("=== Interactive Parameter Input ===")
        print("Press Enter to use default values shown in [brackets]")
        
        # Project info
        project_name = input(f"Project name [{self.default_parameters.project_name}]: ").strip()
        if not project_name:
            project_name = self.default_parameters.project_name
        
        description = input(f"Description [{self.default_parameters.description}]: ").strip()
        if not description:
            description = self.default_parameters.description
        
        # Slope parameters
        print("\n--- Slope Parameters ---")
        slope_angles_input = input(f"Slope angles (degrees, comma-separated) [{','.join(map(str, self.default_parameters.slope_angles))}]: ").strip()
        if slope_angles_input:
            slope_angles = [float(x.strip()) for x in slope_angles_input.split(',')]
        else:
            slope_angles = self.default_parameters.slope_angles
        
        slope_heights_input = input(f"Slope heights (feet, comma-separated) [{','.join(map(str, self.default_parameters.slope_heights))}]: ").strip()
        if slope_heights_input:
            slope_heights = [float(x.strip()) for x in slope_heights_input.split(',')]
        else:
            slope_heights = self.default_parameters.slope_heights
        
        # Use default soil scenarios for interactive mode (too complex for command line)
        print("\n--- Using default soil scenarios ---")
        for scenario in self.default_parameters.soil_scenarios:
            print(f"  {scenario['name']}: {len(scenario['layers'])} layers")
        
        # Pipeline parameters
        print("\n--- Pipeline Parameters ---")
        use_default_pipes = input("Use default pipeline configurations? [Y/n]: ").strip().lower()
        if use_default_pipes in ['n', 'no']:
            print("Pipeline configuration requires Excel or JSON input for detailed specification")
            print("Using default pipeline parameters")
        
        return ProjectParameters(
            project_name=project_name,
            description=description,
            slope_angles=slope_angles,
            slope_heights=slope_heights,
            soil_scenarios=self.default_parameters.soil_scenarios,
            pipeline_sizes=self.default_parameters.pipeline_sizes,
            pipeline_grades=self.default_parameters.pipeline_grades,
            depths_of_cover=self.default_parameters.depths_of_cover,
            internal_pressures=self.default_parameters.internal_pressures,
            pgd_lengths=self.default_parameters.pgd_lengths,
            groundwater_ratios=self.default_parameters.groundwater_ratios
        )
    
    # Method 5: Command Line Arguments
    def get_parameters_from_args(self, args: argparse.Namespace) -> ProjectParameters:
        """Get parameters from command line arguments"""
        
        params = self.default_parameters
        
        if hasattr(args, 'angles') and args.angles:
            params.slope_angles = [float(x) for x in args.angles.split(',')]
        
        if hasattr(args, 'heights') and args.heights:
            params.slope_heights = [float(x) for x in args.heights.split(',')]
        
        if hasattr(args, 'project_name') and args.project_name:
            params.project_name = args.project_name
            
        return params
    
    # Configuration Generation
    def generate_slope_configurations(self, parameters: ProjectParameters) -> List[SlopeConfiguration]:
        """Generate slope configurations from parameters"""
        configurations = []
        config_id = 0
        
        for angle in parameters.slope_angles:
            for height in parameters.slope_heights:
                for gw_ratio in parameters.groundwater_ratios:
                    for soil_scenario in parameters.soil_scenarios:
                        
                        # Create geometry
                        geometry = SlopeGeometry(
                            slope_angle=angle,
                            slope_height=height,
                            bench_width=0,  # Simple slope
                            toe_distance=50
                        )
                        
                        # Create soil layers
                        soil_layers = []
                        for layer_data in soil_scenario['layers']:
                            layer = SoilLayer(
                                name=layer_data['name'],
                                unit_weight=layer_data['unit_weight'],
                                cohesion_total=layer_data['cohesion_total'],
                                cohesion_effective=layer_data['cohesion_effective'],
                                friction_angle=layer_data['friction_angle'],
                                thickness=layer_data['thickness']
                            )
                            soil_layers.append(layer)
                        
                        # Create configuration
                        config = SlopeConfiguration(
                            config_id=f"Config_{config_id:04d}",
                            geometry=geometry,
                            soil_layers=soil_layers,
                            groundwater_depth=height * gw_ratio
                        )
                        
                        configurations.append(config)
                        config_id += 1
        
        return configurations
    
    def generate_pipeline_configurations(self, parameters: ProjectParameters) -> List[PipelineConfiguration]:
        """Generate pipeline configurations from parameters"""
        configurations = []
        
        for (od, wt) in parameters.pipeline_sizes[:3]:  # Limit for demo
            for grade in parameters.pipeline_grades[:2]:  # Limit for demo
                for doc in parameters.depths_of_cover[:3]:  # Limit for demo
                    for pressure in parameters.internal_pressures[:2]:  # Limit for demo
                        for length in parameters.pgd_lengths[:3]:  # Limit for demo
                            for direction in ["Parallel", "Perpendicular"]:
                                
                                config = PipelineConfiguration(
                                    pipe_od=od,
                                    pipe_wt=wt,
                                    pipe_smys=grade,
                                    pipe_doc=doc,
                                    pipe_length_in_pgd=length,
                                    internal_pressure=pressure,
                                    pgd_direction=direction
                                )
                                
                                configurations.append(config)
        
        return configurations


def create_default_config_files():
    """Create default configuration files for user reference"""
    
    manager = ParameterInputManager()
    default_params = manager.default_parameters
    
    # Create JSON template
    manager.save_parameters_to_json(default_params, "project_parameters_template.json")
    
    # Create YAML template
    manager.save_parameters_to_yaml(default_params, "project_parameters_template.yaml")
    
    # Create Excel template
    manager.save_parameters_to_excel(default_params, "project_parameters_template.xlsx")
    
    print("Default configuration templates created:")
    print("  - project_parameters_template.json")
    print("  - project_parameters_template.yaml") 
    print("  - project_parameters_template.xlsx")


def demonstrate_parameter_input():
    """Demonstrate different parameter input methods"""
    
    print("=== Parameter Input Methods Demonstration ===")
    
    manager = ParameterInputManager()
    
    # Method 1: Default parameters
    print("\n1. Default Parameters:")
    default_params = manager.default_parameters
    print(f"   Project: {default_params.project_name}")
    print(f"   Slope angles: {default_params.slope_angles}")
    print(f"   Pipeline sizes: {default_params.pipeline_sizes}")
    
    # Method 2: Save/load JSON
    print("\n2. JSON Configuration:")
    json_file = "demo_parameters.json"
    manager.save_parameters_to_json(default_params, json_file)
    loaded_params = manager.load_parameters_from_json(json_file)
    print(f"   Loaded from JSON: {loaded_params.project_name}")
    
    # Method 3: Excel template
    print("\n3. Excel Configuration:")
    excel_file = "demo_parameters.xlsx"
    manager.save_parameters_to_excel(default_params, excel_file)
    print(f"   Excel template created: {excel_file}")
    
    # Method 4: Generate configurations
    print("\n4. Configuration Generation:")
    # Use subset for demo
    demo_params = ProjectParameters(
        project_name="Demo Analysis",
        description="Small demo",
        slope_angles=[30, 35],
        slope_heights=[40, 60],
        soil_scenarios=default_params.soil_scenarios[:1],  # Just one scenario
        pipeline_sizes=default_params.pipeline_sizes[:2],
        pipeline_grades=default_params.pipeline_grades[:1],
        depths_of_cover=default_params.depths_of_cover[:2],
        internal_pressures=default_params.internal_pressures[:1],
        pgd_lengths=default_params.pgd_lengths[:2],
        groundwater_ratios=[0.7]
    )
    
    slope_configs = manager.generate_slope_configurations(demo_params)
    pipeline_configs = manager.generate_pipeline_configurations(demo_params)
    
    print(f"   Generated {len(slope_configs)} slope configurations")
    print(f"   Generated {len(pipeline_configs)} pipeline configurations")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parameter Input System")
    parser.add_argument("--create-templates", action="store_true", help="Create default configuration templates")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    parser.add_argument("--interactive", action="store_true", help="Interactive parameter input")
    
    args = parser.parse_args()
    
    if args.create_templates:
        create_default_config_files()
    elif args.demo:
        demonstrate_parameter_input()
    elif args.interactive:
        manager = ParameterInputManager()
        params = manager.get_parameters_interactive()
        print(f"\nParameters configured for: {params.project_name}")
    else:
        print("Use --help for available options")
        print("Quick start: python parameter_input_system.py --create-templates")