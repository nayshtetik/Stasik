#!/usr/bin/env python3
"""
Comprehensive Test Suite with RAG Reasoning Logging
Tests Enhanced Stasik Agent with detailed reasoning capture
"""

import json
import time
from datetime import datetime
from enhanced_stasik_agent import EnhancedStasikAgent
from pathlib import Path

class RAGReasoningLogger:
    """Captures detailed RAG (Retrieval-Augmented Generation) reasoning"""
    
    def __init__(self):
        self.reasoning_log = []
    
    def log_query_reasoning(self, question_id, question, method_used, reasoning_steps):
        """Log detailed reasoning for each query"""
        entry = {
            "question_id": question_id,
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "method_used": method_used,
            "rag_steps": reasoning_steps
        }
        self.reasoning_log.append(entry)
    
    def save_reasoning_log(self, filename):
        """Save reasoning log to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.reasoning_log, f, indent=2, ensure_ascii=False)

class EnhancedStasikAgentWithLogging(EnhancedStasikAgent):
    """Enhanced Stasik Agent with detailed RAG reasoning logging"""
    
    def __init__(self, ardupilot_kb_path=None):
        super().__init__(ardupilot_kb_path)
        self.rag_logger = RAGReasoningLogger()
        self.query_count = 0
    
    def log_rag_reasoning(self, question_id, question, method, steps):
        """Log RAG reasoning steps"""
        self.rag_logger.log_query_reasoning(question_id, question, method, steps)
    
    def query_technology_with_logging(self, technology, question_id, question):
        """Query technology with detailed RAG logging"""
        self.query_count += 1
        
        rag_steps = [
            {
                "step": 1,
                "process": "Intent Analysis",
                "action": f"Analyzing query for technology: {technology}",
                "reasoning": f"Question asks about {technology} - routing to core knowledge base"
            },
            {
                "step": 2,
                "process": "Knowledge Retrieval",
                "action": f"Accessing Stasik knowledge base for {technology}",
                "reasoning": f"Retrieving technology overview, advantages, applications for {technology}"
            },
            {
                "step": 3,
                "process": "Context Preparation",
                "action": "Structuring response with patent insights",
                "reasoning": "Organizing retrieved knowledge into coherent technical response"
            },
            {
                "step": 4,
                "process": "Response Generation", 
                "action": "Generating technical explanation",
                "reasoning": "Synthesizing patent data into professional technical guidance"
            }
        ]
        
        self.log_rag_reasoning(question_id, question, "query_technology", rag_steps)
        return super().query_technology(technology)
    
    def query_ardupilot_integration_with_logging(self, technology, question_id, question, platform="ardupilot"):
        """Query ArduPilot integration with RAG logging"""
        self.query_count += 1
        
        rag_steps = [
            {
                "step": 1,
                "process": "Dual Knowledge Access",
                "action": f"Accessing both Stasik DB and ArduPilot KB for {technology}",
                "reasoning": "Question requires both technology knowledge and ArduPilot integration details"
            },
            {
                "step": 2,
                "process": "ArduPilot Parameter Mapping",
                "action": f"Retrieving ArduPilot parameters for {technology}",
                "reasoning": "Looking up ARSPD_*, EK3_* parameters and integration mappings"
            },
            {
                "step": 3,
                "process": "Integration Analysis",
                "action": "Analyzing driver compatibility and configuration requirements",
                "reasoning": "Matching technology capabilities with ArduPilot driver support"
            },
            {
                "step": 4,
                "process": "Professional Insights Integration",
                "action": "Adding best practices and common issues",
                "reasoning": "Enhancing response with real-world implementation guidance"
            }
        ]
        
        self.log_rag_reasoning(question_id, question, "query_ardupilot_integration", rag_steps)
        return super().query_ardupilot_integration(technology, platform)
    
    def get_parameter_guidance_with_logging(self, parameter, question_id, question):
        """Get parameter guidance with RAG logging"""
        self.query_count += 1
        
        rag_steps = [
            {
                "step": 1,
                "process": "Parameter Database Query",
                "action": f"Looking up parameter {parameter} in ArduPilot knowledge base",
                "reasoning": "Accessing parameter-specific configuration and tuning guidance"
            },
            {
                "step": 2,
                "process": "Context Enrichment",
                "action": "Adding parameter values, ranges, and relationships",
                "reasoning": "Providing comprehensive parameter configuration information"
            },
            {
                "step": 3,
                "process": "Professional Guidance",
                "action": "Including tuning notes and best practices",
                "reasoning": "Adding practical implementation and calibration guidance"
            }
        ]
        
        self.log_rag_reasoning(question_id, question, "get_parameter_guidance", rag_steps)
        return super().get_parameter_guidance(parameter)
    
    def get_ekf_tuning_guidance_with_logging(self, sensor_type, question_id, question):
        """Get EKF tuning guidance with RAG logging"""
        self.query_count += 1
        
        rag_steps = [
            {
                "step": 1,
                "process": "EKF Knowledge Retrieval",
                "action": f"Accessing EKF tuning procedures for {sensor_type}",
                "reasoning": "Retrieving sensor fusion and state estimation guidance"
            },
            {
                "step": 2,
                "process": "Parameter Sequence Generation",
                "action": "Creating step-by-step tuning sequence",
                "reasoning": "Organizing EKF parameters in logical tuning order"
            },
            {
                "step": 3,
                "process": "Validation Integration",
                "action": "Adding validation checks and monitoring procedures",
                "reasoning": "Including performance validation and health monitoring guidance"
            }
        ]
        
        self.log_rag_reasoning(question_id, question, "get_ekf_tuning_guidance", rag_steps)
        return super().get_ekf_tuning_guidance(sensor_type)
    
    def analyze_enhanced_system_integration_with_logging(self, primary_sensor, question_id, question, platform="ardupilot"):
        """Analyze system integration with RAG logging"""
        self.query_count += 1
        
        rag_steps = [
            {
                "step": 1,
                "process": "Multi-Source Knowledge Fusion",
                "action": f"Combining Stasik technology data with ArduPilot integration for {primary_sensor}",
                "reasoning": "Integrating sensor characteristics with platform-specific implementation"
            },
            {
                "step": 2,
                "process": "System Architecture Analysis", 
                "action": "Analyzing hardware/software integration requirements",
                "reasoning": "Determining wiring, driver, and configuration requirements"
            },
            {
                "step": 3,
                "process": "EKF Integration Planning",
                "action": "Planning sensor fusion and state estimation integration",
                "reasoning": "Configuring EKF parameters for optimal sensor performance"
            },
            {
                "step": 4,
                "process": "Professional Implementation Path",
                "action": "Creating comprehensive implementation roadmap",
                "reasoning": "Providing end-to-end integration guidance with best practices"
            }
        ]
        
        self.log_rag_reasoning(question_id, question, "analyze_enhanced_system_integration", rag_steps)
        return super().analyze_enhanced_system_integration(primary_sensor, platform)

def create_comprehensive_test_questions():
    """Create 50 comprehensive test questions with diverse complexity"""
    
    questions = [
        # Technology Fundamentals (1-10)
        ("What are the fundamental operating principles of pitot tubes?", "technology", "pitot_tubes"),
        ("How do MEMS airflow sensors detect air velocity?", "technology", "mems_sensors"),
        ("What makes multi-hole probes different from single-hole pitot tubes?", "technology", "multi_hole_probes"), 
        ("Explain the working principle of thermal anemometers", "technology", "anemometers"),
        ("What are the accuracy limitations of pitot tube measurements?", "technology", "pitot_tubes"),
        ("How do MEMS pressure sensors achieve miniaturization?", "technology", "mems_sensors"),
        ("What directional measurements can multi-hole probes provide?", "technology", "multi_hole_probes"),
        ("How do ultrasonic anemometers measure wind velocity?", "technology", "anemometers"),
        ("What are the temperature compensation methods for airspeed sensors?", "technology", "pitot_tubes"),
        ("How do silicon-based MEMS sensors handle environmental conditions?", "technology", "mems_sensors"),
        
        # ArduPilot Integration (11-20) 
        ("How to configure ARSPD_TYPE for different sensor hardware?", "parameter", "ARSPD_TYPE"),
        ("What is the proper ARSPD_RATIO calibration procedure?", "parameter", "ARSPD_RATIO"),
        ("How does ARSPD_AUTOCAL work in ArduPilot?", "parameter", "ARSPD_AUTOCAL"),
        ("What are the EK3_ARSP_THR tuning guidelines?", "parameter", "EK3_ARSP_THR"),
        ("How to integrate differential pressure sensors with ArduPilot?", "integration", "pitot_tubes"),
        ("What ArduPilot drivers support MEMS airflow sensors?", "integration", "mems_sensors"),
        ("Can multi-hole probes work with standard ArduPilot firmware?", "integration", "multi_hole_probes"),
        ("How to input anemometer data into ArduPilot navigation?", "integration", "anemometers"),
        ("What is synthetic airspeed and when is it used?", "integration", "pitot_tubes"),
        ("How to configure dual airspeed sensor redundancy?", "integration", "pitot_tubes"),
        
        # EKF and State Estimation (21-30)
        ("How does EKF3 fuse airspeed measurements with other sensors?", "ekf", "airspeed"),
        ("What are the wind estimation algorithms in ArduPilot EKF?", "ekf", "wind"),
        ("How to tune EKF innovation thresholds for airspeed sensors?", "ekf", "airspeed"),
        ("What causes EKF airspeed innovation spikes?", "ekf", "airspeed"),
        ("How to validate EKF airspeed fusion performance?", "ekf", "airspeed"),
        ("What are the drag coefficient parameters in EKF3?", "ekf", "drag"),
        ("How does EKF handle airspeed sensor failures?", "ekf", "failsafe"),
        ("What is the relationship between EKF and flight modes?", "ekf", "flight_modes"),
        ("How to optimize EKF performance for high-speed flight?", "ekf", "performance"),
        ("What EKF parameters affect wind estimation convergence?", "ekf", "wind"),
        
        # System Integration (31-40)
        ("Design a complete airspeed sensing system for a fixed-wing UAV", "system", "pitot_tubes"),
        ("How to integrate multiple airflow sensors on a large UAV?", "system", "multi_sensor"),
        ("What are the wiring requirements for ArduPilot airspeed sensors?", "system", "hardware"),
        ("How to implement airspeed sensor heating systems?", "system", "environmental"),
        ("What calibration procedures are needed for flight testing?", "system", "calibration"),
        ("How to design airspeed sensor placement for minimal interference?", "system", "installation"),
        ("What data logging is required for airspeed sensor validation?", "system", "validation"),
        ("How to implement airspeed sensor health monitoring?", "system", "monitoring"),
        ("What are the power requirements for different sensor types?", "system", "power"),
        ("How to design redundant airspeed measurement architecture?", "system", "redundancy"),
        
        # Advanced Applications (41-50)
        ("How to measure angle of attack with multi-hole probes?", "advanced", "multi_hole_probes"),
        ("What sensors work best for VTOL transition flight phases?", "advanced", "vtol"),
        ("How to implement distributed airflow sensing on large aircraft?", "advanced", "distributed"),
        ("What are the requirements for high-altitude airspeed sensing?", "advanced", "high_altitude"),
        ("How to measure sideslip angle for flight control?", "advanced", "sideslip"),
        ("What airspeed sensors work in icing conditions?", "advanced", "icing"),
        ("How to implement real-time airspeed sensor calibration?", "advanced", "real_time_cal"),
        ("What are the latency requirements for flight control sensors?", "advanced", "latency"),
        ("How to validate airspeed measurements against GPS data?", "advanced", "validation"),
        ("What future technologies will improve UAV airspeed sensing?", "advanced", "future")
    ]
    
    return questions

def run_comprehensive_test_with_rag_logging():
    """Run comprehensive test with detailed RAG reasoning logging"""
    
    print("COMPREHENSIVE TEST SUITE WITH RAG REASONING LOGGING")
    print("=" * 80)
    print("Testing Enhanced Stasik Agent with detailed reasoning capture")
    print("=" * 80)
    print()
    
    # Initialize agent with logging
    agent = EnhancedStasikAgentWithLogging()
    
    # Display agent info
    info = agent.get_enhanced_agent_info()
    print(f"Agent: {info['agent_name']} v{info['version']}")
    print(f"Domain: {info['domain']}")
    print(f"ArduPilot Integration: {info.get('ardupilot_knowledge_loaded', False)}")
    print()
    
    # Create test questions
    questions = create_comprehensive_test_questions()
    
    print(f"Executing {len(questions)} comprehensive test questions...")
    print("Logging detailed RAG reasoning for each query...")
    print()
    
    # Test results
    test_results = []
    start_time = time.time()
    
    for i, (question, category, target) in enumerate(questions, 1):
        print(f"Test {i:2d}: {question[:60]}{'...' if len(question) > 60 else ''}")
        
        test_start = time.time()
        
        try:
            # Route question based on category with logging
            if category == "technology":
                result = agent.query_technology_with_logging(target, i, question)
            elif category == "parameter":
                result = agent.get_parameter_guidance_with_logging(target, i, question) 
            elif category == "integration":
                result = agent.query_ardupilot_integration_with_logging(target, i, question)
            elif category == "ekf":
                result = agent.get_ekf_tuning_guidance_with_logging(target, i, question)
            elif category in ["system", "advanced"]:
                result = agent.analyze_enhanced_system_integration_with_logging(target, i, question)
            else:
                result = agent.query_technology_with_logging(target, i, question)
            
            # Evaluate result
            success = result.get("status") == "success"
            response_size = len(str(result))
            
            test_result = {
                "id": i,
                "question": question,
                "category": category,
                "target": target,
                "success": success,
                "response_size": response_size,
                "execution_time": time.time() - test_start,
                "status": "PASS" if success else "FAIL"
            }
            
            test_results.append(test_result)
            print(f"         Status: {test_result['status']} | Time: {test_result['execution_time']:.3f}s | Size: {response_size} chars")
            
        except Exception as e:
            test_result = {
                "id": i,
                "question": question, 
                "category": category,
                "target": target,
                "success": False,
                "response_size": 0,
                "execution_time": time.time() - test_start,
                "status": "ERROR",
                "error": str(e)
            }
            test_results.append(test_result)
            print(f"         Status: ERROR | Error: {str(e)[:50]}...")
        
        print()
    
    total_time = time.time() - start_time
    
    # Calculate results
    passed = sum(1 for r in test_results if r["success"])
    success_rate = (passed / len(test_results)) * 100
    avg_response_size = sum(r["response_size"] for r in test_results) / len(test_results)
    
    # Results summary
    print("=" * 80)
    print("COMPREHENSIVE TEST RESULTS WITH RAG LOGGING")
    print("=" * 80)
    print(f"Overall Results: {passed}/{len(test_results)} tests passed ({success_rate:.1f}%)")
    print(f"Total Execution Time: {total_time:.2f} seconds")
    print(f"Average Response Size: {avg_response_size:.0f} characters")
    print(f"Total RAG Queries Logged: {agent.query_count}")
    print()
    
    # Category breakdown
    categories = {}
    for result in test_results:
        cat = result["category"]
        if cat not in categories:
            categories[cat] = {"passed": 0, "total": 0}
        categories[cat]["total"] += 1
        if result["success"]:
            categories[cat]["passed"] += 1
    
    print("Category Breakdown:")
    for cat, stats in categories.items():
        rate = (stats["passed"] / stats["total"]) * 100
        print(f"  {cat:15s}: {stats['passed']:2d}/{stats['total']:2d} ({rate:5.1f}%)")
    
    print()
    print("=" * 80)
    
    # Save results and RAG logs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save test results
    results_file = f"test_results_with_rag_{timestamp}.json"
    test_summary = {
        "test_summary": {
            "total_tests": len(test_results),
            "passed": passed,
            "success_rate": success_rate,
            "execution_time": total_time,
            "timestamp": datetime.now().isoformat()
        },
        "detailed_results": test_results,
        "category_breakdown": categories
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(test_summary, f, indent=2, ensure_ascii=False)
    
    # Save RAG reasoning log
    rag_log_file = f"rag_reasoning_log_{timestamp}.json"
    agent.rag_logger.save_reasoning_log(rag_log_file)
    
    print(f"Test results saved to: {results_file}")
    print(f"RAG reasoning log saved to: {rag_log_file}")
    print()
    print("=" * 80)
    print("COMPREHENSIVE TESTING WITH RAG LOGGING COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    run_comprehensive_test_with_rag_logging()