#!/usr/bin/env python3
"""
Comprehensive Test Suite for Stasik v2.0 with Unknown-Unknown Discovery Loop
===========================================================================

Complete test coverage for all Stasik functionality including:
- Core UAV airflow sensing knowledge queries
- Unknown-Unknown Discovery Loop with epistemic landscape navigation
- Competency question assessment
- API compatibility methods
- Integration testing
"""

import sys
import traceback
import time
from datetime import datetime

def run_test_suite():
    """Execute complete test suite for Stasik v2.0"""
    
    print("=" * 80)
    print("STASIK v2.0 COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'tests': []
    }
    
    # Test 1: Unknown-Unknown Discovery Loop Standalone
    print("[TEST 1] Unknown-Unknown Discovery Loop Standalone")
    print("-" * 60)
    
    try:
        from unknown_unknown_loop import UnknownUnknownDiscoveryLoop
        
        # Mock knowledge base
        mock_kb = {
            'patents': [
                {'category': 'MEMS_Airflow_Sensors', 'title': f'Test MEMS patent {i}'} for i in range(15)
            ] + [
                {'category': 'Pitot_Tubes_UAV', 'title': f'Test pitot patent {i}'} for i in range(10)
            ],
            'papers': [
                {'title': f'Test paper {i}', 'authors': f'Test authors {i}'} for i in range(5)
            ]
        }
        
        # Initialize
        loop = UnknownUnknownDiscoveryLoop(mock_kb)
        print("[OK] UnknownUnknownDiscoveryLoop initialized")
        
        # Execute discovery loop (1 iteration for speed)
        results = loop.execute_discovery_loop(iterations=1)
        gaps_found = len(results['discovered_gaps'])
        bifurcations = len(results['bifurcation_points'])
        print(f"[OK] Discovery loop executed - {gaps_found} gaps, {bifurcations} bifurcations")
        
        # Generate report
        report = loop.generate_ignorance_report(results)
        print("[OK] Ignorance report generated")
        
        test_results['passed'] += 1
        test_results['tests'].append(('Unknown-Unknown Discovery Loop', 'PASS'))
        
    except Exception as e:
        print(f"[FAIL] Test 1 failed: {e}")
        test_results['failed'] += 1
        test_results['tests'].append(('Unknown-Unknown Discovery Loop', 'FAIL'))
        traceback.print_exc()
    
    print()
    
    # Test 2: Stasik Agent Integration
    print("[TEST 2] Stasik Agent Integration")
    print("-" * 60)
    
    try:
        from debugging_chat_with_tracking import DebuggingStasikChat
        
        # Initialize main agent
        chat = DebuggingStasikChat()
        print("[OK] DebuggingStasikChat initialized")
        
        # Verify integration
        if hasattr(chat, 'unknown_unknown_loop') and chat.unknown_unknown_loop:
            print("[OK] Unknown-Unknown Discovery Loop integrated")
        else:
            raise Exception("Unknown-Unknown Discovery Loop not integrated")
        
        # Check required methods exist
        required_methods = [
            'process_query', 'get_debug_summary', 
            'run_ignorance_testing', 'get_competency_assessment'
        ]
        
        for method in required_methods:
            if hasattr(chat, method):
                print(f"[OK] Method {method} available")
            else:
                raise Exception(f"Method {method} missing")
        
        test_results['passed'] += 1
        test_results['tests'].append(('Stasik Agent Integration', 'PASS'))
        
    except Exception as e:
        print(f"[FAIL] Test 2 failed: {e}")
        test_results['failed'] += 1
        test_results['tests'].append(('Stasik Agent Integration', 'FAIL'))
        traceback.print_exc()
    
    print()
    
    # Test 3: Core Query Processing
    print("[TEST] TEST 3: Core Query Processing")
    print("-" * 60)
    
    try:
        # Test various query types
        test_queries = [
            ('MEMS sensors', 'What are MEMS airflow sensors used in UAVs?'),
            ('Pitot tubes', 'How do pitot tubes measure airspeed?'),
            ('Comparison', 'Compare MEMS vs pitot tube accuracy'),
            ('CFD analysis', 'What is computational fluid dynamics?'),
            ('Troubleshooting', 'How to calibrate airflow sensors?')
        ]
        
        successful_queries = 0
        
        for query_type, query in test_queries:
            try:
                result, tracking = chat.process_query_with_tracking(query, debug_mode=False)
                
                if result and isinstance(result, dict):
                    print(f"[OK] {query_type} query processed")
                    successful_queries += 1
                else:
                    print(f"[FAIL] {query_type} query failed")
                    
            except Exception as e:
                print(f"[FAIL] {query_type} query error: {e}")
        
        if successful_queries == len(test_queries):
            test_results['passed'] += 1
            test_results['tests'].append(('Core Query Processing', 'PASS'))
        else:
            raise Exception(f"Only {successful_queries}/{len(test_queries)} queries succeeded")
        
    except Exception as e:
        print(f"[FAIL] Test 3 failed: {e}")
        test_results['failed'] += 1
        test_results['tests'].append(('Core Query Processing', 'FAIL'))
    
    print()
    
    # Test 4: API Compatibility
    print("[TEST] TEST 4: API Compatibility")
    print("-" * 60)
    
    try:
        # Test process_query API method
        api_response = chat.process_query('What are the advantages of MEMS sensors?')
        
        required_fields = [
            'question', 'category', 'final_answer', 'sources_used', 
            'algorithm_steps', 'llm_usage', 'confidence_score', 'timestamp'
        ]
        
        missing_fields = []
        for field in required_fields:
            if field in api_response:
                print(f"[OK] API field {field} present")
            else:
                missing_fields.append(field)
                print(f"[FAIL] API field {field} missing")
        
        if missing_fields:
            raise Exception(f"Missing API fields: {missing_fields}")
        
        # Test debug summary (needs conversation history)
        debug_summary = chat.get_debug_summary()
        if 'error' in debug_summary and debug_summary['error'] == 'No queries processed yet':
            print("[OK] Debug summary API working (no queries yet)")
        elif 'total_steps' in debug_summary and 'total_time' in debug_summary:
            print("[OK] Debug summary API working")
        else:
            raise Exception("Debug summary API incomplete")
        
        test_results['passed'] += 1
        test_results['tests'].append(('API Compatibility', 'PASS'))
        
    except Exception as e:
        print(f"[FAIL] Test 4 failed: {e}")
        test_results['failed'] += 1
        test_results['tests'].append(('API Compatibility', 'FAIL'))
    
    print()
    
    # Test 5: Ignorance Detection Features
    print("[TEST] TEST 5: Ignorance Detection Features")
    print("-" * 60)
    
    try:
        # Test competency assessment
        assessment = chat.get_competency_assessment()
        
        required_sections = [
            'COMPETENCY QUESTIONS ANALYSIS',
            'OVERALL COMPETENCY SCORE', 
            'KNOWLEDGE ENTROPY',
            'DOMAIN COVERAGE',
            'ANTI-COMPETENCY QUESTIONS'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section in assessment:
                print(f"[OK] Assessment section {section}")
            else:
                missing_sections.append(section)
                print(f"[FAIL] Assessment section {section} missing")
        
        if missing_sections:
            raise Exception(f"Missing assessment sections: {missing_sections}")
        
        # Test ignorance testing (quick run)
        print("[INFO] Running ignorance testing (1 iteration)...")
        ignorance_report = chat.run_ignorance_testing(iterations=1)
        
        if 'IGNORANCE ANALYSIS REPORT' in ignorance_report:
            print("[OK] Ignorance testing completed")
        else:
            raise Exception("Ignorance testing failed")
        
        test_results['passed'] += 1
        test_results['tests'].append(('Ignorance Detection', 'PASS'))
        
    except Exception as e:
        print(f"[FAIL] Test 5 failed: {e}")
        test_results['failed'] += 1
        test_results['tests'].append(('Ignorance Detection', 'FAIL'))
    
    print()
    
    # Test 6: Knowledge Base Integrity
    print("[TEST] TEST 6: Knowledge Base Integrity")
    print("-" * 60)
    
    try:
        agent = chat.agent
        
        # Check knowledge base loading
        if hasattr(agent, 'knowledge_sources') and agent.knowledge_sources:
            sources_count = len(agent.knowledge_sources)
            print(f"[OK] Knowledge sources loaded: {sources_count}")
        else:
            raise Exception("No knowledge sources loaded")
        
        # Check patents access
        if hasattr(agent, 'all_patents') and len(agent.all_patents) > 0:
            patents_count = len(agent.all_patents)
            print(f"[OK] Patents accessible: {patents_count}")
        else:
            print("[WARN]  Patents not directly accessible (may be in knowledge sources)")
        
        # Check papers access
        if hasattr(agent, 'all_papers') and len(agent.all_papers) > 0:
            papers_count = len(agent.all_papers)
            print(f"[OK] Papers accessible: {papers_count}")
        else:
            print("[WARN]  Papers not directly accessible (may be in knowledge sources)")
        
        test_results['passed'] += 1
        test_results['tests'].append(('Knowledge Base Integrity', 'PASS'))
        
    except Exception as e:
        print(f"[FAIL] Test 6 failed: {e}")
        test_results['failed'] += 1
        test_results['tests'].append(('Knowledge Base Integrity', 'FAIL'))
    
    # Final Results
    print()
    print("=" * 80)
    print("TEST SUITE RESULTS")
    print("=" * 80)
    
    total_tests = test_results['passed'] + test_results['failed']
    success_rate = (test_results['passed'] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {test_results['passed']} [OK]")
    print(f"Failed: {test_results['failed']} [FAIL]")
    print(f"Success Rate: {success_rate:.1f}%")
    print()
    
    print("Individual Test Results:")
    for test_name, result in test_results['tests']:
        status = "[OK] PASS" if result == "PASS" else "[FAIL] FAIL"
        print(f"  {test_name}: {status}")
    
    print()
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Return success if all tests passed
    return test_results['failed'] == 0

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)