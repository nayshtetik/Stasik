#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Stasik Agent
50 test questions covering UAV airflow sensing + ArduPilot integration
"""

import json
import time
from datetime import datetime
from pathlib import Path
from enhanced_stasik_agent import EnhancedStasikAgent

class StasikTestSuite:
    def __init__(self):
        self.agent = EnhancedStasikAgent()
        self.test_results = []
        self.start_time = datetime.now()
        
        # 50 comprehensive test questions
        self.test_questions = [
            # Technology Overview Questions (1-10)
            {
                "id": 1,
                "category": "Technology Overview",
                "question": "What are the key advantages of pitot tubes for UAV airspeed measurement?",
                "test_method": "query_technology",
                "args": ["pitot_tubes", "overview"],
                "expected_elements": ["description", "advantages", "patent_activity"]
            },
            {
                "id": 2,
                "category": "Technology Overview", 
                "question": "Describe the working principle of MEMS airflow sensors",
                "test_method": "query_technology",
                "args": ["mems_sensors", "overview"],
                "expected_elements": ["principle", "description", "professional_status"]
            },
            {
                "id": 3,
                "category": "Technology Overview",
                "question": "What are multi-hole probes and their applications in UAV systems?",
                "test_method": "query_technology", 
                "args": ["multi_hole_probes", "overview"],
                "expected_elements": ["description", "applications", "patent_activity"]
            },
            {
                "id": 4,
                "category": "Technology Overview",
                "question": "Explain anemometer technology for UAV wind measurement",
                "test_method": "query_technology",
                "args": ["anemometers", "overview"],
                "expected_elements": ["description", "principle", "advantages"]
            },
            {
                "id": 5,
                "category": "Technology Comparison",
                "question": "Compare pitot tubes vs MEMS sensors for small UAV applications",
                "test_method": "query_technology",
                "args": ["pitot_tubes", "comparison"],
                "expected_elements": ["comparison_analysis", "strengths", "competitive_landscape"]
            },
            {
                "id": 6,
                "category": "Technology Comparison",
                "question": "What are the trade-offs between multi-hole probes and traditional pitot tubes?",
                "test_method": "query_technology",
                "args": ["multi_hole_probes", "comparison"],
                "expected_elements": ["comparison_analysis", "strengths", "weaknesses"]
            },
            {
                "id": 7,
                "category": "Technology Applications",
                "question": "What are the best applications for MEMS airflow sensors in UAVs?",
                "test_method": "query_technology",
                "args": ["mems_sensors", "applications"],
                "expected_elements": ["applications", "suitability"]
            },
            {
                "id": 8,
                "category": "Technology Applications",
                "question": "Where should anemometers be used in UAV systems?",
                "test_method": "query_technology",
                "args": ["anemometers", "applications"],
                "expected_elements": ["applications", "suitability"]
            },
            {
                "id": 9,
                "category": "Technology Integration",
                "question": "How do you integrate pitot tubes into UAV flight systems?",
                "test_method": "query_technology",
                "args": ["pitot_tubes", "integration"],
                "expected_elements": ["hardware", "software", "calibration"]
            },
            {
                "id": 10,
                "category": "Technology Integration",
                "question": "What are the integration challenges for MEMS sensors in UAVs?",
                "test_method": "query_technology",
                "args": ["mems_sensors", "integration"],
                "expected_elements": ["hardware", "software", "maintenance"]
            },
            
            # ArduPilot Integration Questions (11-25)
            {
                "id": 11,
                "category": "ArduPilot Integration",
                "question": "How do you integrate a pitot tube sensor with ArduPilot?",
                "test_method": "query_ardupilot_integration",
                "args": ["pitot_tubes"],
                "expected_elements": ["ardupilot_integration", "relevant_parameters"]
            },
            {
                "id": 12,
                "category": "ArduPilot Integration",
                "question": "What ArduPilot parameters are needed for MEMS airflow sensors?",
                "test_method": "query_ardupilot_integration",
                "args": ["mems_sensors"],
                "expected_elements": ["ardupilot_integration", "relevant_parameters"]
            },
            {
                "id": 13,
                "category": "ArduPilot Integration",
                "question": "Can multi-hole probes work with ArduPilot autopilot systems?",
                "test_method": "query_ardupilot_integration",
                "args": ["multi_hole_probes"],
                "expected_elements": ["ardupilot_integration", "status"]
            },
            {
                "id": 14,
                "category": "ArduPilot Integration",
                "question": "How to integrate anemometers with ArduPilot for wind sensing?",
                "test_method": "query_ardupilot_integration",
                "args": ["anemometers"],
                "expected_elements": ["ardupilot_integration", "integration_options"]
            },
            {
                "id": 15,
                "category": "ArduPilot Parameters",
                "question": "What is ARSPD_TYPE parameter and how to configure it?",
                "test_method": "get_parameter_guidance",
                "args": ["ARSPD_TYPE"],
                "expected_elements": ["parameter_details", "values", "tuning_notes"]
            },
            {
                "id": 16,
                "category": "ArduPilot Parameters",
                "question": "How do you calibrate ARSPD_RATIO for pitot tube sensors?",
                "test_method": "get_parameter_guidance",
                "args": ["ARSPD_RATIO"],
                "expected_elements": ["parameter_details", "calibration_procedure"]
            },
            {
                "id": 17,
                "category": "ArduPilot Parameters",
                "question": "What does ARSPD_AUTOCAL parameter control in ArduPilot?",
                "test_method": "get_parameter_guidance",
                "args": ["ARSPD_AUTOCAL"],
                "expected_elements": ["parameter_details", "values", "tuning_notes"]
            },
            {
                "id": 18,
                "category": "ArduPilot Parameters",
                "question": "How to configure EK3_ARSP_THR for airspeed fusion?",
                "test_method": "get_parameter_guidance",
                "args": ["EK3_ARSP_THR"],
                "expected_elements": ["parameter_details", "typical_range"]
            },
            {
                "id": 19,
                "category": "EKF Tuning",
                "question": "How do you tune EKF parameters for airspeed sensor fusion?",
                "test_method": "get_ekf_tuning_guidance",
                "args": ["airspeed"],
                "expected_elements": ["tuning_guidance", "key_parameters", "tuning_sequence"]
            },
            {
                "id": 20,
                "category": "EKF Tuning",
                "question": "What are the validation steps for EKF airspeed integration?",
                "test_method": "get_ekf_tuning_guidance",
                "args": ["airspeed"],
                "expected_elements": ["tuning_guidance", "validation_checks"]
            },
            {
                "id": 21,
                "category": "System Integration",
                "question": "How to integrate pitot tubes with ArduPilot EKF system?",
                "test_method": "analyze_enhanced_system_integration",
                "args": ["pitot_tubes", "ardupilot"],
                "expected_elements": ["ardupilot_specifics", "ekf_tuning"]
            },
            {
                "id": 22,
                "category": "System Integration",
                "question": "What are the requirements for MEMS sensor integration with PX4?",
                "test_method": "analyze_enhanced_system_integration",
                "args": ["mems_sensors", "px4"],
                "expected_elements": ["sensor_integration", "platform_guidance"]
            },
            {
                "id": 23,
                "category": "System Integration",
                "question": "How to set up multi-hole probes for advanced UAV control?",
                "test_method": "analyze_enhanced_system_integration",
                "args": ["multi_hole_probes", "ardupilot"],
                "expected_elements": ["ardupilot_specifics", "professional_insights"]
            },
            {
                "id": 24,
                "category": "System Integration",
                "question": "What integration approach is needed for anemometer wind data?",
                "test_method": "analyze_enhanced_system_integration",
                "args": ["anemometers", "ardupilot"],
                "expected_elements": ["sensor_integration", "challenges_solutions"]
            },
            {
                "id": 25,
                "category": "Professional Guidance",
                "question": "What are the best practices for airspeed sensor calibration?",
                "test_method": "get_professional_guidance",
                "args": ["calibration", "ardupilot"],
                "expected_elements": ["calibration_guidance", "topic", "context"]
            },
            
            # Advanced Technical Questions (26-35)
            {
                "id": 26,
                "category": "Advanced Technical",
                "question": "How do temperature effects impact MEMS airflow sensor accuracy?",
                "test_method": "query_technology",
                "args": ["mems_sensors", "integration"],
                "expected_elements": ["calibration", "maintenance"]
            },
            {
                "id": 27,
                "category": "Advanced Technical", 
                "question": "What are the Reynolds number considerations for multi-hole probes?",
                "test_method": "query_technology",
                "args": ["multi_hole_probes", "overview"],
                "expected_elements": ["principle", "professional_status"]
            },
            {
                "id": 28,
                "category": "Advanced Technical",
                "question": "How do static port errors affect pitot tube measurements?",
                "test_method": "query_technology",
                "args": ["pitot_tubes", "integration"],
                "expected_elements": ["installation", "calibration"]
            },
            {
                "id": 29,
                "category": "Advanced Technical",
                "question": "What mounting considerations apply to anemometer installation?",
                "test_method": "query_technology",
                "args": ["anemometers", "integration"],
                "expected_elements": ["installation", "hardware"]
            },
            {
                "id": 30,
                "category": "Troubleshooting",
                "question": "How to diagnose erratic airspeed readings in ArduPilot?",
                "test_method": "get_professional_guidance",
                "args": ["troubleshooting", "ardupilot"],
                "expected_elements": ["troubleshooting", "topic"]
            },
            {
                "id": 31,
                "category": "Troubleshooting",
                "question": "What causes airspeed sensor calibration drift?",
                "test_method": "query_technology",
                "args": ["pitot_tubes", "integration"],
                "expected_elements": ["maintenance", "calibration"]
            },
            {
                "id": 32,
                "category": "Troubleshooting",
                "question": "How to resolve MEMS sensor noise issues in flight?",
                "test_method": "query_technology",
                "args": ["mems_sensors", "integration"],
                "expected_elements": ["software", "calibration"]
            },
            {
                "id": 33,
                "category": "Performance Optimization",
                "question": "How to optimize EKF performance with multiple airspeed sensors?",
                "test_method": "get_ekf_tuning_guidance", 
                "args": ["airspeed"],
                "expected_elements": ["key_parameters", "tuning_sequence"]
            },
            {
                "id": 34,
                "category": "Performance Optimization",
                "question": "What are the latency considerations for airspeed sensor data?",
                "test_method": "analyze_enhanced_system_integration",
                "args": ["pitot_tubes", "ardupilot"],
                "expected_elements": ["sensor_integration", "professional_insights"]
            },
            {
                "id": 35,
                "category": "Performance Optimization",
                "question": "How to achieve redundancy in airspeed measurement systems?",
                "test_method": "analyze_enhanced_system_integration",
                "args": ["pitot_tubes", "ardupilot"],
                "expected_elements": ["ardupilot_specifics", "challenges_solutions"]
            },
            
            # Specialized Applications (36-45)
            {
                "id": 36,
                "category": "Specialized Applications",
                "question": "Which sensors work best for VTOL transition phases?",
                "test_method": "query_technology",
                "args": ["multi_hole_probes", "applications"],
                "expected_elements": ["applications", "suitability"]
            },
            {
                "id": 37,
                "category": "Specialized Applications",
                "question": "How to measure sideslip angle in UAV flight control?",
                "test_method": "query_technology",
                "args": ["multi_hole_probes", "overview"],
                "expected_elements": ["description", "advantages"]
            },
            {
                "id": 38,
                "category": "Specialized Applications",
                "question": "What sensors are suitable for high-altitude UAV operations?",
                "test_method": "query_technology",
                "args": ["pitot_tubes", "applications"],
                "expected_elements": ["applications", "suitability"]
            },
            {
                "id": 39,
                "category": "Specialized Applications",
                "question": "How to implement distributed airflow sensing on large UAVs?",
                "test_method": "query_technology",
                "args": ["mems_sensors", "applications"],
                "expected_elements": ["applications", "suitability"]
            },
            {
                "id": 40,
                "category": "Research Applications",
                "question": "What sensors provide the most accurate flow field data?",
                "test_method": "query_technology",
                "args": ["multi_hole_probes", "comparison"],
                "expected_elements": ["strengths", "best_applications"]
            },
            {
                "id": 41,
                "category": "Research Applications",
                "question": "How to validate airspeed sensor performance in flight testing?",
                "test_method": "get_professional_guidance",
                "args": ["calibration", "general"],
                "expected_elements": ["calibration_guidance", "topic"]
            },
            {
                "id": 42,
                "category": "Commercial Applications",
                "question": "Which airspeed sensors are best for commercial UAV operations?",
                "test_method": "query_technology",
                "args": ["pitot_tubes", "comparison"],
                "expected_elements": ["best_applications", "competitive_landscape"]
            },
            {
                "id": 43,
                "category": "Commercial Applications",
                "question": "What are the certification requirements for UAV airspeed sensors?",
                "test_method": "query_technology",
                "args": ["pitot_tubes", "overview"],
                "expected_elements": ["professional_status", "advantages"]
            },
            {
                "id": 44,
                "category": "Future Technology",
                "question": "What are the emerging trends in UAV airflow sensing?",
                "test_method": "query_technology",
                "args": ["mems_sensors", "overview"],
                "expected_elements": ["professional_status", "description"]
            },
            {
                "id": 45,
                "category": "Future Technology",
                "question": "How might AI/ML improve airspeed sensor data processing?",
                "test_method": "analyze_enhanced_system_integration",
                "args": ["mems_sensors", "ardupilot"],
                "expected_elements": ["professional_insights", "challenges_solutions"]
            },
            
            # Edge Cases and Error Conditions (46-50)
            {
                "id": 46,
                "category": "Edge Cases",
                "question": "What happens when airspeed sensors fail during flight?",
                "test_method": "get_professional_guidance",
                "args": ["troubleshooting", "ardupilot"],
                "expected_elements": ["troubleshooting", "context"]
            },
            {
                "id": 47,
                "category": "Edge Cases",
                "question": "How do icing conditions affect different sensor types?",
                "test_method": "query_technology",
                "args": ["pitot_tubes", "comparison"],
                "expected_elements": ["weaknesses", "comparison_analysis"]
            },
            {
                "id": 48,
                "category": "Edge Cases",
                "question": "What are the limitations of synthetic airspeed in ArduPilot?",
                "test_method": "query_ardupilot_integration",
                "args": ["pitot_tubes"],
                "expected_elements": ["ardupilot_integration", "common_issues"]
            },
            {
                "id": 49,
                "category": "Integration Testing",
                "question": "How to validate airspeed sensor integration with ArduPilot EKF?",
                "test_method": "get_ekf_tuning_guidance",
                "args": ["airspeed"],
                "expected_elements": ["validation_checks", "tuning_guidance"]
            },
            {
                "id": 50,
                "category": "Comprehensive System",
                "question": "Design a complete airflow sensing system for a research UAV",
                "test_method": "analyze_enhanced_system_integration",
                "args": ["multi_hole_probes", "ardupilot", {"accuracy": "high", "research": True}],
                "expected_elements": ["ardupilot_specifics", "ekf_tuning", "professional_insights"]
            }
        ]
    
    def run_single_test(self, test_case):
        """Run a single test case"""
        test_id = test_case["id"]
        category = test_case["category"]
        question = test_case["question"]
        method = test_case["test_method"]
        args = test_case["args"]
        expected = test_case["expected_elements"]
        
        result = {
            "id": test_id,
            "category": category,
            "question": question,
            "method": method,
            "start_time": datetime.now().isoformat(),
            "success": False,
            "response_status": "unknown",
            "elements_found": [],
            "elements_missing": [],
            "response_size": 0,
            "execution_time": 0,
            "error": None
        }
        
        try:
            start_time = time.time()
            
            # Execute the test method
            if method == "query_technology":
                response = self.agent.query_technology(*args)
            elif method == "query_ardupilot_integration":
                response = self.agent.query_ardupilot_integration(*args)
            elif method == "get_parameter_guidance":
                response = self.agent.get_parameter_guidance(*args)
            elif method == "get_ekf_tuning_guidance":
                response = self.agent.get_ekf_tuning_guidance(*args)
            elif method == "analyze_enhanced_system_integration":
                response = self.agent.analyze_enhanced_system_integration(*args)
            elif method == "get_professional_guidance":
                response = self.agent.get_professional_guidance(*args)
            else:
                raise ValueError(f"Unknown test method: {method}")
            
            end_time = time.time()
            result["execution_time"] = round(end_time - start_time, 3)
            result["response_status"] = response.get("status", "unknown")
            result["response_size"] = len(str(response))
            
            # Check for expected elements
            elements_found = []
            elements_missing = []
            
            def check_nested_dict(data, key):
                """Check if key exists in nested dictionary structure"""
                if isinstance(data, dict):
                    if key in data:
                        return True
                    for value in data.values():
                        if check_nested_dict(value, key):
                            return True
                elif isinstance(data, list):
                    for item in data:
                        if check_nested_dict(item, key):
                            return True
                return False
            
            for element in expected:
                if check_nested_dict(response, element):
                    elements_found.append(element)
                else:
                    elements_missing.append(element)
            
            result["elements_found"] = elements_found
            result["elements_missing"] = elements_missing
            
            # Test passes if response is successful and most expected elements are found
            if (response.get("status") == "success" and 
                len(elements_found) >= len(expected) * 0.5):  # At least 50% of expected elements
                result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            result["execution_time"] = time.time() - start_time
        
        return result
    
    def run_comprehensive_test(self):
        """Run all 50 test cases"""
        print("=" * 80)
        print("COMPREHENSIVE STASIK AGENT TEST SUITE")
        print("50 Test Questions - UAV Airflow Sensing + ArduPilot Integration")
        print("=" * 80)
        print()
        
        # Initialize agent info
        agent_info = self.agent.get_enhanced_agent_info()
        print(f"Testing: {agent_info['agent_name']} v{agent_info['version']}")
        print(f"Domain: {agent_info['domain']}")
        print(f"ArduPilot Knowledge: {agent_info['ardupilot_knowledge_loaded']}")
        print()
        
        print("Starting comprehensive test execution...")
        print()
        
        # Run tests by category
        categories = {}
        for test_case in self.test_questions:
            category = test_case["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(test_case)
        
        category_results = {}
        total_tests = 0
        total_passed = 0
        
        for category, tests in categories.items():
            print(f"[CATEGORY] {category} - {len(tests)} tests")
            print("-" * 60)
            
            category_passed = 0
            category_total = len(tests)
            
            for test_case in tests:
                print(f"Test {test_case['id']:2d}: {test_case['question'][:60]}{'...' if len(test_case['question']) > 60 else ''}")
                
                result = self.run_single_test(test_case)
                self.test_results.append(result)
                
                status = "PASS" if result["success"] else "FAIL"
                print(f"         Status: {status} | Time: {result['execution_time']}s | Elements: {len(result['elements_found'])}/{len(test_case['expected_elements'])}")
                
                if result["error"]:
                    print(f"         Error: {result['error']}")
                
                if result["success"]:
                    category_passed += 1
                    total_passed += 1
                
                total_tests += 1
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.1)
            
            category_results[category] = {
                "passed": category_passed,
                "total": category_total,
                "success_rate": (category_passed / category_total * 100) if category_total > 0 else 0
            }
            
            print(f"Category Result: {category_passed}/{category_total} passed ({category_results[category]['success_rate']:.1f}%)")
            print()
        
        # Generate comprehensive report
        self.generate_test_report(category_results, total_passed, total_tests)
        
        return total_passed, total_tests
    
    def generate_test_report(self, category_results, total_passed, total_tests):
        """Generate comprehensive test report"""
        end_time = datetime.now()
        total_duration = end_time - self.start_time
        
        print("=" * 80)
        print("COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)
        print()
        
        # Overall results
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        print(f"Overall Results: {total_passed}/{total_tests} tests passed ({overall_success_rate:.1f}%)")
        print(f"Test Duration: {str(total_duration).split('.')[0]}")
        print(f"Average Test Time: {sum(r['execution_time'] for r in self.test_results) / len(self.test_results):.3f}s")
        print()
        
        # Category breakdown
        print("Category Breakdown:")
        print("-" * 50)
        for category, results in category_results.items():
            print(f"{category:<25} {results['passed']:2d}/{results['total']:2d} ({results['success_rate']:5.1f}%)")
        print()
        
        # Performance metrics
        response_times = [r['execution_time'] for r in self.test_results if r['execution_time'] > 0]
        if response_times:
            print("Performance Metrics:")
            print("-" * 30)
            print(f"Fastest Response: {min(response_times):.3f}s")
            print(f"Slowest Response: {max(response_times):.3f}s")
            print(f"Average Response: {sum(response_times) / len(response_times):.3f}s")
            print()
        
        # Knowledge base utilization
        methods_used = {}
        for result in self.test_results:
            method = result["method"]
            methods_used[method] = methods_used.get(method, 0) + 1
        
        print("Knowledge Base Utilization:")
        print("-" * 40)
        for method, count in methods_used.items():
            print(f"{method:<30} {count:2d} calls")
        print()
        
        # Error analysis
        errors = [r for r in self.test_results if r["error"]]
        if errors:
            print("Error Analysis:")
            print("-" * 20)
            print(f"Tests with errors: {len(errors)}")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  Test {error['id']}: {error['error']}")
            print()
        
        # Success factors
        successful_tests = [r for r in self.test_results if r["success"]]
        if successful_tests:
            avg_elements_found = sum(len(r["elements_found"]) for r in successful_tests) / len(successful_tests)
            avg_response_size = sum(r["response_size"] for r in successful_tests) / len(successful_tests)
            print("Success Metrics:")
            print("-" * 20)
            print(f"Avg Elements Found: {avg_elements_found:.1f}")
            print(f"Avg Response Size: {avg_response_size:.0f} chars")
            print()
        
        # Final assessment
        print("=" * 80)
        print("FINAL ASSESSMENT")
        print("=" * 80)
        
        if overall_success_rate >= 90:
            assessment = "EXCELLENT - Production ready system"
        elif overall_success_rate >= 80:
            assessment = "GOOD - System performing well with minor issues"
        elif overall_success_rate >= 70:
            assessment = "ACCEPTABLE - System functional with some limitations"
        elif overall_success_rate >= 60:
            assessment = "NEEDS IMPROVEMENT - Multiple issues detected"
        else:
            assessment = "POOR - Significant system problems"
        
        print(f"System Assessment: {assessment}")
        print(f"Knowledge Base Coverage: {'Comprehensive' if total_passed > 40 else 'Partial' if total_passed > 30 else 'Limited'}")
        print(f"ArduPilot Integration: {'Functional' if any('ardupilot' in r['method'] for r in successful_tests) else 'Not Tested'}")
        
        # Save detailed results
        self.save_test_results(category_results, total_passed, total_tests, overall_success_rate)
        
        print(f"Detailed results saved to: stasik_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        print("=" * 80)
    
    def save_test_results(self, category_results, total_passed, total_tests, success_rate):
        """Save detailed test results to JSON file"""
        
        results_summary = {
            "test_summary": {
                "total_tests": total_tests,
                "passed": total_passed,
                "success_rate": success_rate,
                "test_duration": str(datetime.now() - self.start_time),
                "timestamp": datetime.now().isoformat()
            },
            "agent_info": self.agent.get_enhanced_agent_info(),
            "category_results": category_results,
            "detailed_results": self.test_results
        }
        
        filename = f"stasik_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = Path("C:/Knowledge/Patents/Stasik-Agent") / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results_summary, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[WARNING] Failed to save detailed results: {e}")

def main():
    """Main test execution"""
    print("Enhanced Stasik Agent - Comprehensive Test Suite")
    print("Generating and executing 50 test questions...")
    print()
    
    test_suite = StasikTestSuite()
    passed, total = test_suite.run_comprehensive_test()
    
    return passed, total

if __name__ == "__main__":
    main()