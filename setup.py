#!/usr/bin/env python3
"""
Setup script for Stasik UAV Airflow Sensing Knowledge Agent
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Stasik: UAV Airflow Sensing Knowledge Agent"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="stasik-agent",
    version="1.0.0",
    author="Eugene Nayshtetik",
    author_email="e.nayshtetik@example.com",
    description="Advanced AI Knowledge Agent for UAV Airflow Sensing Technologies",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/stasik-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.900',
        ],
        'docs': [
            'sphinx>=4.0',
            'sphinx-rtd-theme>=1.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'stasik=stasik_agent:main',
        ],
    },
    include_package_data=True,
    package_data={
        'stasik_agent': ['knowledge_base/*.json', 'data/*.csv', 'docs/*.md'],
    },
    keywords=[
        "UAV", "drone", "airflow", "sensing", "sensors", "pitot", "anemometer", 
        "MEMS", "multi-hole probe", "ArduPilot", "PX4", "knowledge agent", "AI"
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/stasik-agent/issues",
        "Documentation": "https://github.com/yourusername/stasik-agent/wiki",
        "Source": "https://github.com/yourusername/stasik-agent",
    },
)