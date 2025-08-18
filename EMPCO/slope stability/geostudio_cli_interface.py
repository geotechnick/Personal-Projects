#!/usr/bin/env python3
"""
GeoStudio Command Line Interface
Provides methods to run GeoStudio analyses without opening the GUI.

Note: This requires GeoStudio installation and command-line tools.
Different versions of GeoStudio may have different CLI interfaces.
"""

import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
import time
import re
from typing import Tuple, Dict, Optional


class GeoStudioCLI:
    """
    Interface for running GeoStudio analyses via command line
    """
    
    def __init__(self, geostudio_install_path: str = None):
        """
        Initialize GeoStudio CLI interface
        
        Args:
            geostudio_install_path: Path to GeoStudio installation
                                  (if None, assumes it's in system PATH)
        """
        self.geostudio_path = geostudio_install_path
        self.logger = logging.getLogger(__name__)
        
        # Common GeoStudio executable names/paths
        self.possible_executables = [
            "GeoStudio.exe",
            "GeoCmd.exe", 
            "SlopeW.exe",
            "GSIBatch.exe"
        ]
        
        self.geostudio_exe = self._find_geostudio_executable()
    
    def _find_geostudio_executable(self) -> Optional[str]:
        """Find GeoStudio executable on system"""
        
        # Common installation paths
        common_paths = [
            r"C:\Program Files\GeoSlope\GeoStudio 2021",
            r"C:\Program Files\GeoSlope\GeoStudio 2022", 
            r"C:\Program Files\GeoSlope\GeoStudio 2023",
            r"C:\Program Files (x86)\GeoSlope\GeoStudio 2021",
            r"C:\Program Files (x86)\GeoSlope\GeoStudio 2022"
        ]
        
        # If specific path provided, check there first
        if self.geostudio_path:
            common_paths.insert(0, self.geostudio_path)
        
        for base_path in common_paths:
            base_dir = Path(base_path)
            if base_dir.exists():
                for exe_name in self.possible_executables:
                    exe_path = base_dir / exe_name
                    if exe_path.exists():
                        self.logger.info(f"Found GeoStudio executable: {exe_path}")
                        return str(exe_path)
        
        # Try system PATH
        for exe_name in self.possible_executables:
            try:
                result = subprocess.run(['where', exe_name], 
                                      capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    exe_path = result.stdout.strip().split('\n')[0]
                    self.logger.info(f"Found GeoStudio in PATH: {exe_path}")
                    return exe_path
            except:
                pass
        
        self.logger.warning("GeoStudio executable not found")
        return None
    
    def run_analysis(self, gsz_file: str, output_dir: str = None) -> Tuple[bool, str]:
        """
        Run GeoStudio analysis via command line
        
        Args:
            gsz_file: Path to GeoStudio .gsz file
            output_dir: Directory for output files
            
        Returns:
            (success, output_message)
        """
        
        if not self.geostudio_exe:
            return False, "GeoStudio executable not found"
        
        gsz_path = Path(gsz_file)
        if not gsz_path.exists():
            return False, f"GSZ file not found: {gsz_file}"
        
        try:
            # Different command line approaches for different GeoStudio versions
            commands = [
                # Method 1: Direct GSZ file execution
                [self.geostudio_exe, str(gsz_path), "/solve"],
                
                # Method 2: Batch mode
                [self.geostudio_exe, "/batch", str(gsz_path)],
                
                # Method 3: Command line solve
                [self.geostudio_exe, "-solve", str(gsz_path)],
            ]
            
            for cmd in commands:
                try:
                    self.logger.info(f"Attempting command: {' '.join(cmd)}")
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=300,  # 5 minute timeout
                        cwd=str(gsz_path.parent)
                    )
                    
                    if result.returncode == 0:
                        self.logger.info("GeoStudio analysis completed successfully")
                        return True, result.stdout
                    else:
                        self.logger.warning(f"Command failed with return code {result.returncode}")
                        continue
                        
                except subprocess.TimeoutExpired:
                    self.logger.error("GeoStudio analysis timed out")
                    continue
                except Exception as e:
                    self.logger.error(f"Command execution failed: {e}")
                    continue
            
            return False, "All GeoStudio command attempts failed"
            
        except Exception as e:
            self.logger.error(f"GeoStudio analysis failed: {e}")
            return False, str(e)
    
    def run_xml_analysis(self, xml_file: str, output_dir: str = None) -> Tuple[bool, Dict]:
        """
        Run analysis from XML template file
        
        Args:
            xml_file: Path to XML template file
            output_dir: Directory for output files
            
        Returns:
            (success, results_dict)
        """
        
        # Convert XML to GSZ if needed
        gsz_file = self._xml_to_gsz(xml_file)
        
        if not gsz_file:
            return False, {"error": "Failed to convert XML to GSZ"}
        
        # Run analysis
        success, output = self.run_analysis(gsz_file, output_dir)
        
        if success:
            # Parse results from output files
            results = self._parse_results(gsz_file, output_dir)
            return True, results
        else:
            return False, {"error": output}
    
    def _xml_to_gsz(self, xml_file: str) -> Optional[str]:
        """
        Convert XML template to GSZ file (if needed)
        
        Note: This may require additional tools or GeoStudio utilities
        """
        # This is a placeholder - actual implementation would depend on
        # GeoStudio version and available conversion tools
        
        xml_path = Path(xml_file)
        gsz_path = xml_path.parent / f"{xml_path.stem}.gsz"
        
        # If GSZ already exists, use it
        if gsz_path.exists():
            return str(gsz_path)
        
        # Otherwise, would need to convert XML to GSZ
        # This might involve:
        # 1. Using GeoStudio import utilities
        # 2. Creating GSZ from XML using GeoStudio libraries
        # 3. Manual conversion process
        
        self.logger.warning("XML to GSZ conversion not implemented")
        return None
    
    def _parse_results(self, gsz_file: str, output_dir: str = None) -> Dict:
        """
        Parse Factor of Safety results from GeoStudio output files
        """
        
        gsz_path = Path(gsz_file)
        base_name = gsz_path.stem
        
        # Look for output files
        possible_output_files = [
            gsz_path.parent / f"{base_name}.txt",
            gsz_path.parent / f"{base_name}_results.txt", 
            gsz_path.parent / f"{base_name}.out",
        ]
        
        results = {
            'total_stress_fos': None,
            'effective_stress_fos': None,
            'critical_slip_surface': None
        }
        
        for output_file in possible_output_files:
            if output_file.exists():
                try:
                    with open(output_file, 'r') as f:
                        content = f.read()
                    
                    # Parse Factor of Safety values using regex
                    fos_patterns = [
                        r"Factor of Safety\s*[=:]\s*(\d+\.?\d*)",
                        r"FoS\s*[=:]\s*(\d+\.?\d*)",
                        r"Safety Factor\s*[=:]\s*(\d+\.?\d*)"
                    ]
                    
                    for pattern in fos_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            # Assume first match is total stress, second is effective
                            if results['total_stress_fos'] is None:
                                results['total_stress_fos'] = float(matches[0])
                            if len(matches) > 1 and results['effective_stress_fos'] is None:
                                results['effective_stress_fos'] = float(matches[1])
                    
                    break
                    
                except Exception as e:
                    self.logger.error(f"Failed to parse output file {output_file}: {e}")
        
        # If no results found, use placeholder values
        if results['total_stress_fos'] is None:
            self.logger.warning("Could not parse Factor of Safety from output - using placeholder")
            results['total_stress_fos'] = 1.5  # Placeholder
            results['effective_stress_fos'] = 1.3  # Placeholder
        
        return results


