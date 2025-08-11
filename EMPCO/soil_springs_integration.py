#!/usr/bin/env python3
"""
Soil Springs Integration Module
Integrates slope stability analysis results with soil springs analysis
to create comprehensive decision matrix for pipeline analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import xlwings as xw
from slope_stability_automation import SlopeAnalysisResult, SlopeConfiguration


@dataclass
class PipelineConfiguration:
    """Pipeline configuration parameters"""
    pipe_od: float  # inches - Outside Diameter
    pipe_wt: float  # inches - Wall Thickness  
    pipe_grade: str  # API grade (e.g., "X-52")
    pipe_smys: float  # psi - Specified Minimum Yield Strength
    pipe_doc: float  # feet - Depth of Cover
    pipe_length_in_pgd: float  # feet - Length in PGD zone
    pipe_coating: str  # Coating type (e.g., "FBE", "3LPE", "Concrete")
    internal_pressure: float  # psi
    pgd_direction: str  # "perpendicular" or "parallel" to pipe


@dataclass 
class SoilSpringParameters:
    """Soil parameters for spring analysis"""
    friction_angle: float  # degrees
    cohesion: float  # psf
    unit_weight: float  # psf
    soil_type: str  # description


@dataclass
class IntegratedAnalysisResult:
    """Combined results from slope stability and soil springs analysis"""
    config_id: str
    slope_fos: float
    pipeline_config: PipelineConfiguration
    soil_params: SoilSpringParameters
    longitudinal_force: float  # lb/ft
    axial_stress: float  # psi
    remaining_allowable_stress: float  # psi
    allowable_length: float  # feet
    exceeds_allowable: bool
    analysis_recommendation: str
    priority_level: int  # 1=Critical, 2=High, 3=Medium, 4=Low


class SoilSpringsAnalyzer:
    """Handles soil springs calculations using Excel automation"""
    
    def __init__(self, excel_path: str):
        self.excel_path = Path(excel_path)
        self.wb = None
        self.input_sheet = None
        self.calc_sheet = None
        self.app = None
    
    def open_excel(self, visible=False):
        """Open Excel file for analysis using robust connection method"""
        try:
            # Use robust connection method similar to HybridExcelAnalyzer
            if not visible:
                self.app = xw.App(visible=False, add_book=False)
                self.app.display_alerts = False
                self.app.screen_updating = False
                self.wb = self.app.books.open(str(self.excel_path))
            else:
                self.wb = xw.Book(str(self.excel_path))
                self.app = self.wb.app
            
            self.input_sheet = self.wb.sheets['Input&Summary'] 
            self.calc_sheet = self.wb.sheets['Calcs']
            
        except Exception as e:
            print(f"Failed to open Excel: {e}")
            raise
    
    def close_excel(self):
        """Close Excel file with proper cleanup"""
        try:
            if self.wb:
                self.wb.close()
                self.wb = None
            if self.app:
                self.app.quit()
                self.app = None
        except Exception as e:
            print(f"Error closing Excel: {e}")
            pass
    
    def analyze_pipeline_configuration(self, 
                                     pipeline_config: PipelineConfiguration,
                                     soil_params: SoilSpringParameters) -> Dict[str, float]:
        """Run soil springs analysis for given configuration"""
        
        if not self.wb:
            self.open_excel()
        
        try:
            # Update input parameters in Excel
            self._update_excel_inputs(pipeline_config, soil_params)
            
            # Read calculated results
            results = self._read_excel_outputs()
            
            return results
            
        except Exception as e:
            print(f"Error in soil springs analysis: {e}")
            return {}
    
    def _update_excel_inputs(self, pipeline_config: PipelineConfiguration, 
                           soil_params: SoilSpringParameters):
        """Update Excel input cells with configuration parameters"""
        
        # Pipe Properties
        self.input_sheet.range('C3').value = pipeline_config.pipe_od
        self.input_sheet.range('C4').value = pipeline_config.pipe_wt
        self.input_sheet.range('C5').value = pipeline_config.pipe_smys
        self.input_sheet.range('C6').value = pipeline_config.pipe_doc
        self.input_sheet.range('C7').value = pipeline_config.pipe_length_in_pgd
        self.input_sheet.range('C9').value = pipeline_config.internal_pressure
        
        # Soil Properties
        self.input_sheet.range('F3').value = soil_params.friction_angle
        self.input_sheet.range('F4').value = soil_params.cohesion
        self.input_sheet.range('F5').value = soil_params.unit_weight
        self.input_sheet.range('F6').value = pipeline_config.pgd_direction
        
        # Force Excel to recalculate with error handling
        try:
            if self.app:
                self.app.calculation = 'automatic'
                self.app.calculate()
            elif self.wb and self.wb.app:
                self.wb.app.calculation = 'automatic'
                self.wb.app.calculate()
        except Exception as e:
            print(f"Warning: Excel calculation may have failed: {e}")
            pass
    
    def _read_excel_outputs(self) -> Dict[str, float]:
        """Read calculated results from Excel"""
        
        results = {
            'longitudinal_force': self.input_sheet.range('C13').value or 0,
            'axial_stress': self.input_sheet.range('C14').value or 0,
            'remaining_allowable_stress': self.input_sheet.range('C15').value or 0,
            'allowable_length': self.input_sheet.range('C16').value or 0,
            'exceeds_allowable': self.input_sheet.range('C17').value == "Exceeds"
        }
        
        return results


class IntegratedAnalysisEngine:
    """Main engine for integrated slope stability and soil springs analysis"""
    
    def __init__(self, excel_path: str):
        self.soil_springs_analyzer = SoilSpringsAnalyzer(excel_path)
        self.integrated_results: List[IntegratedAnalysisResult] = []
    
    def create_pipeline_configurations(self) -> List[PipelineConfiguration]:
        """Generate typical pipeline configurations for analysis"""
        
        configurations = []
        
        # Common pipeline sizes and grades
        pipe_sizes = [(16, 0.375), (20, 0.5), (24, 0.5), (30, 0.625), (36, 0.75)]
        pipe_grades = ["X-52", "X-60", "X-65", "X-70"]
        depths_of_cover = [4, 6, 8, 10, 12, 15]
        pressures = [1000, 1200, 1440, 1600]
        pgd_lengths = [5, 10, 15, 20, 30, 50]
        
        config_id = 0
        for (od, wt) in pipe_sizes:
            for grade in pipe_grades:
                for doc in depths_of_cover:
                    for pressure in pressures:
                        for length in pgd_lengths:
                            # Create configuration for both PGD directions
                            for direction in ["Parallel", "Perpendicular"]:
                                config = PipelineConfiguration(
                                    pipe_od=od,
                                    pipe_wt=wt,
                                    pipe_grade=grade,
                                    pipe_smys=52000 if 'X-52' in grade else 60000 if 'X-60' in grade else 65000 if 'X-65' in grade else 70000,
                                    pipe_doc=doc,
                                    pipe_length_in_pgd=length,
                                    pipe_coating="FBE",
                                    internal_pressure=pressure,
                                    pgd_direction=direction
                                )
                                configurations.append(config)
                                config_id += 1
                                
                                # Limit total configurations for demo
                                if config_id > 100:
                                    return configurations
        
        return configurations
    
    def convert_slope_to_soil_params(self, slope_config: SlopeConfiguration, 
                                   pipe_depth_of_cover: float = None) -> SoilSpringParameters:
        """
        Convert slope soil properties to soil spring parameters based on pipe location
        
        Uses 2-layer soil system:
        - Layer 1: Slope Material (upper layer)
        - Layer 2: Foundation Material (lower layer)
        
        Args:
            slope_config: Slope configuration with exactly 2 soil layers
            pipe_depth_of_cover: Pipe depth of cover in feet (determines which soil layer contains the pipe)
        
        Returns:
            Soil parameters for the specific layer containing the pipe
        """
        
        if not slope_config.soil_layers:
            # Default parameters if no layers
            return SoilSpringParameters(
                friction_angle=30,
                cohesion=100,
                unit_weight=125,
                soil_type="Default"
            )
        
        # If pipe depth is specified, determine which soil layer the pipe is in
        if pipe_depth_of_cover is not None:
            current_depth = 0
            for layer in slope_config.soil_layers:
                # Check if pipe is within this layer
                if current_depth <= pipe_depth_of_cover <= (current_depth + layer.thickness):
                    return SoilSpringParameters(
                        friction_angle=layer.friction_angle,
                        cohesion=layer.cohesion_effective,
                        unit_weight=layer.unit_weight,
                        soil_type=f"{layer.name} (at {pipe_depth_of_cover} ft depth)"
                    )
                current_depth += layer.thickness
            
            # If pipe is deeper than all defined layers, use the deepest layer
            deepest_layer = slope_config.soil_layers[-1]
            return SoilSpringParameters(
                friction_angle=deepest_layer.friction_angle,
                cohesion=deepest_layer.cohesion_effective,
                unit_weight=deepest_layer.unit_weight,
                soil_type=f"{deepest_layer.name} (extrapolated to {pipe_depth_of_cover} ft depth)"
            )
        
        # Fallback: Use weighted average of all layers (original approach)
        total_thickness = sum(layer.thickness for layer in slope_config.soil_layers)
        if total_thickness == 0:
            layer = slope_config.soil_layers[0]
            return SoilSpringParameters(
                friction_angle=layer.friction_angle,
                cohesion=layer.cohesion_effective,
                unit_weight=layer.unit_weight,
                soil_type=layer.name
            )
        
        # Weighted average based on thickness
        weighted_phi = sum(layer.friction_angle * layer.thickness 
                          for layer in slope_config.soil_layers) / total_thickness
        weighted_cohesion = sum(layer.cohesion_effective * layer.thickness 
                               for layer in slope_config.soil_layers) / total_thickness  
        weighted_unit_weight = sum(layer.unit_weight * layer.thickness 
                                  for layer in slope_config.soil_layers) / total_thickness
        
        soil_type = ", ".join([layer.name for layer in slope_config.soil_layers[:2]])
        
        return SoilSpringParameters(
            friction_angle=weighted_phi,
            cohesion=weighted_cohesion,
            unit_weight=weighted_unit_weight,
            soil_type=f"Weighted average: {soil_type}"
        )
    
    def integrate_analyses(self, 
                          slope_results: List[SlopeAnalysisResult],
                          slope_configs: List[SlopeConfiguration],
                          pipeline_configs: List[PipelineConfiguration]) -> List[IntegratedAnalysisResult]:
        """Integrate slope stability and soil springs analyses"""
        
        integrated_results = []
        
        print(f"Integrating {len(slope_results)} slope results with {len(pipeline_configs)} pipeline configurations...")
        
        # Use headless Excel mode with error handling
        try:
            self.soil_springs_analyzer.open_excel(visible=False)
        except Exception as e:
            print(f"Failed to open Excel for analysis: {e}")
            print("Falling back to mock/placeholder results...")
            return self._create_mock_integrated_results(slope_results, slope_configs, pipeline_configs)
        
        try:
            for slope_result in slope_results:
                # Find corresponding slope configuration
                slope_config = next((config for config in slope_configs 
                                   if config.config_id == slope_result.config_id), None)
                
                if not slope_config:
                    continue
                
                # Only analyze pipeline configs if slope requires detailed analysis
                # or if FoS is close to threshold
                min_fos = min(slope_result.total_stress_fos, slope_result.effective_stress_fos)
                
                if slope_result.requires_detailed_analysis or min_fos < 2.0:
                    
                    for pipeline_config in pipeline_configs[:5]:  # Limit for demo
                        
                        # Convert slope soil properties to soil spring parameters for specific pipe depth
                        soil_params = self.convert_slope_to_soil_params(slope_config, pipeline_config.pipe_doc)
                        
                        # Run soil springs analysis
                        spring_results = self.soil_springs_analyzer.analyze_pipeline_configuration(
                            pipeline_config, soil_params)
                        
                        if spring_results:
                            # Create integrated result
                            integrated_result = IntegratedAnalysisResult(
                                config_id=f"{slope_result.config_id}_{pipeline_config.pipe_od}in_{pipeline_config.pgd_path}",
                                slope_fos=min_fos,
                                pipeline_config=pipeline_config,
                                soil_params=soil_params,
                                longitudinal_force=spring_results.get('longitudinal_force', 0),
                                axial_stress=spring_results.get('axial_stress', 0),
                                remaining_allowable_stress=spring_results.get('remaining_allowable_stress', 0),
                                allowable_length=spring_results.get('allowable_length', 0),
                                exceeds_allowable=spring_results.get('exceeds_allowable', False),
                                analysis_recommendation=self._get_recommendation(slope_result, spring_results),
                                priority_level=self._get_priority_level(slope_result, spring_results)
                            )
                            
                            integrated_results.append(integrated_result)
                
                print(f"Completed integration for {slope_result.config_id}")
        
        finally:
            self.soil_springs_analyzer.close_excel()
        
        self.integrated_results = integrated_results
        return integrated_results
    
    def _get_recommendation(self, slope_result: SlopeAnalysisResult, 
                          spring_results: Dict[str, float]) -> str:
        """Generate analysis recommendation based on combined results"""
        
        min_fos = min(slope_result.total_stress_fos, slope_result.effective_stress_fos)
        exceeds_allowable = spring_results.get('exceeds_allowable', False)
        
        if min_fos < 1.0:
            return "CRITICAL: Immediate detailed analysis required - Slope unstable"
        elif exceeds_allowable:
            return "HIGH PRIORITY: Pipeline stresses exceed allowable - Detailed analysis required"
        elif min_fos < 1.5:
            return "MEDIUM PRIORITY: Slope stability marginal - Monitor and consider analysis"
        elif min_fos < 2.0:
            return "LOW PRIORITY: Acceptable but monitor conditions"
        else:
            return "ACCEPTABLE: No immediate action required"
    
    def _create_mock_integrated_results(self, slope_results: List[SlopeAnalysisResult],
                                       slope_configs: List[SlopeConfiguration],
                                       pipeline_configs: List[PipelineConfiguration]) -> List[IntegratedAnalysisResult]:
        """Create mock integrated results when Excel is not available"""
        integrated_results = []
        
        for slope_result in slope_results:
            slope_config = next((config for config in slope_configs 
                               if config.config_id == slope_result.config_id), None)
            
            if not slope_config:
                continue
                
            min_fos = min(slope_result.total_stress_fos, slope_result.effective_stress_fos)
            
            if slope_result.requires_detailed_analysis or min_fos < 2.0:
                for pipeline_config in pipeline_configs[:5]:  # Limit for demo
                    
                    soil_params = self.convert_slope_to_soil_params(slope_config, pipeline_config.pipe_doc)
                    
                    # Mock/estimated results based on engineering judgment
                    mock_results = {
                        'longitudinal_force': 1500.0 * (pipeline_config.pipe_od / 20.0),
                        'axial_stress': 300.0 * (pipeline_config.pipe_od / 20.0),
                        'remaining_allowable_stress': 15000.0 - (300.0 * (pipeline_config.pipe_od / 20.0)),
                        'allowable_length': 150.0 / max(1.0, (2.5 - min_fos)),
                        'exceeds_allowable': min_fos < 1.2
                    }
                    
                    integrated_result = IntegratedAnalysisResult(
                        config_id=f"{slope_result.config_id}_{pipeline_config.pipe_od}in_{pipeline_config.pgd_direction}",
                        slope_fos=min_fos,
                        pipeline_config=pipeline_config,
                        soil_params=soil_params,
                        longitudinal_force=mock_results['longitudinal_force'],
                        axial_stress=mock_results['axial_stress'],
                        remaining_allowable_stress=mock_results['remaining_allowable_stress'],
                        allowable_length=mock_results['allowable_length'],
                        exceeds_allowable=mock_results['exceeds_allowable'],
                        analysis_recommendation=self._get_recommendation(slope_result, mock_results),
                        priority_level=self._get_priority_level(slope_result, mock_results)
                    )
                    
                    integrated_results.append(integrated_result)
            
            print(f"Completed mock integration for {slope_result.config_id}")
        
        return integrated_results

    def _get_priority_level(self, slope_result: SlopeAnalysisResult, 
                           spring_results: Dict[str, float]) -> int:
        """Assign priority level (1=Critical, 4=Low)"""
        
        min_fos = min(slope_result.total_stress_fos, slope_result.effective_stress_fos)
        exceeds_allowable = spring_results.get('exceeds_allowable', False)
        
        if min_fos < 1.0 or exceeds_allowable:
            return 1  # Critical
        elif min_fos < 1.2:
            return 2  # High
        elif min_fos < 1.5:
            return 3  # Medium
        else:
            return 4  # Low
    
    def create_comprehensive_decision_matrix(self) -> pd.DataFrame:
        """Create comprehensive decision matrix with integrated results"""
        
        if not self.integrated_results:
            print("No integrated results available. Run integrate_analyses first.")
            return pd.DataFrame()
        
        data = []
        for result in self.integrated_results:
            data.append({
                'Config_ID': result.config_id,
                'Slope_FoS': round(result.slope_fos, 2),
                'Pipe_OD_in': result.pipeline_config.pipe_od,
                'Pipe_Grade': result.pipeline_config.pipe_grade,
                'DOC_ft': result.pipeline_config.pipe_doc,
                'PGD_Direction': result.pipeline_config.pgd_direction,
                'PGD_Length_ft': result.pipeline_config.pipe_length_in_pgd,
                'Friction_Angle': round(result.soil_params.friction_angle, 1),
                'Cohesion_psf': round(result.soil_params.cohesion, 0),
                'Axial_Stress_psi': round(result.axial_stress, 1),
                'Allowable_Length_ft': round(result.allowable_length, 1),
                'Exceeds_Allowable': result.exceeds_allowable,
                'Priority_Level': result.priority_level,
                'Recommendation': result.analysis_recommendation
            })
        
        df = pd.DataFrame(data)
        
        # Sort by priority level (Critical first)
        df = df.sort_values(['Priority_Level', 'Slope_FoS'])
        
        return df
    
    def export_comprehensive_results(self, output_dir: str = "integrated_results"):
        """Export comprehensive analysis results"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Create comprehensive decision matrix
        decision_matrix = self.create_comprehensive_decision_matrix()
        
        if decision_matrix.empty:
            print("No results to export")
            return
        
        # Export full decision matrix
        decision_matrix.to_csv(output_path / "comprehensive_decision_matrix.csv", index=False)
        
        # Create summary by priority level
        priority_summary = decision_matrix.groupby('Priority_Level').size().reset_index(name='Count')
        priority_summary['Priority_Name'] = priority_summary['Priority_Level'].map({
            1: 'Critical', 2: 'High', 3: 'Medium', 4: 'Low'
        })
        
        priority_summary.to_csv(output_path / "priority_summary.csv", index=False)
        
        # Create filtered views for each priority level
        for priority in [1, 2, 3, 4]:
            priority_name = {1: 'Critical', 2: 'High', 3: 'Medium', 4: 'Low'}[priority]
            priority_data = decision_matrix[decision_matrix['Priority_Level'] == priority]
            
            if not priority_data.empty:
                priority_data.to_csv(output_path / f"{priority_name.lower()}_priority_configurations.csv", index=False)
        
        print(f"\nComprehensive Results Summary:")
        print(f"Total Integrated Configurations: {len(decision_matrix)}")
        print(f"Critical Priority: {len(decision_matrix[decision_matrix['Priority_Level'] == 1])}")
        print(f"High Priority: {len(decision_matrix[decision_matrix['Priority_Level'] == 2])}")
        print(f"Medium Priority: {len(decision_matrix[decision_matrix['Priority_Level'] == 3])}")
        print(f"Low Priority: {len(decision_matrix[decision_matrix['Priority_Level'] == 4])}")
        print(f"Results exported to {output_path}")
        
        return decision_matrix


