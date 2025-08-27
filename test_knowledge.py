#!/usr/bin/env python3
"""
Test Stasik Knowledge Base Access
Direct test without GPT integration
"""

from stasik_agent import StasikAgent

def test_stasik_knowledge():
    """Test direct Stasik knowledge base access"""
    print("=" * 60)
    print("Testing Stasik Knowledge Base Access")
    print("=" * 60)
    
    # Initialize agent
    agent = StasikAgent()
    
    # Test 1: Multi-hole probes overview
    print("\n[Test 1] Multi-hole Probes Overview:")
    print("-" * 40)
    result1 = agent.query_technology("multi_hole_probes", "overview")
    if result1['status'] == 'success':
        overview = result1['overview']
        print(f"Description: {overview['description']}")
        print(f"Principle: {overview['principle']}")
        print(f"Patent Activity: {overview['patent_activity']}")
        print(f"Professional Status: {overview['professional_status']}")
    else:
        print(f"Error: {result1.get('message', 'Unknown error')}")
    
    # Test 2: MEMS sensors overview
    print("\n[Test 2] MEMS Sensors Overview:")
    print("-" * 40)
    result2 = agent.query_technology("mems_sensors", "overview")
    if result2['status'] == 'success':
        overview = result2['overview']
        print(f"Description: {overview['description']}")
        print(f"Principle: {overview['principle']}")
        print(f"Patent Activity: {overview['patent_activity']}")
        print(f"Professional Status: {overview['professional_status']}")
    else:
        print(f"Error: {result2.get('message', 'Unknown error')}")
    
    # Test 3: Multi-hole probes comparison
    print("\n[Test 3] Multi-hole Probes Comparison:")
    print("-" * 40)
    result3 = agent.query_technology("multi_hole_probes", "comparison")
    if result3['status'] == 'success':
        if 'comparison' in result3:
            comparison = result3['comparison']
            for key, value in comparison.items():
                print(f"{key}: {value}")
    else:
        print(f"Error: {result3.get('message', 'Unknown error')}")
    
    # Test 4: System integration analysis
    print("\n[Test 4] System Integration Analysis:")
    print("-" * 40)
    result4 = agent.analyze_system_integration("multi_hole_probes", "ardupilot")
    if result4['status'] == 'success':
        print(f"Primary Sensor: {result4['primary_sensor']}")
        print(f"Platform: {result4['platform']}")
        if 'sensor_integration' in result4:
            print("Integration Details:")
            integration = result4['sensor_integration']
            for key, value in integration.items():
                if isinstance(value, list):
                    print(f"  {key}: {', '.join(value[:2])}")  # Show first 2 items
                else:
                    print(f"  {key}: {value}")
    else:
        print(f"Error: {result4.get('message', 'Unknown error')}")
    
    # Test 5: Professional guidance
    print("\n[Test 5] Professional Guidance:")
    print("-" * 40)
    result5 = agent.get_professional_guidance("calibration", "ardupilot")
    if result5['status'] == 'success':
        print(f"Topic: {result5['topic']}")
        print(f"Context: {result5['context']}")
        print("Guidance available in response")
    else:
        print(f"Error: {result5.get('message', 'Unknown error')}")
    
    print("\n" + "=" * 60)
    print("Knowledge Base Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    test_stasik_knowledge()