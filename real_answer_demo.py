#!/usr/bin/env python3
"""
Real Answer Demonstration from Stasik Patent Knowledge Base
Shows actual meaningful answers derived from 1,100+ real patents
"""

import json
from collections import defaultdict
import re

def load_patent_data():
    """Load the actual patent data"""
    with open('C:/Knowledge/Patents/FOCUSED_UAS_PATENTS_20250826_070612.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['patents']

def analyze_pitot_tube_patents(patents):
    """Analyze actual pitot tube patents for meaningful insights"""
    
    pitot_keywords = ['pitot', 'airspeed', 'pressure probe', 'air data', 'total pressure', 'static pressure']
    pitot_patents = []
    
    for patent in patents:
        abstract = patent.get('abstract', '').lower()
        title = patent.get('title', '').lower()
        
        if any(keyword in abstract or keyword in title for keyword in pitot_keywords):
            pitot_patents.append(patent)
    
    # Extract real insights
    technologies = []
    advantages = []
    applications = []
    companies = set()
    
    for patent in pitot_patents:
        abstract = patent.get('abstract', '')
        title = patent.get('title', '')
        assignees = patent.get('assignees', [])
        
        # Extract technologies mentioned
        if 'lidar' in abstract.lower():
            technologies.append('LiDAR air data sensors')
        if 'optical' in abstract.lower():
            technologies.append('Optical airspeed measurement')
        if 'time multiplex' in abstract.lower():
            technologies.append('Time-multiplexed optical channels')
        if 'bias' in abstract.lower():
            advantages.append('Systematic bias compensation')
        if 'aircraft' in abstract.lower():
            applications.append('Aircraft systems')
        if 'vehicle' in abstract.lower():
            applications.append('Vehicle applications')
        
        # Extract companies
        for assignee in assignees:
            if assignee:
                companies.add(assignee)
    
    return {
        'total_patents': len(pitot_patents),
        'technologies': list(set(technologies)),
        'advantages': list(set(advantages)),
        'applications': list(set(applications)),
        'key_companies': list(companies),
        'sample_patents': pitot_patents[:3]
    }

def analyze_mems_patents(patents):
    """Analyze actual MEMS patents"""
    
    mems_keywords = ['mems', 'microelectromechanical', 'micro sensor', 'resonator', 'silicon']
    mems_patents = []
    
    for patent in patents:
        abstract = patent.get('abstract', '').lower()
        title = patent.get('title', '').lower()
        
        if any(keyword in abstract or keyword in title for keyword in mems_keywords):
            mems_patents.append(patent)
    
    # Extract insights
    technologies = []
    applications = []
    
    for patent in mems_patents:
        abstract = patent.get('abstract', '')
        
        if 'resonator' in abstract.lower():
            technologies.append('MEMS resonators')
        if 'bulk acoustic' in abstract.lower():
            technologies.append('Bulk acoustic resonators')
        if 'flexural mode' in abstract.lower():
            technologies.append('Flexural mode resonators')
        if 'vibration' in abstract.lower():
            applications.append('Vibration sensing')
    
    return {
        'total_patents': len(mems_patents),
        'technologies': list(set(technologies)),
        'applications': list(set(applications)),
        'sample_patents': mems_patents[:2]
    }

def main():
    """Generate real meaningful answers from patent data"""
    
    print("REAL MEANINGFUL ANSWERS FROM 1,100+ PATENTS")
    print("=" * 80)
    print()
    
    # Load actual patent data
    patents = load_patent_data()
    print(f"Loaded {len(patents)} real patents from knowledge base")
    print()
    
    # Question 1: Pitot tube advantages
    print("Q1: What are the key advantages of pitot tubes for UAV airspeed measurement?")
    print("-" * 70)
    
    pitot_analysis = analyze_pitot_tube_patents(patents)
    
    print("REAL ANSWER FROM PATENT ANALYSIS:")
    print()
    print(f"Found {pitot_analysis['total_patents']} relevant patents in airspeed sensing")
    print()
    print("Technologies Identified:")
    for tech in pitot_analysis['technologies']:
        print(f"  • {tech}")
    print()
    print("Key Advantages from Patents:")
    for adv in pitot_analysis['advantages']:
        print(f"  • {adv}")
    print()
    print("Applications:")
    for app in pitot_analysis['applications']:
        print(f"  • {app}")
    print()
    print("Leading Companies:")
    for company in pitot_analysis['key_companies'][:3]:
        print(f"  • {company}")
    print()
    
    # Show actual patent example
    if pitot_analysis['sample_patents']:
        patent = pitot_analysis['sample_patents'][0]
        print("REAL PATENT EXAMPLE:")
        print(f"Title: {patent.get('title')}")
        print(f"Abstract: {patent.get('abstract')[:300]}...")
        print(f"Assignee: {patent.get('assignees', ['N/A'])[0] if patent.get('assignees') else 'N/A'}")
    print()
    print("=" * 80)
    print()
    
    # Question 2: MEMS sensors
    print("Q2: What MEMS airflow sensing technologies are available?")
    print("-" * 70)
    
    mems_analysis = analyze_mems_patents(patents)
    
    print("REAL ANSWER FROM PATENT ANALYSIS:")
    print()
    print(f"Found {mems_analysis['total_patents']} relevant MEMS patents")
    print()
    print("MEMS Technologies:")
    for tech in mems_analysis['technologies']:
        print(f"  • {tech}")
    print()
    print("Applications:")
    for app in mems_analysis['applications']:
        print(f"  • {app}")
    print()
    
    # Show MEMS patent example
    if mems_analysis['sample_patents']:
        patent = mems_analysis['sample_patents'][0]
        print("REAL MEMS PATENT EXAMPLE:")
        print(f"Title: {patent.get('title')}")
        print(f"Abstract: {patent.get('abstract')[:300]}...")
    print()
    
    print("=" * 80)
    print("These answers are derived from analyzing actual patent abstracts,")
    print("titles, assignees, and technical content from the knowledge base!")
    print("=" * 80)

if __name__ == "__main__":
    main()