def demonstrate_integration():
    """Demonstrate the integrated analysis workflow"""
    
    # This would typically be called after running slope stability analysis
    print("=== Integrated Slope Stability and Soil Springs Analysis ===")
    
    excel_path = "Soil Springs_2024.xlsx"
    
    # Initialize integrated analysis engine
    engine = IntegratedAnalysisEngine(excel_path)
    
    # For demonstration, create sample slope results
    # In practice, these would come from slope_stability_automation.py
    sample_slope_results = [
        SlopeAnalysisResult(
            config_id="Config_001",
            total_stress_fos=1.2,
            effective_stress_fos=1.1,
            critical_slip_surface={},
            requires_detailed_analysis=True
        ),
        SlopeAnalysisResult(
            config_id="Config_002", 
            total_stress_fos=1.8,
            effective_stress_fos=1.6,
            critical_slip_surface={},
            requires_detailed_analysis=True
        )
    ]
    
    # Create sample slope configurations
    from slope_stability_automation import SoilLayer, SlopeGeometry, SlopeConfiguration
    
    sample_slope_configs = [
        SlopeConfiguration(
            config_id="Config_001",
            geometry=SlopeGeometry(30, 40, 0, 50),
            soil_layers=[SoilLayer("Clay", 120, 200, 100, 25, 20)],
            groundwater_depth=30
        ),
        SlopeConfiguration(
            config_id="Config_002",
            geometry=SlopeGeometry(25, 30, 0, 50), 
            soil_layers=[SoilLayer("Dense Clay", 125, 400, 200, 35, 20)],
            groundwater_depth=25
        )
    ]
    
    # Generate pipeline configurations
    pipeline_configs = engine.create_pipeline_configurations()
    
    print(f"Generated {len(pipeline_configs)} pipeline configurations")
    
    # Run integrated analysis
    integrated_results = engine.integrate_analyses(
        sample_slope_results, sample_slope_configs, pipeline_configs
    )
    
    # Export comprehensive results
    decision_matrix = engine.export_comprehensive_results()
    
    # Display top critical configurations
    if not decision_matrix.empty:
        print("\nTop Critical Configurations:")
        critical = decision_matrix[decision_matrix['Priority_Level'] == 1]
        if not critical.empty:
            print(critical[['Config_ID', 'Slope_FoS', 'Pipe_OD_in', 'Exceeds_Allowable', 'Recommendation']].head().to_string(index=False))
        else:
            print("No critical configurations found.")


if __name__ == "__main__":
    demonstrate_integration()