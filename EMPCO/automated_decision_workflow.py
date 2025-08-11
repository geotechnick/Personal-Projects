#!/usr/bin/env python3
"""
Automated Decision Workflow
Complete workflow for automated slope stability analysis and decision matrix generation.
Determines which slope configurations require detailed soil springs analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from typing import List, Dict, Tuple
import argparse
import logging
from datetime import datetime

from slope_stability_automation import SlopeStabilityAnalyzer, SlopeConfiguration
from soil_springs_integration import IntegratedAnalysisEngine


class AutomatedDecisionWorkflow:
    """Main workflow orchestrator for automated analysis"""
    
    def __init__(self, template_path: str, excel_path: str, output_dir: str = "analysis_results"):
        self.template_path = template_path
        self.excel_path = excel_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize analyzers
        self.slope_analyzer = SlopeStabilityAnalyzer(template_path)
        self.integration_engine = IntegratedAnalysisEngine(excel_path)
        
        # Setup logging
        self._setup_logging()
        
        self.logger.info(f"Initialized automated workflow with output directory: {self.output_dir}")
    
    def _setup_logging(self):
        """Setup logging for the workflow"""
        log_file = self.output_dir / f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def run_complete_analysis(self, 
                            limit_configurations: int = None,
                            generate_plots: bool = True) -> pd.DataFrame:
        """Run complete automated analysis workflow"""
        
        self.logger.info("Starting complete automated analysis workflow")
        
        try:
            # Step 1: Generate slope configurations
            self.logger.info("Step 1: Generating slope configurations")
            slope_configs = self.slope_analyzer.generate_slope_configurations()
            
            if limit_configurations:
                slope_configs = slope_configs[:limit_configurations]
                self.logger.info(f"Limited to {len(slope_configs)} configurations for analysis")
            
            # Step 2: Run slope stability analysis  
            self.logger.info(f"Step 2: Running slope stability analysis on {len(slope_configs)} configurations")
            slope_results = self.slope_analyzer.batch_analyze(slope_configs)
            
            # Step 3: Create initial decision matrix
            self.logger.info("Step 3: Creating slope stability decision matrix")
            slope_decision_matrix = self.slope_analyzer.create_decision_matrix()
            
            # Export slope-only results
            slope_decision_matrix.to_csv(self.output_dir / "slope_stability_decision_matrix.csv", index=False)
            
            # Step 4: Integrate with soil springs analysis for detailed cases
            self.logger.info("Step 4: Integrating with soil springs analysis")
            detailed_slope_results = [r for r in slope_results if r.requires_detailed_analysis]
            detailed_slope_configs = [c for c in slope_configs 
                                    if any(r.config_id == c.config_id for r in detailed_slope_results)]
            
            if detailed_slope_results:
                pipeline_configs = self.integration_engine.create_pipeline_configurations()
                integrated_results = self.integration_engine.integrate_analyses(
                    detailed_slope_results, detailed_slope_configs, pipeline_configs
                )
                
                # Step 5: Create comprehensive decision matrix
                self.logger.info("Step 5: Creating comprehensive decision matrix")
                comprehensive_matrix = self.integration_engine.create_comprehensive_decision_matrix()
                
                # Export comprehensive results
                self.integration_engine.export_comprehensive_results(str(self.output_dir))
                
            else:
                self.logger.info("No configurations require detailed soil springs analysis")
                comprehensive_matrix = pd.DataFrame()
            
            # Step 6: Generate summary report and visualizations
            if generate_plots:
                self.logger.info("Step 6: Generating analysis visualizations")
                self._generate_analysis_plots(slope_decision_matrix, comprehensive_matrix)
            
            # Step 7: Create executive summary
            self.logger.info("Step 7: Creating executive summary")
            self._create_executive_summary(slope_decision_matrix, comprehensive_matrix)
            
            self.logger.info("Complete analysis workflow finished successfully")
            
            return comprehensive_matrix if not comprehensive_matrix.empty else slope_decision_matrix
            
        except Exception as e:
            self.logger.error(f"Error in complete analysis workflow: {e}")
            raise
    
    def run_complete_analysis_with_configs(self, 
                                         slope_configurations: List,
                                         pipeline_configurations: List,
                                         generate_plots: bool = True) -> pd.DataFrame:
        """Run complete analysis with pre-generated configurations"""
        
        self.logger.info("Starting complete analysis with custom configurations")
        
        try:
            # Step 1: Run slope stability analysis on provided configurations
            self.logger.info(f"Step 1: Running slope stability analysis on {len(slope_configurations)} configurations")
            slope_results = self.slope_analyzer.batch_analyze(slope_configurations)
            
            # Step 2: Create initial decision matrix
            self.logger.info("Step 2: Creating slope stability decision matrix")
            slope_decision_matrix = self.slope_analyzer.create_decision_matrix()
            
            # Export slope-only results
            slope_decision_matrix.to_csv(self.output_dir / "slope_stability_decision_matrix.csv", index=False)
            
            # Step 3: Integrate with soil springs analysis for detailed cases
            self.logger.info("Step 3: Integrating with soil springs analysis")
            detailed_slope_results = [r for r in slope_results if r.requires_detailed_analysis]
            detailed_slope_configs = [c for c in slope_configurations 
                                    if any(r.config_id == c.config_id for r in detailed_slope_results)]
            
            if detailed_slope_results:
                integrated_results = self.integration_engine.integrate_analyses(
                    detailed_slope_results, detailed_slope_configs, pipeline_configurations
                )
                
                # Step 4: Create comprehensive decision matrix
                self.logger.info("Step 4: Creating comprehensive decision matrix")
                comprehensive_matrix = self.integration_engine.create_comprehensive_decision_matrix()
                
                # Export comprehensive results
                self.integration_engine.export_comprehensive_results(str(self.output_dir))
                
            else:
                self.logger.info("No configurations require detailed soil springs analysis")
                comprehensive_matrix = pd.DataFrame()
            
            # Step 5: Generate summary report and visualizations
            if generate_plots:
                self.logger.info("Step 5: Generating analysis visualizations")
                self._generate_analysis_plots(slope_decision_matrix, comprehensive_matrix)
            
            # Step 6: Create executive summary
            self.logger.info("Step 6: Creating executive summary")
            self._create_executive_summary(slope_decision_matrix, comprehensive_matrix)
            
            self.logger.info("Complete analysis workflow finished successfully")
            
            return comprehensive_matrix if not comprehensive_matrix.empty else slope_decision_matrix
            
        except Exception as e:
            self.logger.error(f"Error in complete analysis workflow: {e}")
            raise
    
    def _generate_analysis_plots(self, slope_matrix: pd.DataFrame, 
                               comprehensive_matrix: pd.DataFrame):
        """Generate visualization plots for analysis results"""
        
        plt.style.use('seaborn-v0_8')
        
        # Plot 1: Slope FoS Distribution
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Slope Stability and Pipeline Analysis Results', fontsize=16, fontweight='bold')
        
        # FoS histogram
        axes[0, 0].hist(slope_matrix['Min_FoS'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].axvline(x=1.5, color='red', linestyle='--', label='FoS = 1.5 Threshold')
        axes[0, 0].set_xlabel('Minimum Factor of Safety')
        axes[0, 0].set_ylabel('Number of Configurations')
        axes[0, 0].set_title('Distribution of Minimum Factor of Safety')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Priority distribution pie chart
        priority_counts = slope_matrix['Analysis_Priority'].value_counts()
        axes[0, 1].pie(priority_counts.values, labels=priority_counts.index, autopct='%1.1f%%',
                      colors=['red', 'orange', 'yellow', 'green'])
        axes[0, 1].set_title('Analysis Priority Distribution')
        
        # Detailed analysis requirement
        detailed_req = slope_matrix['Requires_Detailed_Analysis'].value_counts()
        axes[1, 0].bar(detailed_req.index.map({True: 'Required', False: 'Not Required'}), 
                      detailed_req.values, color=['red', 'green'], alpha=0.7)
        axes[1, 0].set_ylabel('Number of Configurations')
        axes[1, 0].set_title('Detailed Analysis Requirement')
        axes[1, 0].grid(True, alpha=0.3)
        
        # FoS vs Configuration scatter
        if not comprehensive_matrix.empty:
            scatter = axes[1, 1].scatter(comprehensive_matrix['Slope_FoS'], 
                                       comprehensive_matrix['Axial_Stress_psi'],
                                       c=comprehensive_matrix['Priority_Level'], 
                                       cmap='RdYlGn_r', alpha=0.7)
            axes[1, 1].set_xlabel('Slope Factor of Safety')
            axes[1, 1].set_ylabel('Pipeline Axial Stress (psi)')
            axes[1, 1].set_title('Slope FoS vs Pipeline Stress')
            plt.colorbar(scatter, ax=axes[1, 1], label='Priority Level')
        else:
            axes[1, 1].text(0.5, 0.5, 'No Comprehensive\nAnalysis Data', 
                          ha='center', va='center', transform=axes[1, 1].transAxes,
                          fontsize=12, style='italic')
            axes[1, 1].set_title('Slope FoS vs Pipeline Stress')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'analysis_summary_plots.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Plot 2: Decision Matrix Heatmap (if comprehensive data available)
        if not comprehensive_matrix.empty and len(comprehensive_matrix) > 1:
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create pivot table for heatmap
            pivot_data = comprehensive_matrix.pivot_table(
                values='Priority_Level', 
                index='Pipe_OD_in',
                columns='Slope_FoS',
                aggfunc='mean'
            )
            
            sns.heatmap(pivot_data, annot=True, cmap='RdYlGn_r', ax=ax, cbar_kws={'label': 'Priority Level'})
            ax.set_title('Decision Matrix: Pipeline Size vs Slope Factor of Safety')
            ax.set_xlabel('Slope Factor of Safety')
            ax.set_ylabel('Pipeline Outside Diameter (inches)')
            
            plt.tight_layout()
            plt.savefig(self.output_dir / 'decision_matrix_heatmap.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        self.logger.info(f"Analysis plots saved to {self.output_dir}")
    
    def _create_executive_summary(self, slope_matrix: pd.DataFrame, 
                                comprehensive_matrix: pd.DataFrame):
        """Create executive summary report"""
        
        summary_file = self.output_dir / 'executive_summary.txt'
        
        with open(summary_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("AUTOMATED SLOPE STABILITY AND PIPELINE ANALYSIS\n")
            f.write("EXECUTIVE SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Output Directory: {self.output_dir}\n\n")
            
            # Slope Analysis Summary
            f.write("SLOPE STABILITY ANALYSIS SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Configurations Analyzed: {len(slope_matrix)}\n")
            
            if not slope_matrix.empty:
                requiring_detailed = slope_matrix['Requires_Detailed_Analysis'].sum()
                f.write(f"Configurations Requiring Detailed Analysis: {requiring_detailed} ({requiring_detailed/len(slope_matrix)*100:.1f}%)\n")
                
                min_fos = slope_matrix['Min_FoS'].min()
                max_fos = slope_matrix['Min_FoS'].max()
                avg_fos = slope_matrix['Min_FoS'].mean()
                
                f.write(f"Factor of Safety Range: {min_fos:.2f} - {max_fos:.2f}\n")
                f.write(f"Average Factor of Safety: {avg_fos:.2f}\n\n")
                
                # Priority breakdown
                priority_counts = slope_matrix['Analysis_Priority'].value_counts()
                f.write("Analysis Priority Breakdown:\n")
                for priority, count in priority_counts.items():
                    f.write(f"  {priority}: {count} configurations ({count/len(slope_matrix)*100:.1f}%)\n")
                f.write("\n")
            
            # Comprehensive Analysis Summary (if available)
            if not comprehensive_matrix.empty:
                f.write("INTEGRATED PIPELINE ANALYSIS SUMMARY\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total Integrated Configurations: {len(comprehensive_matrix)}\n")
                
                critical_count = len(comprehensive_matrix[comprehensive_matrix['Priority_Level'] == 1])
                high_count = len(comprehensive_matrix[comprehensive_matrix['Priority_Level'] == 2])
                
                f.write(f"Critical Priority Configurations: {critical_count}\n")
                f.write(f"High Priority Configurations: {high_count}\n")
                
                exceeds_allowable = comprehensive_matrix['Exceeds_Allowable'].sum()
                f.write(f"Configurations Exceeding Allowable Stress: {exceeds_allowable}\n\n")
                
                if critical_count > 0:
                    f.write("TOP CRITICAL CONFIGURATIONS:\n")
                    critical_configs = comprehensive_matrix[comprehensive_matrix['Priority_Level'] == 1]
                    critical_configs = critical_configs.sort_values('Slope_FoS').head(5)
                    
                    for _, config in critical_configs.iterrows():
                        f.write(f"  Config ID: {config['Config_ID']}\n")
                        f.write(f"    Slope FoS: {config['Slope_FoS']:.2f}\n")
                        f.write(f"    Pipeline: {config['Pipe_OD_in']}\" {config['Pipe_Grade']}\n")
                        f.write(f"    Exceeds Allowable: {config['Exceeds_Allowable']}\n")
                        f.write(f"    Recommendation: {config['Recommendation']}\n\n")
            
            # Recommendations
            f.write("KEY RECOMMENDATIONS\n")
            f.write("-" * 40 + "\n")
            
            if not slope_matrix.empty:
                critical_slope_count = len(slope_matrix[slope_matrix['Analysis_Priority'] == 'Critical'])
                if critical_slope_count > 0:
                    f.write(f"• IMMEDIATE ACTION: {critical_slope_count} configurations have critical slope stability issues\n")
                
                marginal_count = len(slope_matrix[slope_matrix['Min_FoS'] < 1.5])
                if marginal_count > 0:
                    f.write(f"• MONITORING REQUIRED: {marginal_count} configurations have Factor of Safety < 1.5\n")
            
            if not comprehensive_matrix.empty:
                stress_exceed_count = comprehensive_matrix['Exceeds_Allowable'].sum()
                if stress_exceed_count > 0:
                    f.write(f"• PIPELINE CONCERN: {stress_exceed_count} pipeline configurations exceed allowable stress\n")
            
            f.write("• Review all Critical and High priority configurations immediately\n")
            f.write("• Consider design modifications for configurations exceeding allowable limits\n")
            f.write("• Implement monitoring program for marginal configurations\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF EXECUTIVE SUMMARY\n")
            f.write("=" * 80 + "\n")
        
        self.logger.info(f"Executive summary saved to {summary_file}")
    
    def generate_configuration_recommendations(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Generate specific recommendations for each configuration"""
        
        if results_df.empty:
            return pd.DataFrame()
        
        recommendations = []
        
        for _, row in results_df.iterrows():
            config_id = row.get('Config_ID', 'Unknown')
            min_fos = row.get('Min_FoS', row.get('Slope_FoS', 0))
            
            recommendation = {
                'Config_ID': config_id,
                'Min_FoS': min_fos,
                'Action_Required': self._get_action_required(row),
                'Timeline': self._get_timeline(row),
                'Estimated_Cost': self._get_estimated_cost(row),
                'Risk_Level': self._get_risk_level(row)
            }
            
            recommendations.append(recommendation)
        
        recommendations_df = pd.DataFrame(recommendations)
        recommendations_df.to_csv(self.output_dir / 'configuration_recommendations.csv', index=False)
        
        return recommendations_df
    
    def _get_action_required(self, row) -> str:
        """Determine action required based on analysis results"""
        min_fos = row.get('Min_FoS', row.get('Slope_FoS', 0))
        exceeds_allowable = row.get('Exceeds_Allowable', False)
        priority = row.get('Priority_Level', row.get('Analysis_Priority', 'Low'))
        
        if min_fos < 1.0 or exceeds_allowable:
            return "Immediate detailed geotechnical analysis and design review"
        elif min_fos < 1.2 or priority in ['Critical', 1]:
            return "Detailed analysis within 30 days, consider design modifications"
        elif min_fos < 1.5 or priority in ['High', 2]:
            return "Engineering evaluation within 60 days"
        else:
            return "Routine monitoring and periodic review"
    
    def _get_timeline(self, row) -> str:
        """Get recommended timeline for action"""
        min_fos = row.get('Min_FoS', row.get('Slope_FoS', 0))
        priority = row.get('Priority_Level', row.get('Analysis_Priority', 'Low'))
        
        if min_fos < 1.0 or priority in ['Critical', 1]:
            return "Immediate (0-7 days)"
        elif min_fos < 1.2 or priority in ['High', 2]:
            return "Short-term (1-4 weeks)"
        elif min_fos < 1.5 or priority in ['Medium', 3]:
            return "Medium-term (1-3 months)"
        else:
            return "Long-term (6-12 months)"
    
    def _get_estimated_cost(self, row) -> str:
        """Estimate cost category for required action"""
        priority = row.get('Priority_Level', row.get('Analysis_Priority', 'Low'))
        
        cost_map = {
            'Critical': '$50,000 - $200,000',
            'High': '$20,000 - $75,000', 
            'Medium': '$10,000 - $30,000',
            'Low': '$5,000 - $15,000',
            1: '$50,000 - $200,000',
            2: '$20,000 - $75,000',
            3: '$10,000 - $30,000',
            4: '$5,000 - $15,000'
        }
        
        return cost_map.get(priority, '$10,000 - $30,000')
    
    def _get_risk_level(self, row) -> str:
        """Assess overall risk level"""
        min_fos = row.get('Min_FoS', row.get('Slope_FoS', 0))
        exceeds_allowable = row.get('Exceeds_Allowable', False)
        
        if min_fos < 1.0 or exceeds_allowable:
            return "VERY HIGH"
        elif min_fos < 1.2:
            return "HIGH"
        elif min_fos < 1.5:
            return "MEDIUM"
        elif min_fos < 2.0:
            return "LOW"
        else:
            return "VERY LOW"


