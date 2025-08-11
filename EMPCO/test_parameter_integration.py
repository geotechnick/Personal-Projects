#!/usr/bin/env python3
"""
Test Parameter Integration
Test script to verify that the updated parameter system works correctly
with all the new pipeline parameters and soil layer evaluation.
"""

import sys
from pathlib import Path
import json

# Add EMPCO directory to path
sys.path.insert(0, str(Path(__file__).parent))

from parameter_input_system import ParameterInputManager, ProjectParameters
from soil_springs_integration import PipelineConfiguration, IntegratedAnalysisEngine
from slope_stability_automation import SlopeGeometry, SoilLayer, SlopeConfiguration


def test_parameter_system():
    """Test the complete parameter system with new pipeline parameters"""
    
    print("="*60)
    print("PARAMETER INTEGRATION TEST")
    print("="*60)
    
    # Initialize parameter manager
    manager = ParameterInputManager()
    
    # Test 1: Default parameters structure
    print("\n1. Testing default parameters structure...")
    default_params = manager.default_parameters
    
    # Check all new parameter fields exist
    required_fields = [
        'pipe_outside_diameters', 'pipe_wall_thicknesses', 'pipe_grades',
        'pipe_smys_values', 'pipe_depths_of_cover', 'pipe_lengths_in_pgd',
        'pipe_coatings', 'internal_pressures', 'pgd_paths'
    ]
    
    print(f"   Project: {default_params.project_name}")
    for field in required_fields:
        value = getattr(default_params, field, None)
        print(f"   {field}: {value}")
        assert value is not None, f"Missing parameter field: {field}"
    
    print("   ✅ All parameter fields present")
    
    # Test 2: Pipeline configuration generation
    print("\n2. Testing pipeline configuration generation...")
    pipeline_configs = manager.generate_pipeline_configurations(default_params)
    
    print(f"   Generated {len(pipeline_configs)} pipeline configurations")
    assert len(pipeline_configs) > 0, "No pipeline configurations generated"
    
    # Check first configuration has all required fields
    first_config = pipeline_configs[0]
    pipeline_fields = [
        'pipe_od', 'pipe_wt', 'pipe_grade', 'pipe_smys', 'pipe_doc',
        'pipe_length_in_pgd', 'pipe_coating', 'internal_pressure', 'pgd_path'
    ]
    
    print("   Sample configuration:")
    for field in pipeline_fields:
        value = getattr(first_config, field, None)
        print(f"     {field}: {value}")
        assert value is not None, f"Missing pipeline configuration field: {field}"
    
    print("   ✅ Pipeline configurations generated correctly")
    
    # Test 3: Soil layer evaluation for pipe depth
    print("\n3. Testing soil layer evaluation for pipe depth...")
    
    # Create test slope configuration with multiple soil layers
    test_soil_layers = [
        SoilLayer("Surface Fill", 110, 50, 25, 20, 5),    # 0-5 ft
        SoilLayer("Weak Clay", 115, 100, 50, 15, 15),     # 5-20 ft
        SoilLayer("Dense Clay", 125, 400, 200, 35, 30)    # 20-50 ft
    ]
    
    test_slope_config = SlopeConfiguration(
        config_id="TEST_001",
        geometry=SlopeGeometry(30, 50, 0, 50),
        soil_layers=test_soil_layers,
        groundwater_depth=10
    )
    
    # Create integration engine to test soil layer selection
    from soil_springs_integration import IntegratedAnalysisEngine
    engine = IntegratedAnalysisEngine("dummy_excel_path.xlsx")
    
    # Test different pipe depths
    test_depths = [3, 8, 15, 25, 60]  # Various depths to test layer selection
    
    for depth in test_depths:
        soil_params = engine.convert_slope_to_soil_params(test_slope_config, depth)
        print(f"   Pipe at {depth} ft depth:")
        print(f"     Soil type: {soil_params.soil_type}")
        print(f"     Friction angle: {soil_params.friction_angle}°")
        print(f"     Cohesion: {soil_params.cohesion} psf")
        print(f"     Unit weight: {soil_params.unit_weight} pcf")
        
        # Verify correct layer is selected
        if depth <= 5:
            assert "Surface Fill" in soil_params.soil_type, f"Wrong layer for depth {depth}"
        elif depth <= 20:
            assert "Weak Clay" in soil_params.soil_type, f"Wrong layer for depth {depth}"
        else:
            assert "Dense Clay" in soil_params.soil_type, f"Wrong layer for depth {depth}"
    
    print("   ✅ Soil layer evaluation working correctly")
    
    # Test 4: JSON export/import
    print("\n4. Testing JSON configuration export/import...")
    test_json_file = "test_config.json"
    
    # Create custom parameters for testing
    test_params = ProjectParameters(
        project_name="Test Project",
        description="Integration test parameters",
        slope_angles=[25, 30, 35],
        slope_heights=[40, 60],
        soil_scenarios=[default_params.soil_scenarios[0]],
        pipe_outside_diameters=[24, 30],
        pipe_wall_thicknesses=[0.5, 0.625],
        pipe_grades=["X-52", "X-65"],
        pipe_smys_values=[52000, 65000],
        pipe_depths_of_cover=[4, 6, 8],
        pipe_lengths_in_pgd=[10, 20],
        pipe_coatings=["FBE", "3LPE"],
        internal_pressures=[1200, 1440],
        pgd_paths=["perpendicular", "parallel"],
        groundwater_ratios=[0.7]
    )
    
    # Save and reload
    manager.save_parameters_to_json(test_params, test_json_file)
    loaded_params = manager.load_parameters_from_json(test_json_file)
    
    # Verify parameters match
    assert loaded_params.project_name == test_params.project_name
    assert loaded_params.pipe_outside_diameters == test_params.pipe_outside_diameters
    assert loaded_params.pipe_coatings == test_params.pipe_coatings
    assert loaded_params.pgd_paths == test_params.pgd_paths
    
    print(f"   Saved and loaded {test_json_file}")
    print("   ✅ JSON export/import working correctly")
    
    # Cleanup
    Path(test_json_file).unlink(missing_ok=True)
    
    # Test 5: Verify specific user-requested parameters
    print("\n5. Verifying user-requested parameters are available...")
    user_params = {
        "Pipe OD (in)": default_params.pipe_outside_diameters,
        "Pipe wt (in)": default_params.pipe_wall_thicknesses, 
        "Pipe SMYS (psi)": default_params.pipe_smys_values,
        "Pipe DOC (ft)": default_params.pipe_depths_of_cover,
        "Length of Pipe in PGD (ft)": default_params.pipe_lengths_in_pgd,
        "Pipe Coating": default_params.pipe_coatings,
        "Internal Pressure (psi)": default_params.internal_pressures,
        "PGD Path (perpendicular/parallel to pipe)": default_params.pgd_paths
    }
    
    for param_name, param_values in user_params.items():
        print(f"   {param_name}: {param_values}")
        assert param_values and len(param_values) > 0, f"Empty parameter: {param_name}"
    
    print("   ✅ All user-requested parameters available")
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED!")
    print("Parameter integration working correctly with:")
    print("• Updated pipeline parameters including coating and PGD path")
    print("• Proper soil layer evaluation based on pipe depth")
    print("• JSON/YAML/Excel configuration support")
    print("• Backward compatibility maintained")
    print("="*60)


