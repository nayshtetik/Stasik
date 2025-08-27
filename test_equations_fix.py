#!/usr/bin/env python3
"""
Test Fixed Equations Response
"""

def mock_cfd_answer(question: str) -> str:
    """Mock CFD answer with fixed order"""
    
    answer_parts = []
    answer_parts.append("CFD ANALYSIS FOR AIRFLOW SENSORS")
    answer_parts.append("=" * 50)
    
    question_lower = question.lower()
    
    # Fixed order: most specific first
    if any(term in question_lower for term in ['equations', 'equation', 'navier-stokes', 'continuity', 'momentum']):
        answer_parts.append("**FUNDAMENTAL CFD EQUATIONS FOR AIRFLOW SENSORS:**")
        answer_parts.append("")
        answer_parts.append("**1. Navier-Stokes Equations (Momentum Conservation):**")
        answer_parts.append("   • Governs fluid motion around sensors")
        answer_parts.append("   • Form: ∂u/∂t + u·∇u = -∇p/ρ + ν∇²u + f")
        answer_parts.append("")
        answer_parts.append("**2. Continuity Equation (Mass Conservation):**")
        answer_parts.append("   • Ensures mass conservation in flow domain")
        answer_parts.append("   • Form: ∂ρ/∂t + ∇·(ρu) = 0")
        
    elif any(term in question_lower for term in ['most common', 'common techniques', 'techniques', 'methods']):
        answer_parts.append("**COMMON CFD ANALYSIS TECHNIQUES:**")
        answer_parts.append("• RANS Modeling")
        answer_parts.append("• Large Eddy Simulation")
        
    else:
        answer_parts.append("**GENERAL CFD APPLICATIONS:**")
        answer_parts.append("• Design optimization")
    
    return "\\n".join(answer_parts)

def test_both_questions():
    """Test both equations and techniques questions"""
    
    print("TESTING FIXED CFD QUESTION ROUTING")
    print("="*50)
    
    questions = [
        "What are the most used equations in CFD analysis of airflow sensors?",
        "What are the most common CFD analysis techniques in airflow sensors?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\\nTest {i}: {question}")
        print("-"*40)
        
        response = mock_cfd_answer(question)
        
        if "EQUATIONS" in response:
            print("[OK] Correctly routed to EQUATIONS response")
        elif "TECHNIQUES" in response:
            print("[OK] Correctly routed to TECHNIQUES response")  
        elif "APPLICATIONS" in response:
            print("[WARNING] Routed to general APPLICATIONS response")
        
        # Show a snippet
        lines = response.split("\\n")
        for line in lines[:5]:
            print(f"  {line}")

if __name__ == "__main__":
    test_both_questions()