def main():
    """Main execution function with command line interface"""
    
    parser = argparse.ArgumentParser(description="Automated Slope Stability and Pipeline Analysis")
    
    # Analysis configuration
    parser.add_argument("--template", default="Slope Template/uncompressed/SlopeTemplate.xml",
                       help="Path to GeoStudio template XML file")
    parser.add_argument("--excel", default="Soil Springs_2024.xlsx", 
                       help="Path to Soil Springs Excel file")
    parser.add_argument("--output", default="analysis_results",
                       help="Output directory for results")
    parser.add_argument("--limit", type=int, default=None,
                       help="Limit number of configurations (default: use all from parameters)")
    parser.add_argument("--no-plots", action="store_true",
                       help="Skip generating visualization plots")
    
    # Parameter input methods
    param_group = parser.add_mutually_exclusive_group()
    param_group.add_argument("--config-json", type=str,
                           help="Load parameters from JSON file")
    param_group.add_argument("--config-yaml", type=str,
                           help="Load parameters from YAML file")
    param_group.add_argument("--config-excel", type=str,
                           help="Load parameters from Excel file")
    param_group.add_argument("--interactive", action="store_true",
                           help="Interactive parameter input")
    param_group.add_argument("--create-templates", action="store_true",
                           help="Create parameter template files and exit")
    
    # Quick parameter overrides
    parser.add_argument("--angles", type=str,
                       help="Slope angles (comma-separated, e.g., '25,30,35')")
    parser.add_argument("--heights", type=str,
                       help="Slope heights (comma-separated, e.g., '30,50,80')")
    parser.add_argument("--project-name", type=str,
                       help="Project name for analysis")
    
    args = parser.parse_args()
    
    # Handle template creation
    if args.create_templates:
        from parameter_input_system import create_default_config_files
        create_default_config_files()
        print("\n✅ Template files created!")
        print("📝 Edit the templates and use --config-json, --config-yaml, or --config-excel to load them")
        return 0
    
    # Load parameters using the parameter input system
    from parameter_input_system import ParameterInputManager
    param_manager = ParameterInputManager()
    
    if args.interactive:
        print("🎯 Interactive Parameter Input Mode")
        parameters = param_manager.get_parameters_interactive()
    elif args.config_json:
        print(f"📄 Loading parameters from JSON: {args.config_json}")
        parameters = param_manager.load_parameters_from_json(args.config_json)
    elif args.config_yaml:
        print(f"📄 Loading parameters from YAML: {args.config_yaml}")
        parameters = param_manager.load_parameters_from_yaml(args.config_yaml)
    elif args.config_excel:
        print(f"📊 Loading parameters from Excel: {args.config_excel}")
        parameters = param_manager.load_parameters_from_excel(args.config_excel)
    else:
        print("🔧 Using default parameters (create custom config with --create-templates)")
        parameters = param_manager.default_parameters
        
        # Apply command line overrides
        parameters = param_manager.get_parameters_from_args(args)
    
    # Generate configurations from parameters
    print(f"\n🏗️ Generating configurations for: {parameters.project_name}")
    slope_configurations = param_manager.generate_slope_configurations(parameters)
    pipeline_configurations = param_manager.generate_pipeline_configurations(parameters)
    
    print(f"📊 Generated {len(slope_configurations)} slope configurations")
    print(f"🔧 Generated {len(pipeline_configurations)} pipeline configurations")
    
    # Apply limit if specified
    if args.limit:
        slope_configurations = slope_configurations[:args.limit]
        print(f"⚡ Limited to {len(slope_configurations)} slope configurations")
    
    # Initialize workflow
    workflow = AutomatedDecisionWorkflow(
        template_path=args.template,
        excel_path=args.excel,
        output_dir=args.output
    )
    
    try:
        # Run analysis with custom configurations
        print(f"\n🚀 Starting analysis workflow...")
        results = workflow.run_complete_analysis_with_configs(
            slope_configurations=slope_configurations,
            pipeline_configurations=pipeline_configurations,
            generate_plots=not args.no_plots
        )
        
        # Generate configuration recommendations
        recommendations = workflow.generate_configuration_recommendations(results)
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        print(f"Results saved to: {workflow.output_dir}")
        print(f"Configurations analyzed: {len(results) if not results.empty else 0}")
        
        if not results.empty:
            if 'Priority_Level' in results.columns:
                critical = len(results[results['Priority_Level'] == 1])
                high = len(results[results['Priority_Level'] == 2]) 
                print(f"Critical priority: {critical}")
                print(f"High priority: {high}")
            elif 'Analysis_Priority' in results.columns:
                critical = len(results[results['Analysis_Priority'] == 'Critical'])
                high = len(results[results['Analysis_Priority'] == 'High'])
                print(f"Critical priority: {critical}")
                print(f"High priority: {high}")
        
        print(f"Executive summary: {workflow.output_dir}/executive_summary.txt")
        print("="*60)
        
    except Exception as e:
        print(f"Error running analysis workflow: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())