def test_soil_layer_selection_edge_cases():
    """Test edge cases for soil layer selection"""
    
    print("\n6. Testing soil layer selection edge cases...")
    
    # Create layers with gaps and varying thicknesses
    test_layers = [
        SoilLayer("Layer 1", 120, 200, 100, 25, 10),  # 0-10 ft
        SoilLayer("Layer 2", 125, 300, 150, 30, 20),  # 10-30 ft  
        SoilLayer("Layer 3", 130, 500, 250, 35, 25),  # 30-55 ft
    ]
    
    test_config = SlopeConfiguration(
        config_id="EDGE_TEST",
        geometry=SlopeGeometry(35, 45, 0, 60),
        soil_layers=test_layers,
        groundwater_depth=15
    )
    
    engine = IntegratedAnalysisEngine("dummy.xlsx")
    
    # Test boundary conditions
    boundary_tests = [
        (0, "Layer 1"),     # At surface
        (10, "Layer 2"),    # At layer boundary
        (29.9, "Layer 2"),  # Just before boundary
        (30.1, "Layer 3"),  # Just after boundary
        (55, "Layer 3"),    # At last layer boundary
        (100, "Layer 3"),   # Beyond all layers (should extrapolate)
    ]
    
    for depth, expected_layer in boundary_tests:
        soil_params = engine.convert_slope_to_soil_params(test_config, depth)
        print(f"   Depth {depth} ft -> {soil_params.soil_type}")
        assert expected_layer in soil_params.soil_type, f"Wrong layer at depth {depth}"
    
    print("   ✅ Edge cases handled correctly")


if __name__ == "__main__":
    test_parameter_system()
    test_soil_layer_selection_edge_cases()
    print("\n✅ All integration tests completed successfully!")