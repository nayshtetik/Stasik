#!/usr/bin/env python3
"""
Test Equations Detection in CFD Response
"""

def test_equations_detection():
    """Test if equations keywords are being detected properly"""
    
    test_query = "What are the most used equations in CFD analysis of airflow sensors?"
    question_lower = test_query.lower()
    
    print("TESTING EQUATIONS DETECTION")
    print("="*50)
    print(f"Query: {test_query}")
    print(f"Lowercase: {question_lower}")
    print()
    
    # Test the detection logic
    equation_terms = ['equations', 'equation', 'navier-stokes', 'continuity', 'momentum']
    
    print("Testing equation terms:")
    for term in equation_terms:
        if term in question_lower:
            print(f"[OK] FOUND: '{term}' in query")
        else:
            print(f"[X] NOT FOUND: '{term}' in query")
    
    # Overall detection
    equations_detected = any(term in question_lower for term in equation_terms)
    print(f"\nOverall equations detection: {equations_detected}")
    
    # Test other CFD terms to see what might be triggering instead
    other_cfd_terms = {
        'techniques': ['most common', 'common techniques', 'techniques', 'methods'],
        'turbulence': ['turbulence modeling', 'turbulence', 'modeling'],
        'software': ['openfoam', 'ansys', 'fluent', 'software'],
        'boundary': ['boundary layer', 'boundary', 'layer']
    }
    
    print("\nTesting other CFD categories:")
    for category, terms in other_cfd_terms.items():
        detected = any(term in question_lower for term in terms)
        if detected:
            print(f"[OK] {category.upper()} category detected")
            for term in terms:
                if term in question_lower:
                    print(f"    - Found term: '{term}'")
        else:
            print(f"[X] {category.upper()} category not detected")

if __name__ == "__main__":
    test_equations_detection()