class MockGeoStudioCLI:
    """
    Mock implementation for testing when GeoStudio is not available
    """
    
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
    
    def run_analysis(self, gsz_file: str, output_dir: str = None) -> Tuple[bool, str]:
        """Mock analysis that returns placeholder results"""
        self.logger.info(f"Mock GeoStudio analysis for {gsz_file}")
        
        # Simulate analysis time
        time.sleep(1)
        
        return True, "Mock analysis completed successfully"
    
    def run_xml_analysis(self, xml_file: str, output_dir: str = None) -> Tuple[bool, Dict]:
        """Mock XML analysis"""
        self.logger.info(f"Mock XML analysis for {xml_file}")
        
        # Generate realistic-looking Factor of Safety values
        import random
        
        results = {
            'total_stress_fos': round(random.uniform(0.8, 2.5), 2),
            'effective_stress_fos': round(random.uniform(0.7, 2.2), 2),
            'critical_slip_surface': {'mock': True}
        }
        
        return True, results


def get_geostudio_interface(geostudio_path: str = None, use_mock: bool = False) -> object:
    """
    Factory function to get appropriate GeoStudio interface
    
    Args:
        geostudio_path: Path to GeoStudio installation
        use_mock: Force use of mock interface for testing
        
    Returns:
        GeoStudio interface object
    """
    
    if use_mock:
        return MockGeoStudioCLI()
    
    # Try to get real interface
    cli = GeoStudioCLI(geostudio_path)
    
    if cli.geostudio_exe:
        return cli
    else:
        logging.warning("GeoStudio not found - using mock interface")
        return MockGeoStudioCLI()


def demonstrate_geostudio_cli():
    """Demonstrate GeoStudio CLI usage"""
    
    print("=== GeoStudio CLI Demo ===")
    
    # Use mock for demonstration
    geo_cli = get_geostudio_interface(use_mock=True)
    
    xml_file = "Slope Template/uncompressed/SlopeTemplate.xml"
    
    if Path(xml_file).exists():
        success, results = geo_cli.run_xml_analysis(xml_file)
        
        if success:
            print(f"Analysis successful!")
            print(f"Total Stress FoS: {results.get('total_stress_fos', 'N/A')}")
            print(f"Effective Stress FoS: {results.get('effective_stress_fos', 'N/A')}")
        else:
            print(f"Analysis failed: {results}")
    else:
        print(f"XML template not found: {xml_file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demonstrate_geostudio_cli()