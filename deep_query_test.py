#!/usr/bin/env python3
"""
Deep Query Analysis for Stasik Knowledge Base
Trace exactly what data is being retrieved and processed
"""

import json
from datetime import datetime
from stasik_agent import StasikAgent

def deep_query_analysis():
    """Perform deep analysis of knowledge base queries"""
    
    print("=" * 80)
    print("DEEP QUERY ANALYSIS - Stasik Knowledge Base")
    print("=" * 80)
    print()
    
    # Initialize agent
    agent = StasikAgent()
    
    print("[QUERY 1] Pitot Tubes Overview")
    print("-" * 60)
    
    result = agent.query_technology("pitot_tubes", "overview")
    print(f"Status: {result['status']}")
    print(f"Technology: {result.get('technology', 'N/A')}")
    print(f"Query Type: {result.get('query_type', 'N/A')}")
    print(f"Agent: {result.get('agent', 'N/A')}")
    print()
    
    if result['status'] == 'success' and 'overview' in result:
        overview = result['overview']
        print("[DETAILED OVERVIEW DATA]")
        print(f"  Description: {overview.get('description', 'N/A')}")
        print(f"  Principle: {overview.get('principle', 'N/A')}")
        print(f"  Patent Activity: {overview.get('patent_activity', 'N/A')}")
        print(f"  Professional Status: {overview.get('professional_status', 'N/A')}")
        
        if 'advantages' in overview:
            print(f"  Advantages: {len(overview['advantages'])} items")
            for i, adv in enumerate(overview['advantages'][:3], 1):
                print(f"    {i}. {adv}")
        
        if 'applications' in overview:
            print(f"  Applications: {len(overview['applications'])} items")
    print()
    
    print("[QUERY 2] MEMS Sensors Overview")
    print("-" * 60)
    
    result2 = agent.query_technology("mems_sensors", "overview")
    if result2['status'] == 'success' and 'overview' in result2:
        overview2 = result2['overview']
        print("[MEMS OVERVIEW DATA]")
        print(f"  Description: {overview2.get('description', 'N/A')}")
        print(f"  Principle: {overview2.get('principle', 'N/A')}")
        print(f"  Patent Activity: {overview2.get('patent_activity', 'N/A')}")
        print(f"  Professional Status: {overview2.get('professional_status', 'N/A')}")
    print()
    
    print("[QUERY 3] Pitot Tubes Comparison")
    print("-" * 60)
    
    result3 = agent.query_technology("pitot_tubes", "comparison")
    if result3['status'] == 'success' and 'comparison' in result3:
        comparison = result3['comparison']
        print("[COMPARISON DATA]")
        print(f"  Base Technology: {comparison.get('base_technology', 'N/A')}")
        
        if 'comparison_analysis' in comparison:
            print("  Comparison Analysis:")
            for tech, analysis in comparison['comparison_analysis'].items():
                print(f"    {tech}: {analysis}")
        
        if 'strengths' in comparison:
            print(f"  Strengths ({len(comparison['strengths'])} items):")
            for i, strength in enumerate(comparison['strengths'][:3], 1):
                print(f"    {i}. {strength}")
        
        if 'competitive_landscape' in comparison:
            landscape = comparison['competitive_landscape']
            print("  Competitive Landscape:")
            for key, value in landscape.items():
                print(f"    {key}: {value}")
    print()
    
    print("[QUERY 4] System Integration Analysis")
    print("-" * 60)
    
    result4 = agent.analyze_system_integration("mems_sensors", "ardupilot")
    print(f"Status: {result4['status']}")
    if result4['status'] == 'success':
        print(f"Primary Sensor: {result4.get('primary_sensor', 'N/A')}")
        print(f"Platform: {result4.get('platform', 'N/A')}")
        
        if 'sensor_integration' in result4:
            integration = result4['sensor_integration']
            print("[INTEGRATION DATA]")
            for key, value in integration.items():
                if isinstance(value, list):
                    print(f"  {key}: {len(value)} items")
                    for i, item in enumerate(value[:2], 1):
                        print(f"    {i}. {item}")
                else:
                    print(f"  {key}: {value}")
    print()
    
    print("[QUERY 5] Professional Guidance")
    print("-" * 60)
    
    result5 = agent.get_professional_guidance("calibration", "ardupilot")
    print(f"Status: {result5['status']}")
    if result5['status'] == 'success':
        print(f"Topic: {result5.get('topic', 'N/A')}")
        print(f"Context: {result5.get('context', 'N/A')}")
        print(f"Source: {result5.get('source', 'N/A')}")
        
        # Show available guidance keys
        guidance_keys = [k for k in result5.keys() if k not in ['status', 'agent', 'topic', 'context', 'timestamp', 'source']]
        print(f"[GUIDANCE SECTIONS] {len(guidance_keys)} sections")
        for key in guidance_keys[:3]:
            print(f"  - {key}")
    print()
    
    print("[RAW DATA STRUCTURE ANALYSIS]")
    print("-" * 60)
    
    # Show the complete structure of one result
    print("Complete Pitot Overview Structure:")
    pitot_keys = list(result.keys()) if result['status'] == 'success' else []
    print(f"Top-level keys: {pitot_keys}")
    
    if 'overview' in result:
        overview_keys = list(result['overview'].keys())
        print(f"Overview keys: {overview_keys}")
    print()
    
    print("[TECHNOLOGY DATABASE SUMMARY]")
    print("-" * 60)
    
    # Get agent info to show what technologies are supported
    info = agent.get_agent_info()
    print(f"Supported Technologies: {len(info['supported_technologies'])}")
    for i, tech in enumerate(info['supported_technologies'], 1):
        print(f"  {i}. {tech}")
    
    print(f"\nKnowledge Sources: {len(info['knowledge_sources'])}")
    for i, source in enumerate(info['knowledge_sources'], 1):
        print(f"  {i}. {source}")
    
    print(f"\nCapabilities: {len(info['capabilities'])}")
    for capability, description in info['capabilities'].items():
        print(f"  {capability}: {description}")
    
    print("\n" + "=" * 80)
    print("DEEP QUERY ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    deep_query_analysis()