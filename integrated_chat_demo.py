#!/usr/bin/env python3
"""
Demo of Enhanced Integrated Chat Capabilities
Shows the enhanced knowledge base querying without requiring OpenAI API
"""

from enhanced_stasik_agent import EnhancedStasikAgent

def simulate_chat_query_processing(user_question):
    """Simulate the enhanced chat query processing"""
    
    agent = EnhancedStasikAgent()
    
    print(f"USER QUESTION: {user_question}")
    print("=" * 60)
    
    # Simulate the enhanced query processing logic
    user_lower = user_question.lower()
    stasik_results = {}
    
    # Technology detection
    tech_keywords = {
        'pitot_tubes': ['pitot', 'pitot tube', 'pitot-tube'],
        'multi_hole_probes': ['multi-hole', 'multi hole', 'probe', 'probes'],
        'anemometers': ['anemometer', 'anemometers', 'wind sensor'],
        'mems_sensors': ['mems', 'mems sensor', 'mems sensors', 'micro']
    }
    
    detected_techs = []
    for tech, keywords in tech_keywords.items():
        if any(keyword in user_lower for keyword in keywords):
            detected_techs.append(tech)
    
    print(f"[KNOWLEDGE ACCESS] Detected technologies: {', '.join(detected_techs) if detected_techs else 'General query'}")
    
    # Query knowledge base for detected technologies
    if detected_techs:
        for tech in detected_techs[:1]:  # Show first technology
            # Get overview
            overview_result = agent.query_technology(tech)
            stasik_results[f"{tech}_overview"] = overview_result
            print(f"[STASIK DB] Technology overview retrieved for {tech}")
            
            # Get ArduPilot integration if mentioned
            if any(word in user_lower for word in ['integrate', 'integration', 'ardupilot']):
                int_result = agent.query_ardupilot_integration(tech)
                stasik_results[f"{tech}_ardupilot_integration"] = int_result
                print(f"[ARDUPILOT KB] Integration guidance retrieved for {tech}")
    
    # ArduPilot parameter queries
    ardupilot_params = ['ARSPD_TYPE', 'ARSPD_RATIO', 'ARSPD_AUTOCAL', 'EK3_ARSP_THR']
    for param in ardupilot_params:
        if param.lower() in user_lower:
            param_result = agent.get_parameter_guidance(param)
            stasik_results[f"param_{param}"] = param_result
            print(f"[ARDUPILOT KB] Parameter guidance retrieved for {param}")
    
    # EKF tuning queries
    if any(word in user_lower for word in ['ekf', 'ekf3', 'tuning', 'fusion']):
        ekf_result = agent.get_ekf_tuning_guidance('airspeed')
        stasik_results["ekf_tuning"] = ekf_result
        print(f"[ARDUPILOT KB] EKF tuning guidance retrieved")
    
    # Display retrieved knowledge
    print()
    print("KNOWLEDGE BASE DATA RETRIEVED:")
    print("-" * 40)
    
    for key, result in stasik_results.items():
        if result.get("status") == "success":
            print(f"\n[{key.upper()}]")
            
            # Format overview data
            if "overview" in result:
                overview = result["overview"]
                print(f"  Description: {overview.get('description', 'N/A')}")
                print(f"  Patent Activity: {overview.get('patent_activity', 'N/A')}")
                if 'advantages' in overview:
                    print(f"  Advantages: {', '.join(overview['advantages'][:2])}")
            
            # Format ArduPilot integration
            if "ardupilot_integration" in result:
                ardupilot = result["ardupilot_integration"]
                if "ardupilot_drivers" in ardupilot:
                    print(f"  Drivers: {', '.join(ardupilot['ardupilot_drivers'][:2])}")
                if "key_parameters" in ardupilot:
                    params = list(ardupilot["key_parameters"].items())[:2]
                    for param, desc in params:
                        print(f"  {param}: {desc}")
            
            # Format parameter details
            if "parameter_details" in result:
                param_details = result["parameter_details"]
                print(f"  Parameter: {result.get('parameter', 'N/A')}")
                print(f"  Description: {param_details.get('description', 'N/A')}")
                if "values" in param_details:
                    values = list(param_details["values"].items())[:2]
                    for value, desc in values:
                        print(f"    {value}: {desc}")
            
            # Format EKF tuning
            if "tuning_guidance" in result:
                ekf = result["tuning_guidance"]
                if "key_parameters" in ekf:
                    params = list(ekf["key_parameters"].items())[:2]
                    print("  EKF Parameters:")
                    for param, desc in params:
                        print(f"    {param}: {desc}")
    
    print()
    print("=" * 60)
    print("[GPT-5 WOULD PROCESS THIS DATA TO GENERATE NATURAL LANGUAGE RESPONSE]")
    print("The integrated chat uses this retrieved data to create comprehensive,")
    print("conversational responses about UAV airflow sensing and ArduPilot integration.")

def main():
    """Demo the enhanced chat capabilities"""
    
    print("ENHANCED INTEGRATED CHAT DEMO")
    print("=" * 80)
    print("Demonstrating enhanced knowledge base querying capabilities")
    print("(Without requiring OpenAI API key)")
    print("=" * 80)
    print()
    
    # Demo different query types
    demo_queries = [
        "How do pitot tubes work with ArduPilot?",
        "What is ARSPD_TYPE parameter?",
        "How to tune EKF3 for airspeed sensors?",
        "Compare MEMS sensors vs pitot tubes"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"DEMO {i}/4:")
        simulate_chat_query_processing(query)
        print()
        if i < len(demo_queries):
            print("-" * 80)
            print()
    
    print("=" * 80)
    print("ENHANCED CHAT FEATURES DEMONSTRATED:")
    print("✓ Technology detection and routing")
    print("✓ Dual knowledge base access (Stasik + ArduPilot)")
    print("✓ Parameter-specific guidance")
    print("✓ EKF tuning support")
    print("✓ ArduPilot integration details")
    print("✓ Structured knowledge retrieval")
    print()
    print("To use with full GPT-5 natural language generation:")
    print("Set OPENAI_API_KEY and run: python integrated_chat.py")
    print("=" * 80)

if __name__ == "__main__":
    main()