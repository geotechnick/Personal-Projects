#!/usr/bin/env python3
"""
Slope Geometry Visualizer
Generates detailed visualization files showing slope geometry, soil strata, 
failure surfaces, and pipeline locations for engineering review.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Arc
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import json
from dataclasses import asdict

from slope_stability_automation import SlopeConfiguration, SlopeGeometry, SoilLayer, SlopeAnalysisResult


class SlopeGeometryVisualizer:
    """
    Visualizer for slope geometry, soil layers, failure surfaces, and pipeline locations
    """
    
    def __init__(self, output_dir: str = "analysis_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Color schemes for different elements
        self.soil_colors = {
            'Weak Clay': '#8B4513',      # Saddle brown
            'Medium Clay': '#A0522D',    # Sienna
            'Dense Clay': '#654321',     # Dark brown
            'Medium Soil': '#D2B48C',    # Tan
            'Dense Soil': '#F4A460',     # Sandy brown
            'Rock': '#696969',           # Dim gray
        }
        
        self.default_soil_colors = ['#D2691E', '#CD853F', '#DEB887', '#BC8F8F', '#F5DEB3']
        self.pipe_color = '#FF4500'      # Orange red
        self.slip_surface_color = '#FF0000'  # Red
        self.groundwater_color = '#00CED1'   # Dark turquoise
        
    def create_slope_geometry_plot(self, 
                                 config: SlopeConfiguration, 
                                 analysis_result: Optional[SlopeAnalysisResult] = None,
                                 pipe_diameter_in: float = 24.0,
                                 pipe_depth_ft: float = 4.0) -> str:
        """
        Create comprehensive slope geometry plot with all elements
        
        Args:
            config: Slope configuration
            analysis_result: Analysis results with failure surface
            pipe_diameter_in: Pipeline diameter in inches
            pipe_depth_ft: Pipeline depth of cover in feet
            
        Returns:
            Path to saved plot file
        """
        
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # Calculate slope geometry points
        slope_points = self._calculate_slope_boundary_points(config.geometry)
        
        # Plot soil layers
        self._plot_soil_layers(ax, config.geometry, config.soil_layers, slope_points)
        
        # Plot slope boundary
        self._plot_slope_boundary(ax, slope_points)
        
        # Plot groundwater table
        if config.groundwater_depth > 0:
            self._plot_groundwater_table(ax, slope_points, config.groundwater_depth)
        
        # Plot failure surface if available
        if analysis_result and analysis_result.critical_slip_surface:
            self._plot_failure_surface(ax, analysis_result.critical_slip_surface, slope_points)
        
        # Plot pipeline location
        self._plot_pipeline(ax, slope_points, pipe_diameter_in, pipe_depth_ft)
        
        # Add dimensions and annotations
        self._add_dimensions_and_annotations(ax, config, analysis_result, pipe_diameter_in, pipe_depth_ft)
        
        # Format plot
        self._format_plot(ax, config, analysis_result)
        
        # Save plot
        filename = f"slope_geometry_{config.config_id}.png"
        filepath = self.output_dir / filename
        
        plt.savefig(filepath, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        # Also create a detailed data file
        self._create_geometry_data_file(config, analysis_result, pipe_diameter_in, pipe_depth_ft)
        
        return str(filepath)
    
    def _calculate_slope_boundary_points(self, geometry: SlopeGeometry) -> List[Tuple[float, float]]:
        """Calculate slope boundary points"""
        
        slope_rad = np.radians(geometry.slope_angle)
        slope_rise = geometry.slope_height
        slope_run = slope_rise / np.tan(slope_rad)
        
        # Define slope profile points
        points = [
            # Left boundary (upstream)
            (-150, -50),
            (-150, slope_rise + 20),
            
            # Slope crest area
            (-20, slope_rise),
            (slope_run, slope_rise),
            
            # Slope face
            (0, 0),  # Toe
            
            # Right boundary (downstream)  
            (geometry.toe_distance + 100, 0),
            (geometry.toe_distance + 100, -50),
            
            # Bottom boundary
            (-150, -50)
        ]
        
        return points
    
    def _plot_soil_layers(self, ax, geometry: SlopeGeometry, soil_layers: List[SoilLayer], 
                         slope_points: List[Tuple[float, float]]):
        """Plot soil layers with different colors and patterns"""
        
        # Extract boundary coordinates
        x_coords = [p[0] for p in slope_points]
        y_coords = [p[1] for p in slope_points]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min = min(y_coords)
        
        # Calculate layer elevations
        current_depth = 0
        layer_elevations = []
        
        for layer in soil_layers:
            top_elevation = -current_depth
            bottom_elevation = -(current_depth + layer.thickness)
            layer_elevations.append((top_elevation, bottom_elevation))
            current_depth += layer.thickness
        
        # Plot each soil layer
        for i, (layer, (top_elev, bottom_elev)) in enumerate(zip(soil_layers, layer_elevations)):
            
            # Get color for this soil layer
            color = self.soil_colors.get(layer.name, self.default_soil_colors[i % len(self.default_soil_colors)])
            
            # Create layer polygon
            layer_points = [
                (x_min, top_elev),
                (x_max, top_elev),
                (x_max, bottom_elev),
                (x_min, bottom_elev)
            ]
            
            layer_polygon = patches.Polygon(layer_points, closed=True, 
                                          facecolor=color, alpha=0.7, 
                                          edgecolor='black', linewidth=0.5,
                                          label=f'{layer.name} (γ={layer.unit_weight} pcf)')
            ax.add_patch(layer_polygon)
            
            # Add layer thickness annotation
            mid_x = (x_min + x_max) / 2 + 20 * i  # Offset for readability
            mid_y = (top_elev + bottom_elev) / 2
            
            ax.annotate(f'{layer.name}\nt = {layer.thickness}\'\nγ = {layer.unit_weight} pcf\nc = {layer.cohesion_total} psf\nφ = {layer.friction_angle}°',
                       xy=(mid_x, mid_y), xytext=(x_max + 20, mid_y),
                       fontsize=8, ha='left', va='center',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.3),
                       arrowprops=dict(arrowstyle='->', lw=0.5))
    
    def _plot_slope_boundary(self, ax, slope_points: List[Tuple[float, float]]):
        """Plot slope boundary"""
        
        # Extract slope face coordinates
        slope_rad = None
        slope_face_points = []
        
        # Find slope toe and crest points
        toe_point = next((p for p in slope_points if p[1] == 0 and p[0] >= 0), (0, 0))
        crest_points = [p for p in slope_points if p[1] > 0]
        
        if crest_points:
            crest_point = min(crest_points, key=lambda p: p[0])
            
            # Create slope face line
            slope_face_points = [toe_point, crest_point]
            
            # Plot slope face
            slope_x = [p[0] for p in slope_face_points]
            slope_y = [p[1] for p in slope_face_points]
            ax.plot(slope_x, slope_y, 'k-', linewidth=3, label='Slope Face')
            
            # Calculate and display slope angle
            rise = crest_point[1] - toe_point[1]
            run = crest_point[0] - toe_point[0]
            slope_angle = np.degrees(np.arctan(rise / run)) if run != 0 else 90
            
            # Add slope angle annotation
            mid_x = (toe_point[0] + crest_point[0]) / 2
            mid_y = (toe_point[1] + crest_point[1]) / 2
            ax.annotate(f'{slope_angle:.1f}°', 
                       xy=(mid_x, mid_y), xytext=(mid_x - 15, mid_y + 10),
                       fontsize=10, fontweight='bold', color='red',
                       arrowprops=dict(arrowstyle='->', color='red'))
        
        # Plot ground surface
        ground_points = [(p[0], max(0, p[1])) for p in slope_points if p[1] >= -1]
        if len(ground_points) > 1:
            ground_x = [p[0] for p in ground_points]
            ground_y = [p[1] for p in ground_points]
            ax.plot(ground_x, ground_y, 'k-', linewidth=2, alpha=0.8, label='Ground Surface')
    
    def _plot_groundwater_table(self, ax, slope_points: List[Tuple[float, float]], gw_depth: float):
        """Plot groundwater table"""
        
        x_coords = [p[0] for p in slope_points]
        x_min, x_max = min(x_coords), max(x_coords)
        
        gw_elevation = -gw_depth
        
        # Plot groundwater table line
        ax.plot([x_min, x_max], [gw_elevation, gw_elevation], 
               color=self.groundwater_color, linestyle='--', linewidth=2, 
               label=f'Groundwater Table (depth = {gw_depth} ft)')
        
        # Add water symbols
        for x in np.linspace(x_min + 20, x_max - 20, 8):
            ax.plot(x, gw_elevation, 'o', color=self.groundwater_color, markersize=4, alpha=0.7)
    
    def _plot_failure_surface(self, ax, slip_surface: Dict[str, Any], slope_points: List[Tuple[float, float]]):
        """Plot critical failure surface"""
        
        if not slip_surface:
            return
        
        surface_type = slip_surface.get('surface_type', 'circular')
        
        if surface_type == 'circular':
            # Plot circular failure surface
            center_x = slip_surface.get('center_x', 0)
            center_y = slip_surface.get('center_y', 0)
            radius = slip_surface.get('radius', 50)
            
            # Create circular arc for failure surface
            circle = Circle((center_x, center_y), radius, 
                          fill=False, color=self.slip_surface_color, 
                          linewidth=3, linestyle='-', alpha=0.8,
                          label='Critical Failure Surface')
            ax.add_patch(circle)
            
            # Add center point
            ax.plot(center_x, center_y, 'x', color=self.slip_surface_color, 
                   markersize=8, markeredgewidth=2)
            
            # Add radius dimension
            ax.annotate(f'R = {radius:.1f} ft', 
                       xy=(center_x + radius*0.7, center_y + radius*0.7),
                       fontsize=9, color=self.slip_surface_color, fontweight='bold')
        
        elif surface_type == 'coordinates' and slip_surface.get('coordinates'):
            # Plot failure surface from coordinates
            coords = slip_surface['coordinates']
            if len(coords) > 1:
                x_coords = [c[0] for c in coords]
                y_coords = [c[1] for c in coords]
                ax.plot(x_coords, y_coords, color=self.slip_surface_color, 
                       linewidth=3, label='Critical Failure Surface', alpha=0.8)
    
    def _plot_pipeline(self, ax, slope_points: List[Tuple[float, float]], 
                      pipe_diameter_in: float, pipe_depth_ft: float):
        """Plot pipeline location and details"""
        
        # Convert diameter to feet
        pipe_diameter_ft = pipe_diameter_in / 12.0
        pipe_radius_ft = pipe_diameter_ft / 2.0
        
        # Determine pipeline location (typically crossing the slope toe area)
        x_coords = [p[0] for p in slope_points]
        x_min, x_max = min(x_coords), max(x_coords)
        
        # Pipeline typically runs perpendicular to slope, across toe area
        pipe_y = -pipe_depth_ft - pipe_radius_ft  # Pipe centerline elevation
        pipe_x_start = x_min + 30
        pipe_x_end = x_max - 30
        
        # Plot pipeline as a thick line
        ax.plot([pipe_x_start, pipe_x_end], [pipe_y, pipe_y], 
               color=self.pipe_color, linewidth=6, 
               label=f'Pipeline ({pipe_diameter_in}" OD)')
        
        # Add pipeline circles at key locations to show cross-section
        key_x_locations = [pipe_x_start + 20, 0, pipe_x_start + (pipe_x_end - pipe_x_start)*0.75]
        
        for x_loc in key_x_locations:
            if pipe_x_start <= x_loc <= pipe_x_end:
                pipe_circle = Circle((x_loc, pipe_y), pipe_radius_ft,
                                   facecolor=self.pipe_color, alpha=0.3,
                                   edgecolor=self.pipe_color, linewidth=2)
                ax.add_patch(pipe_circle)
        
        # Add pipeline annotations
        mid_x = (pipe_x_start + pipe_x_end) / 2
        ax.annotate(f'Pipeline\nOD = {pipe_diameter_in}"\nDOC = {pipe_depth_ft} ft',
                   xy=(mid_x, pipe_y), xytext=(mid_x, pipe_y - 20),
                   ha='center', va='top', fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor=self.pipe_color, alpha=0.2),
                   arrowprops=dict(arrowstyle='->', lw=1))
        
        # Add depth of cover dimension
        ax.annotate('', xy=(mid_x + 40, 0), xytext=(mid_x + 40, pipe_y + pipe_radius_ft),
                   arrowprops=dict(arrowstyle='<->', lw=1.5, color='blue'))
        ax.text(mid_x + 45, (0 + pipe_y + pipe_radius_ft)/2, f'{pipe_depth_ft} ft\nDOC', 
               fontsize=8, color='blue', va='center', ha='left',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='lightblue', alpha=0.7))
    
    def _add_dimensions_and_annotations(self, ax, config: SlopeConfiguration, 
                                      analysis_result: Optional[SlopeAnalysisResult],
                                      pipe_diameter_in: float, pipe_depth_ft: float):
        """Add dimensions and engineering annotations"""
        
        geometry = config.geometry
        
        # Slope height dimension
        slope_rad = np.radians(geometry.slope_angle)
        slope_run = geometry.slope_height / np.tan(slope_rad)
        
        # Height dimension line
        ax.annotate('', xy=(-120, 0), xytext=(-120, geometry.slope_height),
                   arrowprops=dict(arrowstyle='<->', lw=1.5, color='green'))
        ax.text(-130, geometry.slope_height/2, f'{geometry.slope_height} ft\nSlope Height', 
               fontsize=9, color='green', va='center', ha='center', rotation=90,
               bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
        
        # Slope length dimension
        slope_length = np.sqrt(slope_run**2 + geometry.slope_height**2)
        mid_slope_x = slope_run / 2
        mid_slope_y = geometry.slope_height / 2
        
        ax.text(mid_slope_x - 10, mid_slope_y + 5, f'L = {slope_length:.1f} ft', 
               fontsize=9, color='red', fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.7))
    
    def _format_plot(self, ax, config: SlopeConfiguration, 
                    analysis_result: Optional[SlopeAnalysisResult]):
        """Format the plot with labels, title, and legend"""
        
        # Set labels and title
        ax.set_xlabel('Distance (ft)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Elevation (ft)', fontsize=12, fontweight='bold')
        
        title = f'Slope Geometry Analysis - Configuration {config.config_id}\n'
        title += f'Slope: {config.geometry.slope_angle}° × {config.geometry.slope_height} ft'
        
        if analysis_result:
            title += f' | FoS = {analysis_result.effective_stress_fos:.2f}'
            
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Set equal aspect ratio for accurate geometry representation
        ax.set_aspect('equal', adjustable='box')
        
        # Add grid
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # Add legend
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        
        # Set reasonable axis limits
        slope_points = self._calculate_slope_boundary_points(config.geometry)
        x_coords = [p[0] for p in slope_points]
        y_coords = [p[1] for p in slope_points]
        
        x_margin = (max(x_coords) - min(x_coords)) * 0.1
        y_margin = (max(y_coords) - min(y_coords)) * 0.15
        
        ax.set_xlim(min(x_coords) - x_margin, max(x_coords) + x_margin)
        ax.set_ylim(min(y_coords) - y_margin, max(y_coords) + y_margin)
    
    def _create_geometry_data_file(self, config: SlopeConfiguration, 
                                 analysis_result: Optional[SlopeAnalysisResult],
                                 pipe_diameter_in: float, pipe_depth_ft: float):
        """Create detailed geometry data file"""
        
        # Calculate key geometric parameters
        geometry = config.geometry
        slope_rad = np.radians(geometry.slope_angle)
        slope_run = geometry.slope_height / np.tan(slope_rad)
        slope_length = np.sqrt(slope_run**2 + geometry.slope_height**2)
        
        # Create comprehensive data structure
        geometry_data = {
            'configuration_id': config.config_id,
            'slope_geometry': {
                'angle_degrees': geometry.slope_angle,
                'height_ft': geometry.slope_height,
                'horizontal_run_ft': slope_run,
                'slope_length_ft': slope_length,
                'bench_width_ft': geometry.bench_width,
                'toe_distance_ft': geometry.toe_distance
            },
            'soil_layers': [
                {
                    'name': layer.name,
                    'unit_weight_pcf': layer.unit_weight,
                    'cohesion_total_psf': layer.cohesion_total,
                    'cohesion_effective_psf': layer.cohesion_effective,
                    'friction_angle_degrees': layer.friction_angle,
                    'thickness_ft': layer.thickness
                } for layer in config.soil_layers
            ],
            'groundwater': {
                'depth_below_surface_ft': config.groundwater_depth
            },
            'pipeline': {
                'diameter_in': pipe_diameter_in,
                'diameter_ft': pipe_diameter_in / 12.0,
                'depth_of_cover_ft': pipe_depth_ft,
                'centerline_elevation_ft': -(pipe_depth_ft + pipe_diameter_in/24.0)
            },
            'boundary_points': self._calculate_slope_boundary_points(geometry)
        }
        
        # Add analysis results if available
        if analysis_result:
            geometry_data['analysis_results'] = {
                'total_stress_fos': analysis_result.total_stress_fos,
                'effective_stress_fos': analysis_result.effective_stress_fos,
                'requires_detailed_analysis': analysis_result.requires_detailed_analysis,
                'critical_slip_surface': analysis_result.critical_slip_surface
            }
        
        # Save to JSON file
        data_filename = f"geometry_data_{config.config_id}.json"
        data_filepath = self.output_dir / data_filename
        
        with open(data_filepath, 'w') as f:
            json.dump(geometry_data, f, indent=2, default=str)
    
    def create_multiple_slope_plots(self, 
                                  configurations: List[SlopeConfiguration],
                                  analysis_results: List[SlopeAnalysisResult] = None,
                                  pipe_diameter_in: float = 24.0,
                                  pipe_depth_ft: float = 4.0) -> List[str]:
        """
        Create slope geometry plots for multiple configurations
        
        Args:
            configurations: List of slope configurations
            analysis_results: List of corresponding analysis results
            pipe_diameter_in: Pipeline diameter
            pipe_depth_ft: Pipeline depth of cover
            
        Returns:
            List of file paths for generated plots
        """
        
        created_files = []
        
        for i, config in enumerate(configurations):
            result = analysis_results[i] if analysis_results and i < len(analysis_results) else None
            
            try:
                filepath = self.create_slope_geometry_plot(config, result, pipe_diameter_in, pipe_depth_ft)
                created_files.append(filepath)
            except Exception as e:
                print(f"Error creating plot for configuration {config.config_id}: {e}")
                continue
        
        return created_files
    
    def create_summary_slope_comparison(self, 
                                      configurations: List[SlopeConfiguration],
                                      analysis_results: List[SlopeAnalysisResult] = None,
                                      max_plots: int = 6) -> str:
        """
        Create a summary comparison plot showing multiple slope configurations
        
        Args:
            configurations: List of slope configurations  
            analysis_results: List of analysis results
            max_plots: Maximum number of slopes to show in comparison
            
        Returns:
            Path to summary comparison plot
        """
        
        # Limit to most critical configurations
        if analysis_results:
            # Sort by Factor of Safety (ascending - most critical first)
            paired = list(zip(configurations, analysis_results))
            paired.sort(key=lambda x: x[1].effective_stress_fos)
            configurations = [p[0] for p in paired[:max_plots]]
            analysis_results = [p[1] for p in paired[:max_plots]]
        else:
            configurations = configurations[:max_plots]
        
        # Create subplot grid
        rows = 2
        cols = 3
        fig, axes = plt.subplots(rows, cols, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, config in enumerate(configurations):
            if i >= max_plots:
                break
                
            ax = axes[i]
            result = analysis_results[i] if analysis_results else None
            
            # Calculate and plot slope profile  
            slope_points = self._calculate_slope_boundary_points(config.geometry)
            
            # Plot soil layers (simplified)
            self._plot_soil_layers(ax, config.geometry, config.soil_layers, slope_points)
            
            # Plot slope boundary
            self._plot_slope_boundary(ax, slope_points)
            
            # Plot failure surface if available
            if result and result.critical_slip_surface:
                self._plot_failure_surface(ax, result.critical_slip_surface, slope_points)
            
            # Format individual subplot
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
            
            title = f'{config.config_id}\n{config.geometry.slope_angle}° × {config.geometry.slope_height} ft'
            if result:
                title += f'\nFoS = {result.effective_stress_fos:.2f}'
            ax.set_title(title, fontsize=10)
            
            ax.set_xlabel('Distance (ft)', fontsize=8)
            ax.set_ylabel('Elevation (ft)', fontsize=8)
        
        # Hide unused subplots
        for i in range(len(configurations), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.suptitle('Critical Slope Configurations Comparison', fontsize=16, fontweight='bold', y=0.98)
        
        # Save comparison plot
        comparison_filename = "slope_configurations_comparison.png"
        comparison_filepath = self.output_dir / comparison_filename
        
        plt.savefig(comparison_filepath, dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close()
        
        return str(comparison_filepath)


def main():
    """Test function for slope geometry visualization"""
    
    # Create test configuration
    test_geometry = SlopeGeometry(
        slope_angle=30,
        slope_height=60,
        bench_width=0,
        toe_distance=50
    )
    
    test_soil_layers = [
        SoilLayer("Weak Clay", 115, 100, 50, 15, 25),
        SoilLayer("Dense Soil", 125, 400, 200, 35, 35)
    ]
    
    test_config = SlopeConfiguration(
        config_id="TEST_001",
        geometry=test_geometry,
        soil_layers=test_soil_layers,
        groundwater_depth=15
    )
    
    # Create test analysis result with failure surface
    test_slip_surface = {
        'surface_type': 'circular',
        'center_x': 20,
        'center_y': 40,
        'radius': 45
    }
    
    test_result = SlopeAnalysisResult(
        config_id="TEST_001",
        total_stress_fos=1.45,
        effective_stress_fos=1.25,
        critical_slip_surface=test_slip_surface,
        requires_detailed_analysis=True
    )
    
    # Create visualizer and generate plot
    visualizer = SlopeGeometryVisualizer("test_output")
    
    plot_file = visualizer.create_slope_geometry_plot(
        test_config, test_result, pipe_diameter_in=30, pipe_depth_ft=5
    )
    
    print(f"Test plot created: {plot_file}")
    
    # Test comparison plot
    configs = [test_config] * 3
    results = [test_result] * 3
    
    comparison_file = visualizer.create_summary_slope_comparison(configs, results)
    print(f"Comparison plot created: {comparison_file}")


if __name__ == "__main__":
    main()