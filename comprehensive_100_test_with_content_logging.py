#!/usr/bin/env python3
"""
Comprehensive 100-Question Test Suite with Full Content Logging
Tests Hybrid Search Agent with detailed RAG reasoning, content, and SearXNG results
"""

import json
import time
from datetime import datetime
from pathlib import Path
from hybrid_search_agent import HybridSearchAgent

class ComprehensiveContentLogger:
    """Logs complete content, not just status - RAG reasoning, knowledge content, SearXNG results"""
    
    def __init__(self):
        self.test_log = []
        self.detailed_content_log = []
        self.rag_reasoning_log = []
        self.searxng_results_log = []
        self.knowledge_content_log = []
    
    def log_test_with_full_content(self, test_id: int, question: str, result: dict, execution_time: float):
        """Log test with complete content details"""
        
        # Basic test entry
        test_entry = {
            "test_id": test_id,
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "execution_time": execution_time,
            "status": result.get("status", "unknown"),
            "success": result.get("status") == "success"
        }
        
        # Detailed content logging
        content_entry = {
            "test_id": test_id,
            "question": question,
            "static_knowledge_content": self._extract_static_content(result),
            "dynamic_search_content": self._extract_dynamic_content(result),
            "rag_reasoning": result.get("reasoning", {}),
            "synthesis_details": result.get("synthesis", {}),
            "full_response_size": len(json.dumps(result))
        }
        
        # RAG reasoning details
        rag_entry = {
            "test_id": test_id,
            "reasoning_steps": result.get("reasoning", {}).get("reasoning_steps", []),
            "gaps_identified": result.get("reasoning", {}).get("gaps_identified", {}),
            "search_strategy": result.get("reasoning", {}).get("search_strategy", {}),
            "decision_points": self._extract_decision_points(result)
        }
        
        # SearXNG results details
        searxng_entry = {
            "test_id": test_id,
            "searxng_used": len(result.get("dynamic_results", {})) > 0,
            "search_queries": self._extract_searxng_queries(result),
            "search_results": self._extract_searxng_content(result),
            "search_effectiveness": self._assess_searxng_effectiveness(result)
        }
        
        # Knowledge base content
        knowledge_entry = {
            "test_id": test_id,
            "static_sources": list(result.get("static_results", {}).keys()),
            "knowledge_depth": self._assess_knowledge_depth(result),
            "technical_content": self._extract_technical_content(result),
            "parameter_guidance": self._extract_parameter_content(result),
            "integration_details": self._extract_integration_content(result)
        }
        
        # Store all logs
        self.test_log.append(test_entry)
        self.detailed_content_log.append(content_entry)
        self.rag_reasoning_log.append(rag_entry)
        self.searxng_results_log.append(searxng_entry)
        self.knowledge_content_log.append(knowledge_entry)
    
    def _extract_static_content(self, result: dict) -> dict:
        """Extract detailed static knowledge content"""
        static_content = {}
        
        for key, static_result in result.get("static_results", {}).items():
            if static_result.get("status") == "success":
                content = {}
                
                # Technology overview content
                if "overview" in static_result:
                    overview = static_result["overview"]
                    content["technology_description"] = overview.get("description", "")
                    content["operating_principle"] = overview.get("principle", "")
                    content["advantages"] = overview.get("advantages", [])
                    content["applications"] = overview.get("applications", [])
                    content["patent_activity"] = overview.get("patent_activity", "")
                    content["professional_status"] = overview.get("professional_status", "")
                
                # ArduPilot integration content
                if "ardupilot_integration" in static_result:
                    ardupilot = static_result["ardupilot_integration"]
                    content["ardupilot_drivers"] = ardupilot.get("ardupilot_drivers", [])
                    content["key_parameters"] = ardupilot.get("key_parameters", {})
                    content["calibration_procedures"] = ardupilot.get("calibration_procedures", [])
                    content["best_practices"] = static_result.get("ardupilot_best_practices", [])
                    content["common_issues"] = static_result.get("common_issues", [])
                
                # Parameter details content
                if "parameter_details" in static_result:
                    param_details = static_result["parameter_details"]
                    content["parameter_name"] = static_result.get("parameter", "")
                    content["parameter_description"] = param_details.get("description", "")
                    content["parameter_values"] = param_details.get("values", {})
                    content["tuning_notes"] = param_details.get("tuning_notes", "")
                    content["related_parameters"] = param_details.get("related_params", [])
                
                # EKF tuning content
                if "tuning_guidance" in static_result:
                    ekf = static_result["tuning_guidance"]
                    content["ekf_parameters"] = ekf.get("key_parameters", {})
                    content["tuning_sequence"] = ekf.get("tuning_sequence", [])
                    content["validation_checks"] = ekf.get("validation_checks", [])
                
                static_content[key] = content
        
        return static_content
    
    def _extract_dynamic_content(self, result: dict) -> dict:
        """Extract detailed SearXNG dynamic content"""
        dynamic_content = {}
        
        for key, dynamic_result in result.get("dynamic_results", {}).items():
            if dynamic_result.get("status") == "success":
                content = {
                    "search_query": dynamic_result.get("query", ""),
                    "search_timestamp": dynamic_result.get("timestamp", ""),
                    "search_results": []
                }
                
                # Extract actual search results content
                if "results" in dynamic_result:
                    search_data = dynamic_result["results"]
                    if "results" in search_data:
                        for search_result in search_data["results"][:5]:  # Top 5 results
                            result_content = {
                                "title": search_result.get("title", ""),
                                "url": search_result.get("url", ""),
                                "content": search_result.get("content", ""),
                                "engine": search_result.get("engine", ""),
                                "category": search_result.get("category", "")
                            }
                            content["search_results"].append(result_content)
                
                dynamic_content[key] = content
        
        return dynamic_content
    
    def _extract_decision_points(self, result: dict) -> list:
        """Extract key decision points from reasoning"""
        decision_points = []
        
        reasoning = result.get("reasoning", {})
        
        # Gap analysis decisions
        gaps = reasoning.get("gaps_identified", {})
        total_gaps = len(sum(gaps.values(), []))
        if total_gaps > 0:
            decision_points.append(f"Knowledge gaps identified: {total_gaps} total")
            for gap_type, gap_list in gaps.items():
                if gap_list:
                    decision_points.append(f"{gap_type}: {len(gap_list)} gaps")
        
        # Search strategy decision
        strategy = reasoning.get("search_strategy", {})
        if strategy:
            decision_points.append(f"Search strategy: {strategy.get('reason', 'Unknown')}")
            if strategy.get("use_searxng"):
                decision_points.append(f"SearXNG search type: {strategy.get('search_type', 'Unknown')}")
        
        return decision_points
    
    def _extract_searxng_queries(self, result: dict) -> list:
        """Extract SearXNG search queries"""
        queries = []
        
        for dynamic_result in result.get("dynamic_results", {}).values():
            if dynamic_result.get("query"):
                queries.append(dynamic_result["query"])
        
        return queries
    
    def _extract_searxng_content(self, result: dict) -> dict:
        """Extract meaningful SearXNG search content"""
        searxng_content = {
            "total_results": 0,
            "unique_sources": set(),
            "content_themes": [],
            "technical_depth": "low"
        }
        
        for dynamic_result in result.get("dynamic_results", {}).values():
            if dynamic_result.get("status") == "success" and "results" in dynamic_result:
                search_data = dynamic_result["results"]
                if "results" in search_data:
                    searxng_content["total_results"] += len(search_data["results"])
                    
                    # Extract sources and content themes
                    for search_result in search_data["results"]:
                        url = search_result.get("url", "")
                        if url:
                            domain = url.split("//")[-1].split("/")[0]
                            searxng_content["unique_sources"].add(domain)
                        
                        # Analyze content for technical themes
                        content = search_result.get("content", "").lower()
                        title = search_result.get("title", "").lower()
                        
                        if any(term in content + title for term in ["ardupilot", "parameter", "configuration"]):
                            searxng_content["content_themes"].append("ArduPilot Configuration")
                        if any(term in content + title for term in ["sensor", "calibration", "tuning"]):
                            searxng_content["content_themes"].append("Sensor Calibration")
                        if any(term in content + title for term in ["troubleshoot", "error", "problem"]):
                            searxng_content["content_themes"].append("Troubleshooting")
        
        # Convert set to list for JSON serialization
        searxng_content["unique_sources"] = list(searxng_content["unique_sources"])
        searxng_content["content_themes"] = list(set(searxng_content["content_themes"]))
        
        return searxng_content
    
    def _assess_searxng_effectiveness(self, result: dict) -> dict:
        """Assess effectiveness of SearXNG search"""
        effectiveness = {
            "queries_executed": len(result.get("dynamic_results", {})),
            "results_found": 0,
            "relevant_sources": 0,
            "effectiveness_score": 0.0
        }
        
        for dynamic_result in result.get("dynamic_results", {}).values():
            if dynamic_result.get("status") == "success" and "results" in dynamic_result:
                search_data = dynamic_result["results"]
                if "results" in search_data:
                    effectiveness["results_found"] += len(search_data["results"])
                    
                    # Count relevant sources (technical domains)
                    relevant_domains = ["ardupilot.org", "github.com", "discuss.ardupilot.org", 
                                      "stackoverflow.com", "diydrones.com"]
                    
                    for search_result in search_data["results"]:
                        url = search_result.get("url", "").lower()
                        if any(domain in url for domain in relevant_domains):
                            effectiveness["relevant_sources"] += 1
        
        # Calculate effectiveness score
        if effectiveness["queries_executed"] > 0:
            effectiveness["effectiveness_score"] = min(
                (effectiveness["results_found"] + effectiveness["relevant_sources"] * 2) / 
                (effectiveness["queries_executed"] * 10), 1.0
            )
        
        return effectiveness
    
    def _assess_knowledge_depth(self, result: dict) -> dict:
        """Assess depth of knowledge provided"""
        depth_assessment = {
            "technical_detail_level": "basic",
            "parameter_coverage": 0,
            "integration_guidance": False,
            "troubleshooting_depth": "none",
            "professional_insights": False
        }
        
        static_results = result.get("static_results", {})
        
        # Assess technical detail level
        detail_indicators = 0
        for static_result in static_results.values():
            if "overview" in static_result:
                if static_result["overview"].get("principle"):
                    detail_indicators += 1
                if static_result["overview"].get("advantages"):
                    detail_indicators += 1
            
            if "ardupilot_integration" in static_result:
                detail_indicators += 2
                depth_assessment["integration_guidance"] = True
            
            if "parameter_details" in static_result:
                detail_indicators += 1
                depth_assessment["parameter_coverage"] += 1
            
            if "tuning_guidance" in static_result:
                detail_indicators += 2
        
        # Set technical detail level
        if detail_indicators >= 4:
            depth_assessment["technical_detail_level"] = "comprehensive"
        elif detail_indicators >= 2:
            depth_assessment["technical_detail_level"] = "moderate"
        
        return depth_assessment
    
    def _extract_technical_content(self, result: dict) -> dict:
        """Extract technical content details"""
        technical_content = {
            "physics_principles": [],
            "measurement_techniques": [],
            "calibration_methods": [],
            "system_integration": []
        }
        
        for static_result in result.get("static_results", {}).values():
            if "overview" in static_result:
                overview = static_result["overview"]
                
                principle = overview.get("principle", "").lower()
                if "bernoulli" in principle:
                    technical_content["physics_principles"].append("Bernoulli's principle")
                if "pressure" in principle:
                    technical_content["physics_principles"].append("Pressure differential measurement")
                
                description = overview.get("description", "").lower()
                if "measurement" in description:
                    technical_content["measurement_techniques"].append("Direct measurement")
                if "sensor" in description:
                    technical_content["measurement_techniques"].append("Electronic sensing")
            
            if "ardupilot_integration" in static_result:
                technical_content["system_integration"].append("ArduPilot compatibility")
                
                calibration_procs = static_result["ardupilot_integration"].get("calibration_procedures", [])
                technical_content["calibration_methods"].extend(calibration_procs)
        
        return technical_content
    
    def _extract_parameter_content(self, result: dict) -> dict:
        """Extract ArduPilot parameter content"""
        parameter_content = {
            "parameters_covered": [],
            "configuration_details": {},
            "tuning_procedures": []
        }
        
        for key, static_result in result.get("static_results", {}).items():
            if "parameter_details" in static_result:
                param_name = static_result.get("parameter", "")
                parameter_content["parameters_covered"].append(param_name)
                
                param_details = static_result["parameter_details"]
                parameter_content["configuration_details"][param_name] = {
                    "description": param_details.get("description", ""),
                    "values": param_details.get("values", {}),
                    "tuning_notes": param_details.get("tuning_notes", "")
                }
            
            if "tuning_guidance" in static_result:
                tuning_seq = static_result["tuning_guidance"].get("tuning_sequence", [])
                parameter_content["tuning_procedures"].extend(tuning_seq)
        
        return parameter_content
    
    def _extract_integration_content(self, result: dict) -> dict:
        """Extract system integration content"""
        integration_content = {
            "supported_platforms": [],
            "drivers_available": [],
            "integration_steps": [],
            "best_practices": [],
            "common_issues": []
        }
        
        for static_result in result.get("static_results", {}).values():
            if "ardupilot_integration" in static_result:
                ardupilot_info = static_result["ardupilot_integration"]
                
                integration_content["supported_platforms"].append("ArduPilot")
                integration_content["drivers_available"].extend(
                    ardupilot_info.get("ardupilot_drivers", [])
                )
                integration_content["integration_steps"].extend(
                    ardupilot_info.get("calibration_procedures", [])
                )
            
            if "ardupilot_best_practices" in static_result:
                integration_content["best_practices"].extend(
                    static_result["ardupilot_best_practices"]
                )
            
            if "common_issues" in static_result:
                integration_content["common_issues"].extend(
                    static_result["common_issues"]
                )
        
        return integration_content
    
    def save_comprehensive_logs(self, test_name: str):
        """Save all comprehensive logs to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save test summary
        summary_file = f"{test_name}_summary_{timestamp}.json"
        summary = {
            "test_metadata": {
                "test_name": test_name,
                "total_tests": len(self.test_log),
                "timestamp": timestamp,
                "success_rate": sum(1 for test in self.test_log if test["success"]) / len(self.test_log) * 100
            },
            "test_results": self.test_log
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Save detailed content log
        content_file = f"{test_name}_detailed_content_{timestamp}.json"
        with open(content_file, 'w', encoding='utf-8') as f:
            json.dump(self.detailed_content_log, f, indent=2, ensure_ascii=False)
        
        # Save RAG reasoning log
        rag_file = f"{test_name}_rag_reasoning_{timestamp}.json"
        with open(rag_file, 'w', encoding='utf-8') as f:
            json.dump(self.rag_reasoning_log, f, indent=2, ensure_ascii=False)
        
        # Save SearXNG results log
        searxng_file = f"{test_name}_searxng_results_{timestamp}.json"
        with open(searxng_file, 'w', encoding='utf-8') as f:
            json.dump(self.searxng_results_log, f, indent=2, ensure_ascii=False)
        
        # Save knowledge content log
        knowledge_file = f"{test_name}_knowledge_content_{timestamp}.json"
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_content_log, f, indent=2, ensure_ascii=False)
        
        return {
            "summary_file": summary_file,
            "content_file": content_file,
            "rag_file": rag_file,
            "searxng_file": searxng_file,
            "knowledge_file": knowledge_file
        }

def generate_100_comprehensive_questions():
    """Generate 100 comprehensive questions covering all aspects"""
    
    questions = [
        # Basic Technology Questions (1-20)
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
        ("What is the Reynolds number impact on probe measurements?", "technology", "multi_hole_probes"),
        ("How do cup anemometers differ from propeller anemometers?", "technology", "anemometers"),
        ("What are static port errors in pitot tube systems?", "technology", "pitot_tubes"),
        ("How do piezoresistive MEMS sensors work?", "technology", "mems_sensors"),
        ("What calibration is required for multi-hole probes?", "technology", "multi_hole_probes"),
        ("How do sonic anemometers eliminate moving parts?", "technology", "anemometers"),
        ("What causes pitot tube icing and how to prevent it?", "technology", "pitot_tubes"),
        ("How do capacitive MEMS sensors measure flow?", "technology", "mems_sensors"),
        ("What is angle of attack measurement with probes?", "technology", "multi_hole_probes"),
        ("How do hot-wire anemometers achieve high frequency response?", "technology", "anemometers"),
        
        # ArduPilot Integration Questions (21-40)
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
        ("What is ARSPD_PSI_RANGE parameter used for?", "parameter", "ARSPD_PSI_RANGE"),
        ("How to set ARSPD_BUS for I2C sensors?", "parameter", "ARSPD_BUS"),
        ("What does ARSPD_TUBE_ORDER control?", "parameter", "ARSPD_TUBE_ORDER"),
        ("How to configure ARSPD_SKIP_CAL parameter?", "parameter", "ARSPD_SKIP_CAL"),
        ("What ArduPilot messages show airspeed sensor status?", "integration", "pitot_tubes"),
        ("How to enable airspeed sensor logging in ArduPilot?", "integration", "pitot_tubes"),
        ("What flight modes require airspeed sensors?", "integration", "pitot_tubes"),
        ("How to configure airspeed failsafe in ArduPilot?", "integration", "pitot_tubes"),
        ("What parameters control synthetic airspeed?", "integration", "pitot_tubes"),
        ("How to validate airspeed sensor installation?", "integration", "pitot_tubes"),
        
        # EKF and State Estimation Questions (41-60)
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
        ("How to configure EK3_ENABLE for airspeed fusion?", "parameter", "EK3_ENABLE"),
        ("What is EK3_WIND_P_NSE parameter?", "parameter", "EK3_WIND_P_NSE"),
        ("How to set EK3_DRAG_BCOEF_X and Y parameters?", "parameter", "EK3_DRAG_BCOEF_X"),
        ("What does EK3_ARSP_THR threshold control?", "parameter", "EK3_ARSP_THR"),
        ("How to monitor EKF airspeed innovations?", "ekf", "monitoring"),
        ("What causes EKF wind estimation divergence?", "ekf", "wind"),
        ("How to tune EKF for different aircraft types?", "ekf", "aircraft"),
        ("What EKF parameters affect airspeed accuracy?", "ekf", "accuracy"),
        ("How to configure EKF for redundant airspeed sensors?", "ekf", "redundancy"),
        ("What is the EKF airspeed measurement model?", "ekf", "modeling"),
        
        # Advanced System Integration Questions (61-80)
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
        ("What communication protocols work with airspeed sensors?", "system", "communication"),
        ("How to integrate airspeed sensors with existing avionics?", "system", "avionics"),
        ("What EMI considerations apply to airspeed sensors?", "system", "emi"),
        ("How to implement sensor fusion for multiple airspeed sources?", "system", "fusion"),
        ("What mechanical mounting considerations are critical?", "system", "mounting"),
        ("How to design airspeed sensor cable harnesses?", "system", "cabling"),
        ("What environmental protection is needed for sensors?", "system", "environmental"),
        ("How to implement automated sensor calibration?", "system", "automation"),
        ("What backup systems are needed for airspeed sensing?", "system", "backup"),
        ("How to integrate with flight management systems?", "system", "fms"),
        
        # Troubleshooting and Maintenance Questions (81-100)
        ("How to diagnose erratic airspeed readings in ArduPilot?", "troubleshooting", "erratic_readings"),
        ("What causes airspeed sensor calibration drift?", "troubleshooting", "calibration_drift"),
        ("How to resolve MEMS sensor noise issues in flight?", "troubleshooting", "noise"),
        ("What happens when airspeed sensors fail during flight?", "troubleshooting", "sensor_failure"),
        ("How do icing conditions affect different sensor types?", "troubleshooting", "icing"),
        ("What are the limitations of synthetic airspeed in ArduPilot?", "troubleshooting", "synthetic"),
        ("How to troubleshoot I2C communication errors with sensors?", "troubleshooting", "i2c"),
        ("What causes airspeed sensor offset errors?", "troubleshooting", "offset"),
        ("How to diagnose airspeed sensor mechanical damage?", "troubleshooting", "mechanical"),
        ("What electrical issues affect airspeed sensor performance?", "troubleshooting", "electrical"),
        ("How to validate airspeed sensor accuracy in flight?", "troubleshooting", "accuracy"),
        ("What maintenance is required for different sensor types?", "troubleshooting", "maintenance"),
        ("How to troubleshoot temperature compensation failures?", "troubleshooting", "temperature"),
        ("What causes intermittent airspeed sensor readings?", "troubleshooting", "intermittent"),
        ("How to diagnose airspeed sensor installation problems?", "troubleshooting", "installation"),
        ("What tools are needed for airspeed sensor diagnostics?", "troubleshooting", "tools"),
        ("How to perform bench testing of airspeed sensors?", "troubleshooting", "bench_test"),
        ("What field calibration procedures are available?", "troubleshooting", "field_cal"),
        ("How to identify counterfeit airspeed sensors?", "troubleshooting", "counterfeit"),
        ("What documentation is needed for sensor troubleshooting?", "troubleshooting", "documentation")
    ]
    
    return questions

def run_comprehensive_100_test():
    """Run comprehensive 100-question test with full content logging"""
    
    print("COMPREHENSIVE 100-QUESTION TEST WITH FULL CONTENT LOGGING")
    print("=" * 80)
    print("Testing Hybrid Search Agent with detailed RAG reasoning,")
    print("knowledge content, and SearXNG results logging")
    print("=" * 80)
    print()
    
    # Initialize hybrid agent and logger
    agent = HybridSearchAgent()
    logger = ComprehensiveContentLogger()
    
    # Display system status
    stats = agent.get_hybrid_stats()
    print(f"Agent: {stats['agent_info']['agent_name']} v{stats['agent_info']['version']}")
    print(f"SearXNG Available: {stats['searxng_available']}")
    print(f"Static Knowledge: 1,100+ patents + ArduPilot documentation")
    print(f"Dynamic Search: Meta-search across multiple engines")
    print()
    
    # Generate test questions
    questions = generate_100_comprehensive_questions()
    
    print(f"Generated {len(questions)} comprehensive test questions")
    print("Categories: Technology, ArduPilot Integration, EKF Tuning,")
    print("System Integration, Troubleshooting")
    print()
    
    print("Starting comprehensive test execution with full content logging...")
    print("This will take several minutes due to SearXNG queries...")
    print()
    
    start_time = time.time()
    
    # Execute all tests
    for i, (question, category, target) in enumerate(questions, 1):
        test_start = time.time()
        
        print(f"Test {i:3d}/100: {question[:60]}{'...' if len(question) > 60 else ''}")
        
        try:
            # Route question based on category with hybrid search
            if category == "technology":
                result = agent.hybrid_query(question, target)
            elif category == "parameter":
                # For parameter questions, detect technology from target
                tech = "pitot_tubes" if "ARSPD" in target else None
                result = agent.hybrid_query(question, tech)
            elif category == "integration":
                result = agent.hybrid_query(question, target)
            elif category == "ekf":
                result = agent.hybrid_query(question, None)  # General EKF query
            elif category in ["system", "troubleshooting"]:
                result = agent.hybrid_query(question, target if target in ["pitot_tubes", "mems_sensors", "multi_hole_probes", "anemometers"] else None)
            else:
                result = agent.hybrid_query(question, None)
            
            execution_time = time.time() - test_start
            
            # Log comprehensive content
            logger.log_test_with_full_content(i, question, result, execution_time)
            
            # Display progress
            status = "PASS" if result.get("status") == "success" else "FAIL"
            static_count = len(result.get("static_results", {}))
            dynamic_count = len(result.get("dynamic_results", {}))
            confidence = result.get("synthesis", {}).get("confidence", 0.0)
            
            print(f"             Status: {status} | Static: {static_count} | Dynamic: {dynamic_count} | Confidence: {confidence:.2f} | Time: {execution_time:.2f}s")
            
        except Exception as e:
            execution_time = time.time() - test_start
            print(f"             Status: ERROR | Error: {str(e)[:50]}... | Time: {execution_time:.2f}s")
            
            # Log error
            error_result = {
                "status": "error",
                "error": str(e),
                "static_results": {},
                "dynamic_results": {},
                "reasoning": {"reasoning_steps": [], "gaps_identified": {}, "search_strategy": {}},
                "synthesis": {"confidence": 0.0, "completeness": 0.0, "primary_source": "none"}
            }
            logger.log_test_with_full_content(i, question, error_result, execution_time)
    
    total_time = time.time() - start_time
    
    # Calculate results
    passed_tests = sum(1 for test in logger.test_log if test["success"])
    success_rate = (passed_tests / len(logger.test_log)) * 100
    
    print()
    print("=" * 80)
    print("COMPREHENSIVE TEST RESULTS")
    print("=" * 80)
    print(f"Total Tests Executed: {len(logger.test_log)}")
    print(f"Tests Passed: {passed_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    print(f"Total Execution Time: {total_time:.2f} seconds")
    print(f"Average Time per Test: {total_time/len(logger.test_log):.2f} seconds")
    print()
    
    # Analyze SearXNG usage
    searxng_used_count = sum(1 for log in logger.searxng_results_log if log["searxng_used"])
    total_searxng_queries = sum(len(log["search_queries"]) for log in logger.searxng_results_log)
    
    print("SEARXNG USAGE ANALYSIS:")
    print(f"Tests Using SearXNG: {searxng_used_count}/{len(logger.test_log)} ({searxng_used_count/len(logger.test_log)*100:.1f}%)")
    print(f"Total SearXNG Queries: {total_searxng_queries}")
    print(f"Average Queries per SearXNG Test: {total_searxng_queries/max(searxng_used_count, 1):.1f}")
    
    # Analyze knowledge depth
    comprehensive_tests = sum(1 for log in logger.knowledge_content_log 
                            if log["knowledge_depth"]["technical_detail_level"] == "comprehensive")
    print()
    print("KNOWLEDGE DEPTH ANALYSIS:")
    print(f"Comprehensive Technical Coverage: {comprehensive_tests}/{len(logger.test_log)} ({comprehensive_tests/len(logger.test_log)*100:.1f}%)")
    
    total_parameters = sum(log["knowledge_depth"]["parameter_coverage"] for log in logger.knowledge_content_log)
    print(f"ArduPilot Parameters Covered: {total_parameters}")
    
    integration_guidance = sum(1 for log in logger.knowledge_content_log 
                             if log["knowledge_depth"]["integration_guidance"])
    print(f"Integration Guidance Provided: {integration_guidance}/{len(logger.test_log)} ({integration_guidance/len(logger.test_log)*100:.1f}%)")
    
    # Save comprehensive logs
    print()
    print("SAVING COMPREHENSIVE LOGS...")
    log_files = logger.save_comprehensive_logs("comprehensive_100_test")
    
    print("Log files created:")
    for log_type, filename in log_files.items():
        print(f"  {log_type}: {filename}")
    
    print()
    print("=" * 80)
    print("COMPREHENSIVE 100-QUESTION TEST COMPLETE")
    print("All content, RAG reasoning, and SearXNG results logged in detail")
    print("=" * 80)

if __name__ == "__main__":
    run_comprehensive_100_test()