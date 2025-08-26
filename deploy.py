#!/usr/bin/env python3
"""
Stasik Agent Deployment Script
Automated deployment and setup utility
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, description=""):
    """Run shell command with error handling"""
    print(f"Running: {description or command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ Success: {description or command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {description or command}")
        print(f"  Error message: {e.stderr}")
        return None

def check_requirements():
    """Check system requirements"""
    print("=== Checking System Requirements ===")
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro} (compatible)")
    else:
        print(f"✗ Python {python_version.major}.{python_version.minor}.{python_version.micro} (requires 3.8+)")
        return False
    
    # Check git
    if run_command("git --version", "Check Git installation"):
        print("✓ Git is available")
    else:
        print("✗ Git is required but not found")
        return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n=== Installing Dependencies ===")
    
    # Upgrade pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrade pip")
    
    # Install requirements
    if Path("requirements.txt").exists():
        run_command(f"{sys.executable} -m pip install -r requirements.txt", "Install requirements")
    
    # Install package in development mode
    run_command(f"{sys.executable} -m pip install -e .", "Install Stasik Agent (development mode)")

def setup_directories():
    """Create necessary directories"""
    print("\n=== Setting Up Directory Structure ===")
    
    directories = [
        "logs",
        "temp", 
        "knowledge_base",
        "data",
        "data/temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def validate_installation():
    """Validate the installation"""
    print("\n=== Validating Installation ===")
    
    try:
        # Test import
        import stasik_agent
        agent = stasik_agent.StasikAgent()
        info = agent.get_agent_info()
        
        print(f"✓ Stasik Agent {info['version']} loaded successfully")
        print(f"  Domain: {info['domain']}")
        print(f"  Status: {info['status']}")
        
        # Test basic functionality
        result = agent.query_technology("pitot_tubes", "overview")
        if result["status"] == "success":
            print("✓ Basic functionality test passed")
        else:
            print("⚠ Basic functionality test returned warnings")
        
        return True
        
    except Exception as e:
        print(f"✗ Installation validation failed: {e}")
        return False

def run_tests():
    """Run the test suite"""
    print("\n=== Running Test Suite ===")
    
    if Path("tests").exists():
        result = run_command(f"{sys.executable} -m pytest tests/ -v", "Run test suite")
        if result:
            print("✓ Test suite completed")
        else:
            print("⚠ Some tests may have failed - check output above")
    else:
        print("⚠ No tests directory found")

def main():
    """Main deployment process"""
    print("╔═══════════════════════════════════════════════╗")
    print("║         Stasik Agent Deployment Script       ║")
    print("║    UAV Airflow Sensing Knowledge Agent       ║")
    print("╚═══════════════════════════════════════════════╝\n")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print(f"Working directory: {script_dir}")
    
    steps = [
        ("System Requirements Check", check_requirements),
        ("Directory Setup", setup_directories),
        ("Dependencies Installation", install_dependencies),
        ("Installation Validation", validate_installation),
        ("Test Suite", run_tests)
    ]
    
    success_count = 0
    for step_name, step_function in steps:
        try:
            if step_function():
                success_count += 1
            else:
                print(f"\n⚠ {step_name} completed with warnings")
        except Exception as e:
            print(f"\n✗ {step_name} failed: {e}")
    
    print(f"\n{'='*50}")
    print(f"Deployment Summary: {success_count}/{len(steps)} steps successful")
    
    if success_count == len(steps):
        print("🎉 Stasik Agent deployed successfully!")
        print("\nUsage:")
        print("  python -c \"from stasik_agent import StasikAgent; agent = StasikAgent(); print(agent.get_agent_info())\"")
    else:
        print("⚠ Deployment completed with some issues - see output above")
    
    print(f"{'='*50}")

if __name__ == "__main__":
    main()