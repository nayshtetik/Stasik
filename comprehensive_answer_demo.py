#!/usr/bin/env python3
"""
Comprehensive Meaningful Answers from 1,100+ Real Patents
Advanced analysis showing detailed technical insights
"""

import json
import re
from collections import defaultdict, Counter

def load_patent_data():
    """Load the actual patent data"""
    with open('C:/Knowledge/Patents/FOCUSED_UAS_PATENTS_20250826_070612.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def analyze_comprehensive_airflow_sensing(patents):
    """Comprehensive analysis of all airflow sensing technologies"""
    
    # Technology categories with keywords
    tech_categories = {
        'Pressure Sensors': ['pressure', 'pitot', 'static pressure', 'differential pressure'],
        'Optical Sensors': ['optical', 'lidar', 'laser', 'interferometer'],
        'MEMS Sensors': ['mems', 'microelectromechanical', 'resonator', 'micro sensor'],
        'Thermal Sensors': ['thermal', 'temperature', 'heat transfer', 'calorimetric'],
        'Ultrasonic Sensors': ['ultrasonic', 'acoustic', 'sound wave'],
        'Flow Sensors': ['flow', 'velocity', 'airspeed', 'wind speed'],
        'Multi-hole Probes': ['multi-hole', '5-hole', 'probe array', 'directional'],
        'Anemometry': ['anemometer', 'wind measurement', 'meteorological']
    }
    
    # Analysis results
    results = defaultdict(list)
    year_trends = defaultdict(int)
    company_analysis = defaultdict(int)
    keyword_frequency = Counter()
    
    for patent in patents:
        abstract = patent.get('abstract', '').lower()
        title = patent.get('title', '').lower()
        year = patent.get('publication_date', '')[:4] if patent.get('publication_date') else 'unknown'
        assignees = patent.get('assignees', [])
        
        # Count year trends
        if year != 'unknown' and year.isdigit():
            year_trends[year] += 1
        
        # Count companies
        for assignee in assignees:
            if assignee:
                company_analysis[assignee] += 1
        
        # Analyze by technology category
        full_text = abstract + ' ' + title
        
        for category, keywords in tech_categories.items():
            if any(keyword in full_text for keyword in keywords):
                results[category].append({
                    'title': patent.get('title'),
                    'abstract': patent.get('abstract')[:200] + '...',
                    'year': year,
                    'assignees': assignees
                })
        
        # Extract technical keywords
        technical_words = re.findall(r'\b(?:sensor|measurement|detection|calibration|accuracy|precision|system|device|method|apparatus)\b', full_text)
        keyword_frequency.update(technical_words)
    
    return results, year_trends, company_analysis, keyword_frequency

def analyze_uav_specific_content(patents):
    """Analyze UAV/drone specific applications"""
    
    uav_keywords = ['uav', 'drone', 'unmanned', 'aircraft', 'aerial', 'flight', 'aviation', 'aerospace']
    uav_patents = []
    applications = Counter()
    
    for patent in patents:
        abstract = patent.get('abstract', '').lower()
        title = patent.get('title', '').lower()
        full_text = abstract + ' ' + title
        
        if any(keyword in full_text for keyword in uav_keywords):
            uav_patents.append(patent)
            
            # Extract applications
            if 'navigation' in full_text:
                applications['Navigation systems'] += 1
            if 'control' in full_text:
                applications['Flight control'] += 1
            if 'monitoring' in full_text:
                applications['System monitoring'] += 1
            if 'autopilot' in full_text:
                applications['Autopilot systems'] += 1
    
    return uav_patents, applications

def main():
    """Generate comprehensive meaningful answers"""
    
    print("COMPREHENSIVE MEANINGFUL ANSWERS FROM REAL PATENT ANALYSIS")
    print("=" * 80)
    print()
    
    # Load data
    data = load_patent_data()
    patents = data['patents']
    metadata = data['collection_metadata']
    
    print(f"Knowledge Base: {metadata['total_patents']} authentic patents")
    print(f"Collection Date: {metadata['collection_date']}")
    print(f"UAS Relevant: {metadata['uas_relevant_patents']} ({metadata['uas_relevance_percentage']:.1f}%)")
    print(f"Date Range: {metadata['date_range']}")
    print()
    
    # Comprehensive technology analysis
    tech_results, year_trends, companies, keywords = analyze_comprehensive_airflow_sensing(patents)
    
    print("QUESTION: What airflow sensing technologies are represented in the patent database?")
    print("-" * 70)
    print("COMPREHENSIVE ANSWER FROM PATENT ANALYSIS:")
    print()
    
    for category, patents_in_category in tech_results.items():
        if patents_in_category:  # Only show categories with patents
            print(f"{category}: {len(patents_in_category)} patents")
            
            # Show recent developments
            recent_patents = [p for p in patents_in_category if p['year'].isdigit() and int(p['year']) >= 2020]
            if recent_patents:
                latest = max(recent_patents, key=lambda x: x['year'] if x['year'].isdigit() else '0')
                print(f"  Latest Development ({latest['year']}): {latest['title']}")
                print(f"  Description: {latest['abstract']}")
                if latest['assignees']:
                    print(f"  Company: {latest['assignees'][0]}")
            print()
    
    print("=" * 80)
    print()
    
    # Patent timeline analysis
    print("QUESTION: What are the innovation trends in airflow sensing?")
    print("-" * 70)
    print("TIMELINE ANALYSIS:")
    print()
    
    # Show year trends for recent years
    recent_years = sorted([year for year in year_trends.keys() if year.isdigit() and int(year) >= 2020])
    if recent_years:
        print("Recent Patent Activity:")
        for year in recent_years[-5:]:  # Last 5 years
            print(f"  {year}: {year_trends[year]} patents")
    print()
    
    # Top companies
    top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Leading Organizations:")
    for company, count in top_companies:
        if count > 1:  # Only show companies with multiple patents
            print(f"  {company}: {count} patents")
    print()
    
    print("=" * 80)
    print()
    
    # UAV-specific analysis
    uav_patents, uav_apps = analyze_uav_specific_content(patents)
    
    print("QUESTION: What UAV-specific airflow sensing applications are covered?")
    print("-" * 70)
    print("UAV-SPECIFIC ANALYSIS:")
    print()
    print(f"UAV-related patents: {len(uav_patents)}")
    print()
    
    if uav_apps:
        print("Applications:")
        for app, count in uav_apps.most_common(5):
            print(f"  • {app}: {count} patents")
    print()
    
    # Show specific UAV patent examples
    if uav_patents:
        print("REAL UAV PATENT EXAMPLES:")
        for i, patent in enumerate(uav_patents[:2]):
            print(f"{i+1}. {patent.get('title')}")
            print(f"   Abstract: {patent.get('abstract', '')[:250]}...")
            if patent.get('assignees'):
                print(f"   Company: {patent.get('assignees')[0]}")
            print()
    
    print("=" * 80)
    print()
    
    # Technical keyword analysis
    print("QUESTION: What are the key technical focus areas?")
    print("-" * 70)
    print("TECHNICAL KEYWORD ANALYSIS:")
    print()
    
    top_keywords = keywords.most_common(10)
    for keyword, count in top_keywords:
        print(f"  {keyword}: {count} occurrences")
    print()
    
    print("=" * 80)
    print("CONCLUSION: This analysis reveals real patterns, trends, and technologies")
    print("from authentic patent data, providing meaningful insights into UAV")
    print("airflow sensing innovations from 2010-2025.")
    print("=" * 80)

if __name__ == "__main__":
    main()