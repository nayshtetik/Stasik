#!/usr/bin/env python3
"""
Test Enhanced Knowledge Integration
Test the new fabrication and testing answer generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MockEnhancedChat:
    def _generate_fabrication_answer(self, question: str) -> str:
        """Mock fabrication answer generation"""
        
        answer_parts = []
        answer_parts.append("AIRFLOW SENSOR FABRICATION & PROTOTYPING")
        answer_parts.append("=" * 60)
        
        question_lower = question.lower()
        
        if any(term in question_lower for term in ['3d printing', 'additive manufacturing']):
            answer_parts.append("**ADDITIVE MANUFACTURING FOR AIRFLOW SENSORS:**")
            answer_parts.append("• Enables complex, one-piece probe geometries")
            answer_parts.append("• Materials: Titanium, stainless steel, ABS plastic")
            answer_parts.append("• Applications: Split pitot tubes, high-frequency probes")
        elif any(term in question_lower for term in ['mems', 'microfabrication']):
            answer_parts.append("**MEMS SENSOR MICROFABRICATION:**")
            answer_parts.append("• Silicon/glass substrates with cleanroom processing")
            answer_parts.append("• Photolithography, DRIE, wafer bonding")
            answer_parts.append("• Two-photon polymerization for 3D structures")
        else:
            answer_parts.append("**CONVENTIONAL FABRICATION METHODS:**")
            answer_parts.append("• Precision CNC machining")
            answer_parts.append("• Materials: Steel, brass, titanium")
        
        return "\\n".join(answer_parts)
    
    def _generate_testing_answer(self, question: str) -> str:
        """Mock testing answer generation"""
        
        answer_parts = []
        answer_parts.append("AIRFLOW SENSOR TESTING & CALIBRATION")
        answer_parts.append("=" * 55)
        
        question_lower = question.lower()
        
        if any(term in question_lower for term in ['wind tunnel']):
            answer_parts.append("**WIND TUNNEL TESTING:**")
            answer_parts.append("• Low turbulence levels (0.07% at NIST)")
            answer_parts.append("• Velocity range: 0.2 to 75 m/s")
            answer_parts.append("• LDA reference: 0.5-0.8% uncertainty")
        elif any(term in question_lower for term in ['calibration']):
            answer_parts.append("**CALIBRATION PROCEDURES:**")
            answer_parts.append("• Dead-weight testers for static calibration")
            answer_parts.append("• Dynamic testing up to 25 kHz")
            answer_parts.append("• NIST-traceable certificates")
        else:
            answer_parts.append("**LABORATORY TESTING OVERVIEW:**")
            answer_parts.append("• Environmental testing per DO-160")
            answer_parts.append("• High-speed DAQ systems")
        
        return "\\n".join(answer_parts)

def test_enhanced_knowledge():
    """Test the enhanced knowledge categories"""
    
    print("TESTING ENHANCED KNOWLEDGE INTEGRATION")
    print("="*60)
    
    mock_chat = MockEnhancedChat()
    
    # Test questions covering new knowledge areas
    test_questions = [
        ("How is 3D printing used for airflow sensor fabrication?", "fabrication"),
        ("What are MEMS microfabrication techniques?", "fabrication"),  
        ("How are airflow sensors tested in wind tunnels?", "testing"),
        ("What calibration procedures are used for pitot tubes?", "testing"),
        ("What are the conventional manufacturing methods?", "fabrication"),
        ("What laboratory testing is required?", "testing")
    ]
    
    for i, (question, category) in enumerate(test_questions, 1):
        print(f"\\n{'='*60}")
        print(f"TEST {i}: {question}")
        print(f"Category: {category.upper()}")
        print('='*60)
        
        if category == "fabrication":
            response = mock_chat._generate_fabrication_answer(question)
        else:  # testing
            response = mock_chat._generate_testing_answer(question)
        
        print(response)
        print()

if __name__ == "__main__":
    test_enhanced_knowledge()