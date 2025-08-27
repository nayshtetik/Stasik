#!/usr/bin/env python3
"""
Test CFD Keywords Classification - No API Required
Direct test of technology classification logic
"""

def test_cfd_keyword_classification():
    """Test CFD keyword classification without API dependencies"""
    
    print("TESTING CFD KEYWORD CLASSIFICATION")
    print("="*60)
    
    # Replicate the technology classification logic from the files
    tech_indicators = {
        'pitot_tubes': {
            'keywords': ['pitot', 'pitot tube', 'static pressure', 'total pressure', 'dynamic pressure'],
            'score': 0
        },
        'multi_hole_probes': {
            'keywords': ['multi-hole', 'multi hole', '5-hole', '3-hole', 'probe', 'angle of attack', 'sideslip'],
            'score': 0
        },
        'mems_sensors': {
            'keywords': ['mems', 'micro', 'silicon', 'microfabrication', 'chip', 'semiconductor'],
            'score': 0
        },
        'anemometers': {
            'keywords': ['anemometer', 'wind sensor', 'wind measurement', 'ultrasonic', 'wind speed'],
            'score': 0
        },
        'cfd_analysis': {
            'keywords': ['cfd', 'computational fluid dynamics', 'flow simulation', 'flow modeling', 'finite volume', 'finite element', 'ansys fluent', 'openfoam', 'turbulence modeling', 'reynolds', 'navier-stokes', 'boundary layer', 'flow visualization'],
            'score': 0
        }
    }
    
    # Test queries with CFD keywords
    test_queries = [
        "What are the most common CFD analysis techniques in airflow sensors?",
        "How do computational fluid dynamics models help validate pitot tube designs?",
        "Can you explain flow simulation methods for UAV sensor development?",
        "What turbulence modeling approaches work best for MEMS sensor analysis?",
        "How does finite volume method apply to boundary layer analysis in airflow sensors?",
        "Compare OpenFOAM vs ANSYS Fluent for UAV airflow sensor CFD studies",
        "What Reynolds number considerations apply to MEMS airflow sensors?",
        "How does Navier-Stokes equation modeling help with flow visualization?",
        "Can finite element analysis improve pitot tube design?",
        "What are the best practices for boundary layer modeling in UAV applications?"
    ]
    
    print("\nTEST RESULTS:")
    print("-" * 40)
    
    for i, question in enumerate(test_queries, 1):
        print(f"\nQuery {i}: {question}")
        
        question_lower = question.lower()
        
        # Reset scores
        for tech, data in tech_indicators.items():
            data['score'] = 0
        
        # Score each technology based on keyword matches
        for tech, data in tech_indicators.items():
            for keyword in data['keywords']:
                if keyword in question_lower:
                    data['score'] += 1
                    # Boost score if keyword appears multiple times
                    data['score'] += question_lower.count(keyword) - 1
        
        # Find highest scoring technology
        max_score = max(data['score'] for data in tech_indicators.values())
        technology = None
        
        if max_score > 0:
            for tech, data in tech_indicators.items():
                if data['score'] == max_score:
                    technology = tech
                    break
        
        # Show results
        scores = {tech: data['score'] for tech, data in tech_indicators.items() if data['score'] > 0}
        print(f"  Keyword scores: {scores}")
        print(f"  Classification: {technology or 'Multi-domain'} (confidence: {max_score})")
        
        # Highlight CFD detection
        if technology == 'cfd_analysis':
            print(f"  [OK] SUCCESSFULLY DETECTED AS CFD ANALYSIS!")
        elif 'cfd' in question_lower or 'computational fluid' in question_lower:
            print(f"  [WARNING] CFD query but classified as: {technology or 'Multi-domain'}")
    
    print("\n" + "="*60)
    print("CFD KEYWORD CLASSIFICATION TEST COMPLETE")
    
    # Summary
    cfd_detected = 0
    cfd_queries = 0
    
    for question in test_queries:
        if 'cfd' in question.lower() or 'computational fluid' in question.lower() or 'flow simulation' in question.lower() or 'turbulence' in question.lower() or 'openfoam' in question.lower() or 'ansys fluent' in question.lower() or 'reynolds' in question.lower() or 'navier-stokes' in question.lower() or 'finite volume' in question.lower() or 'finite element' in question.lower() or 'boundary layer' in question.lower():
            cfd_queries += 1
            
            question_lower = question.lower()
            
            # Reset scores
            for tech, data in tech_indicators.items():
                data['score'] = 0
            
            # Score
            for tech, data in tech_indicators.items():
                for keyword in data['keywords']:
                    if keyword in question_lower:
                        data['score'] += 1
                        data['score'] += question_lower.count(keyword) - 1
            
            # Find max
            max_score = max(data['score'] for data in tech_indicators.values())
            technology = None
            
            if max_score > 0:
                for tech, data in tech_indicators.items():
                    if data['score'] == max_score:
                        technology = tech
                        break
            
            if technology == 'cfd_analysis':
                cfd_detected += 1
    
    print(f"\nSUMMARY:")
    print(f"CFD-related queries: {cfd_queries}")
    print(f"Correctly detected as CFD: {cfd_detected}")
    print(f"Detection rate: {cfd_detected/cfd_queries*100:.1f}%" if cfd_queries > 0 else "N/A")

if __name__ == "__main__":
    test_cfd_keyword_classification()