#!/usr/bin/env python3
"""
Test CFD Analysis Classification
Verify that CFD keywords are properly recognized and classified
"""

from natural_language_stasik import NaturalLanguageStasik
from debugging_chat_with_tracking import DebuggingStasikChat

def test_cfd_technology_classification():
    """Test that CFD queries are properly classified"""
    
    print("TESTING CFD TECHNOLOGY CLASSIFICATION")
    print("="*60)
    
    # Test queries with CFD keywords
    test_queries = [
        "What are the most common CFD analysis techniques in airflow sensors?",
        "How do computational fluid dynamics models help validate pitot tube designs?",
        "Can you explain flow simulation methods for UAV sensor development?",
        "What turbulence modeling approaches work best for MEMS sensor analysis?",
        "How does finite volume method apply to boundary layer analysis in airflow sensors?",
        "Compare OpenFOAM vs ANSYS Fluent for UAV airflow sensor CFD studies"
    ]
    
    # Test with Natural Language Stasik
    print("\n1. TESTING NATURAL LANGUAGE STASIK:")
    print("-" * 40)
    
    try:
        nl_stasik = NaturalLanguageStasik()
        
        for i, query in enumerate(test_queries, 1):
            print(f"\nQuery {i}: {query}")
            technology = nl_stasik._extract_technology_focus(query)
            print(f"Classified as: {technology or 'Multi-domain'}")
            
    except Exception as e:
        print(f"Error with Natural Language Stasik: {e}")
    
    # Test with Debugging Chat (technology classification only)
    print("\n\n2. TESTING DEBUGGING CHAT CLASSIFICATION:")
    print("-" * 40)
    
    try:
        debug_chat = DebuggingStasikChat()
        
        for i, query in enumerate(test_queries, 1):
            print(f"\nQuery {i}: {query}")
            technology = debug_chat._extract_technology_focus_tracked(query, debug_mode=False)
            print(f"Classified as: {technology or 'Multi-domain'}")
            
    except Exception as e:
        print(f"Error with Debugging Chat: {e}")
    
    print("\n" + "="*60)
    print("CFD CLASSIFICATION TEST COMPLETE")
    print("="*60)
    
    # Test specific keyword detection
    print("\nTESTING SPECIFIC CFD KEYWORD DETECTION:")
    print("-" * 40)
    
    cfd_keywords = [
        'cfd', 'computational fluid dynamics', 'flow simulation', 
        'flow modeling', 'finite volume', 'finite element', 
        'ansys fluent', 'openfoam', 'turbulence modeling', 
        'reynolds', 'navier-stokes', 'boundary layer', 'flow visualization'
    ]
    
    test_keyword_query = "How does computational fluid dynamics help with boundary layer analysis using OpenFOAM for finite volume turbulence modeling?"
    
    print(f"\nKeyword-rich query: {test_keyword_query}")
    
    # Count keyword matches manually
    query_lower = test_keyword_query.lower()
    matches = []
    for keyword in cfd_keywords:
        if keyword in query_lower:
            matches.append(keyword)
    
    print(f"Keywords found: {matches}")
    print(f"Total matches: {len(matches)}")
    
    # Test classification
    try:
        nl_stasik = NaturalLanguageStasik()
        technology = nl_stasik._extract_technology_focus(test_keyword_query)
        print(f"Final classification: {technology or 'Multi-domain'}")
    except Exception as e:
        print(f"Classification error: {e}")

if __name__ == "__main__":
    test_cfd_technology_classification()