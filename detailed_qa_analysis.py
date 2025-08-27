#!/usr/bin/env python3
"""
Detailed Q&A Analysis with Full Reasoning Logic
Shows complete question-answer flow with RAG reasoning and content analysis
"""

import json
import time
from datetime import datetime
from hybrid_search_agent import HybridSearchAgent

def show_detailed_qa_flow():
    """Show complete Q&A flow with reasoning logic"""
    
    print("DETAILED Q&A ANALYSIS WITH REASONING LOGIC")
    print("=" * 80)
    print("Complete flow: Question -> RAG Reasoning -> Knowledge Extraction -> Answer")
    print("=" * 80)
    
    # Initialize hybrid agent
    agent = HybridSearchAgent()
    
    # Representative questions across all domains
    test_cases = [
        {
            "question": "How do pitot tubes measure airspeed?",
            "technology": "pitot_tubes",
            "focus": "Basic principle explanation"
        },
        {
            "question": "ARSPD_TYPE configuration errors ArduPilot 2024",
            "technology": "pitot_tubes", 
            "focus": "Parameter troubleshooting with current info"
        },
        {
            "question": "Multi-hole probe angle of attack measurement accuracy",
            "technology": "multi_hole_probes",
            "focus": "Advanced measurement capability"
        },
        {
            "question": "MEMS sensor calibration drift issues",
            "technology": "mems_sensors",
            "focus": "Troubleshooting and solutions"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        question = test_case["question"]
        technology = test_case["technology"]
        focus = test_case["focus"]
        
        print(f"\nQ&A ANALYSIS {i}/4")
        print("=" * 60)
        print(f"QUESTION: {question}")
        print(f"TECHNOLOGY: {technology}")
        print(f"FOCUS: {focus}")
        print()
        
        # Execute hybrid query and capture full reasoning
        start_time = time.time()
        result = agent.hybrid_query(question, technology)
        execution_time = time.time() - start_time
        
        print("STEP 1: REASONING LOGIC ANALYSIS")
        print("-" * 40)
        
        # Show complete reasoning steps
        reasoning_steps = result.get("reasoning", {}).get("reasoning_steps", [])
        print(f"Total Reasoning Steps: {len(reasoning_steps)}")
        
        for step in reasoning_steps:
            step_type = step.get("step_type", "unknown").upper()
            description = step.get("description", "")
            timestamp = step.get("timestamp", "")
            print(f"[{step_type}] {description}")
        
        print()
        print("STEP 2: GAP ANALYSIS")
        print("-" * 40)
        
        gaps = result.get("reasoning", {}).get("gaps_identified", {})
        total_gaps = sum(len(gap_list) for gap_list in gaps.values())
        
        print(f"Total Knowledge Gaps Identified: {total_gaps}")
        for gap_type, gap_list in gaps.items():
            if gap_list:
                print(f"  {gap_type.replace('_', ' ').title()}:")
                for gap in gap_list:
                    print(f"    - {gap}")
        
        print()
        print("STEP 3: SEARCH STRATEGY DECISION")
        print("-" * 40)
        
        strategy = result.get("reasoning", {}).get("search_strategy", {})
        print(f"Use SearXNG: {strategy.get('use_searxng', False)}")
        print(f"Search Type: {strategy.get('search_type', 'N/A')}")
        print(f"Reasoning: {strategy.get('reason', 'N/A')}")
        
        if strategy.get("queries"):
            print(f"Dynamic Queries Generated:")
            for query in strategy["queries"]:
                print(f"  - {query}")
        
        print()
        print("STEP 4: KNOWLEDGE EXTRACTION")
        print("-" * 40)
        
        # Static knowledge content
        static_results = result.get("static_results", {})
        print(f"Static Knowledge Sources: {len(static_results)}")
        
        for source_name, source_data in static_results.items():
            if source_data.get("status") == "success":
                print(f"\n[STATIC SOURCE: {source_name.upper()}]")
                
                # Extract meaningful content
                if "overview" in source_data:
                    overview = source_data["overview"]
                    print(f"Description: {overview.get('description', 'N/A')}")
                    print(f"Patent Activity: {overview.get('patent_activity', 'N/A')}")
                    if overview.get("advantages"):
                        print(f"Key Advantages: {', '.join(overview['advantages'][:3])}")
                
                if "ardupilot_integration" in source_data:
                    ardupilot = source_data["ardupilot_integration"]
                    print("ArduPilot Integration:")
                    if ardupilot.get("key_parameters"):
                        params = list(ardupilot["key_parameters"].items())[:3]
                        for param, desc in params:
                            print(f"  {param}: {desc}")
                    if ardupilot.get("integration_points"):
                        print(f"  Integration Points: {', '.join(ardupilot['integration_points'][:2])}")
                
                if "parameter_details" in source_data:
                    param_details = source_data["parameter_details"]
                    print(f"Parameter: {source_data.get('parameter', 'N/A')}")
                    print(f"Description: {param_details.get('description', 'N/A')[:200]}")
                    if param_details.get("values"):
                        print("Parameter Values:")
                        for value, desc in list(param_details["values"].items())[:3]:
                            print(f"  {value}: {desc}")
        
        # Dynamic search content
        dynamic_results = result.get("dynamic_results", {})
        if dynamic_results:
            print(f"\nDynamic Search Results: {len(dynamic_results)}")
            
            for search_key, search_data in dynamic_results.items():
                if search_data.get("status") == "success":
                    print(f"\n[DYNAMIC SOURCE: {search_key.upper()}]")
                    print(f"Query: {search_data.get('query', 'N/A')}")
                    
                    search_results = search_data.get("results", {}).get("results", [])[:2]
                    for j, search_result in enumerate(search_results, 1):
                        title = search_result.get('title', 'N/A')[:80]
                        content = search_result.get('content', 'N/A')[:150]
                        url = search_result.get('url', 'N/A')
                        print(f"  Result {j}:")
                        print(f"    Title: {title}")
                        print(f"    Content: {content}...")
                        print(f"    URL: {url}")
        
        print()
        print("STEP 5: ANSWER SYNTHESIS")
        print("-" * 40)
        
        synthesis = result.get("synthesis", {})
        print(f"Primary Source: {synthesis.get('primary_source', 'N/A')}")
        print(f"Confidence Score: {synthesis.get('confidence', 0):.2f}")
        print(f"Completeness Score: {synthesis.get('completeness', 0):.2f}")
        
        if synthesis.get("recommendations"):
            print("Recommendations:")
            for rec in synthesis["recommendations"]:
                print(f"  - {rec}")
        
        print()
        print("STEP 6: PERFORMANCE METRICS")
        print("-" * 40)
        print(f"Execution Time: {execution_time:.2f} seconds")
        print(f"Response Size: {len(json.dumps(result))/1024:.1f}KB")
        print(f"Static Coverage: {result.get('reasoning', {}).get('static_coverage', 0)} results")
        print(f"Dynamic Coverage: {result.get('reasoning', {}).get('dynamic_coverage', 0)} results")
        
        print()
        print("STEP 7: SIMULATED GPT RESPONSE LOGIC")
        print("-" * 40)
        
        # Show how this would be processed for GPT response
        knowledge_summary = ""
        
        # Static knowledge synthesis
        for source_name, source_data in static_results.items():
            if source_data.get("status") == "success":
                if "overview" in source_data:
                    overview = source_data["overview"]
                    knowledge_summary += f"[{source_name}] {overview.get('description', '')}\n"
                    if overview.get("advantages"):
                        knowledge_summary += f"Advantages: {', '.join(overview['advantages'][:2])}\n"
                
                if "ardupilot_integration" in source_data:
                    ardupilot = source_data["ardupilot_integration"]
                    if ardupilot.get("key_parameters"):
                        params = list(ardupilot["key_parameters"].items())[:2]
                        knowledge_summary += f"ArduPilot Parameters: {dict(params)}\n"
        
        # Dynamic knowledge synthesis
        for search_key, search_data in dynamic_results.items():
            if search_data.get("status") == "success":
                search_results = search_data.get("results", {}).get("results", [])[:1]
                for search_result in search_results:
                    title = search_result.get('title', '')[:60]
                    content = search_result.get('content', '')[:100]
                    knowledge_summary += f"[Dynamic] {title}: {content}\n"
        
        print("Knowledge Summary for GPT:")
        print(knowledge_summary[:500] + "..." if len(knowledge_summary) > 500 else knowledge_summary)
        
        print()
        print("COMPLETE Q&A LOGIC FLOW DEMONSTRATED")
        print("Static Knowledge -> Gap Analysis -> Dynamic Search -> Synthesis -> Response")
        
        if i < len(test_cases):
            print("\n" + "="*80 + "\n")
            time.sleep(1)
    
    print("\n\nCOMPREHENSIVE Q&A ANALYSIS COMPLETE")
    print("=" * 80)
    print("[OK] Complete reasoning logic captured")
    print("[OK] Knowledge extraction process detailed") 
    print("[OK] Search strategy decisions explained")
    print("[OK] Content synthesis methodology shown")
    print("[OK] Answer generation logic demonstrated")
    print("[OK] Performance metrics documented")

if __name__ == "__main__":
    show_detailed_qa_flow()