#!/usr/bin/env python3
"""
Environment Setup Script
Automatically installs required dependencies and checks system capabilities.
"""

import subprocess
import sys
from pathlib import Path
import logging


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher required")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
        return True


def install_package(package_name, description=""):
    """Install a Python package with pip"""
    try:
        print(f"📦 Installing {package_name}... {description}")
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], 
                      check=True, capture_output=True)
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False


def check_package_availability(package_name, import_name=None):
    """Check if a package is available"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} is available")
        return True
    except ImportError:
        print(f"❌ {package_name} not available")
        return False


def install_core_dependencies():
    """Install core required dependencies"""
    
    print("\n=== Installing Core Dependencies ===")
    
    core_packages = [
        ("pandas", "Data manipulation and analysis"),
        ("numpy", "Numerical computing"),
        ("matplotlib", "Plotting and visualization"),
        ("seaborn", "Statistical data visualization"),
        ("openpyxl", "Excel file handling"),
        ("xlwings", "Excel automation")
    ]
    
    success_count = 0
    
    for package, description in core_packages:
        if install_package(package, description):
            success_count += 1
    
    print(f"\n📊 Core Dependencies: {success_count}/{len(core_packages)} installed")
    return success_count == len(core_packages)


def install_enhanced_dependencies():
    """Install enhanced optional dependencies"""
    
    print("\n=== Installing Enhanced Dependencies ===")
    
    enhanced_packages = [
        ("PyGeoStudio", "Direct GeoStudio .gsz file manipulation (HIGHLY RECOMMENDED)")
    ]
    
    success_count = 0
    
    for package, description in enhanced_packages:
        if install_package(package, description):
            success_count += 1
        else:
            print(f"⚠️  {package} installation failed - will use fallback methods")
    
    print(f"\n📊 Enhanced Dependencies: {success_count}/{len(enhanced_packages)} installed")
    return success_count > 0


def check_system_capabilities():
    """Check what analysis capabilities are available"""
    
    print("\n=== System Capabilities Check ===")
    
    capabilities = {
        "Excel Processing": False,
        "Plotting": False,
        "Data Analysis": False,
        "PyGeoStudio Integration": False,
        "GeoStudio CLI": False
    }
    
    # Check Excel capabilities
    if check_package_availability("xlwings"):
        capabilities["Excel Processing"] = True
    
    # Check plotting
    if check_package_availability("matplotlib") and check_package_availability("seaborn"):
        capabilities["Plotting"] = True
    
    # Check data analysis
    if check_package_availability("pandas") and check_package_availability("numpy"):
        capabilities["Data Analysis"] = True
    
    # Check PyGeoStudio
    if check_package_availability("PyGeoStudio", "pygeostudio"):
        capabilities["PyGeoStudio Integration"] = True
    
    # Check for GeoStudio installation (simplified check)
    geostudio_paths = [
        "C:\\Program Files\\GeoSlope",
        "C:\\Program Files (x86)\\GeoSlope"
    ]
    
    for path in geostudio_paths:
        if Path(path).exists():
            capabilities["GeoStudio CLI"] = True
            break
    
    # Print capabilities summary
    print("\n📋 System Capabilities Summary:")
    for capability, available in capabilities.items():
        status = "✅" if available else "❌"
        print(f"  {status} {capability}")
    
    return capabilities


def create_config_file(capabilities):
    """Create configuration file based on system capabilities"""
    
    config = {
        "excel_headless": capabilities["Excel Processing"],
        "use_pygeostudio": capabilities["PyGeoStudio Integration"],
        "enable_plotting": capabilities["Plotting"],
        "geostudio_available": capabilities["GeoStudio CLI"]
    }
    
    config_file = Path("system_config.json")
    
    try:
        import json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n💾 Configuration saved to {config_file}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False


def run_test_analysis():
    """Run a quick test to verify installation"""
    
    print("\n=== Running Test Analysis ===")
    
    try:
        # Test basic imports
        import pandas as pd
        import numpy as np
        print("✅ Core libraries imported successfully")
        
        # Test Excel capabilities
        try:
            import xlwings as xw
            print("✅ Excel automation available")
        except ImportError:
            print("⚠️  Excel automation not available")
        
        # Test PyGeoStudio
        try:
            import pygeostudio as pgs
            print("✅ PyGeoStudio integration available")
        except ImportError:
            print("⚠️  PyGeoStudio not available - will use fallback methods")
        
        # Test plotting
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            print("✅ Plotting capabilities available")
        except ImportError:
            print("⚠️  Plotting not available")
        
        print("\n🎉 Basic system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False


def main():
    """Main setup function"""
    
    print("🚀 EMPCO Slope Stability Analysis - Environment Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install core dependencies
    if not install_core_dependencies():
        print("\n❌ Failed to install core dependencies")
        sys.exit(1)
    
    # Install enhanced dependencies (optional)
    install_enhanced_dependencies()
    
    # Check system capabilities
    capabilities = check_system_capabilities()
    
    # Create configuration file
    create_config_file(capabilities)
    
    # Run test analysis
    if run_test_analysis():
        print("\n🎉 Setup completed successfully!")
        print("\n📚 Next Steps:")
        print("1. Run: python automated_decision_workflow.py --limit 10")
        print("2. Check the analysis_results/ directory for outputs")
        print("3. Review README.md for detailed usage instructions")
        
        if capabilities["PyGeoStudio Integration"]:
            print("\n🔥 PyGeoStudio detected - you have full GeoStudio integration!")
        else:
            print("\n💡 Install PyGeoStudio for enhanced capabilities:")
            print("   pip install PyGeoStudio")
    
    else:
        print("\n❌ Setup encountered issues - check error messages above")
        sys.exit(1)


if __name__ == "__main__":
    main()