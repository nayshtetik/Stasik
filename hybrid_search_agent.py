#!/usr/bin/env python3
"""
Hybrid Search Agent with Intermediary Reasoning
Combines static knowledge base with SearXNG for comprehensive coverage
"""

import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from enhanced_stasik_agent import EnhancedStasikAgent

class IntermediaryReasoning:
    """Handles reasoning steps and gap analysis between static and dynamic search"""
    
    def __init__(self):
        self.reasoning_log = []
        self.decision_points = []
    
    def log_reasoning_step(self, step_type: str, description: str, data: Any = None):
        """Log a reasoning step"""
        step = {
            "timestamp": datetime.now().isoformat(),
            "step_type": step_type,
            "description": description,
            "data": data
        }
        self.reasoning_log.append(step)
    
    def analyze_knowledge_gaps(self, static_results: Dict, query: str) -> Dict[str, Any]:
        """Analyze gaps in static knowledge that need dynamic search"""
        
        self.log_reasoning_step("gap_analysis", f"Analyzing static results for query: {query}")
        
        gaps = {
            "temporal_gaps": [],
            "coverage_gaps": [],
            "specificity_gaps": [],
            "update_needs": []
        }
        
        # Check temporal gaps (outdated information)
        current_year = datetime.now().year
        for key, result in static_results.items():
            if result.get("status") == "success":
                # Check for outdated patent data
                if "patent_activity" in str(result):
                    gaps["temporal_gaps"].append(f"Patent data may need recent updates for {key}")
                
                # Check for ArduPilot parameters that may have changed
                if "parameter" in result or "ardupilot" in key.lower():
                    gaps["update_needs"].append(f"ArduPilot parameter {key} may need version-specific updates")
        
        # Check coverage gaps (missing information)
        query_lower = query.lower()
        coverage_keywords = {
            "troubleshooting": ["error", "problem", "issue", "fix", "debug"],
            "latest": ["latest", "recent", "new", "current", "2024", "2025"],
            "community": ["forum", "discussion", "community", "experience"],
            "comparison": ["vs", "versus", "compare", "difference", "better"]
        }
        
        for gap_type, keywords in coverage_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                if not self._has_relevant_static_data(static_results, gap_type):
                    gaps["coverage_gaps"].append(f"Missing {gap_type} information")
        
        # Check specificity gaps
        if len(static_results) < 2:
            gaps["specificity_gaps"].append("Limited static knowledge coverage - need broader search")
        
        self.log_reasoning_step("gap_identified", f"Identified gaps: {len(sum(gaps.values(), []))} total")
        
        return gaps
    
    def _has_relevant_static_data(self, static_results: Dict, gap_type: str) -> bool:
        """Check if static results have relevant data for gap type"""
        
        type_indicators = {
            "troubleshooting": ["troubleshooting", "common_issues", "solutions"],
            "latest": ["2024", "2025", "recent"],
            "community": ["professional_insights", "best_practices"],
            "comparison": ["comparison", "advantages", "vs"]
        }
        
        indicators = type_indicators.get(gap_type, [])
        
        for result in static_results.values():
            result_str = json.dumps(result).lower()
            if any(indicator in result_str for indicator in indicators):
                return True
        
        return False
    
    def decide_searxng_strategy(self, gaps: Dict, query: str) -> Dict[str, Any]:
        """Decide SearXNG search strategy based on gap analysis"""
        
        total_gaps = len(sum(gaps.values(), []))
        
        if total_gaps == 0:
            strategy = {
                "use_searxng": False,
                "reason": "Static knowledge base provides comprehensive coverage"
            }
        elif total_gaps <= 2:
            strategy = {
                "use_searxng": True,
                "search_type": "targeted",
                "queries": self._generate_targeted_queries(gaps, query),
                "reason": "Targeted search to fill specific gaps"
            }
        else:
            strategy = {
                "use_searxng": True,
                "search_type": "comprehensive",
                "queries": self._generate_comprehensive_queries(query),
                "reason": "Comprehensive search due to significant knowledge gaps"
            }
        
        self.log_reasoning_step("strategy_decision", f"SearXNG strategy: {strategy}")
        
        return strategy
    
    def _generate_targeted_queries(self, gaps: Dict, original_query: str) -> List[str]:
        """Generate targeted search queries based on identified gaps"""
        
        queries = []
        
        if gaps["temporal_gaps"]:
            queries.append(f"{original_query} 2024 2025 latest")
        
        if gaps["update_needs"]:
            queries.append(f"ArduPilot {original_query} current version parameters")
        
        if gaps["coverage_gaps"]:
            for gap in gaps["coverage_gaps"]:
                if "troubleshooting" in gap:
                    queries.append(f"{original_query} troubleshooting forum discussion")
                elif "community" in gap:
                    queries.append(f"{original_query} ArduPilot community experience")
        
        return queries[:3]  # Limit to 3 targeted queries
    
    def _generate_comprehensive_queries(self, original_query: str) -> List[str]:
        """Generate comprehensive search queries for broad coverage"""
        
        return [
            f"{original_query} ArduPilot latest documentation",
            f"{original_query} 2024 2025 UAV implementation",
            f"{original_query} forum discussion troubleshooting",
            f"{original_query} best practices professional"
        ]

class SearXNGInterface:
    """Interface to SearXNG search engine"""
    
    def __init__(self, searxng_url: str = "http://localhost:8080"):
        self.base_url = searxng_url
        self.session = requests.Session()
        
    def search(self, query: str, categories: List[str] = None, engines: List[str] = None) -> Dict[str, Any]:
        """Perform search via SearXNG"""
        
        params = {
            "q": query,
            "format": "json",
            "safesearch": "0"
        }
        
        if categories:
            params["categories"] = ",".join(categories)
        
        if engines:
            params["engines"] = ",".join(engines)
        
        try:
            response = self.session.get(
                f"{self.base_url}/search",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "results": response.json(),
                    "query": query,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}",
                    "query": query
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "query": query
            }
    
    def health_check(self) -> bool:
        """Check if SearXNG is available"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False

class HybridSearchAgent(EnhancedStasikAgent):
    """Enhanced Stasik Agent with hybrid search capabilities"""
    
    def __init__(self, searxng_url: str = "http://localhost:8080", ardupilot_kb_path=None):
        super().__init__(ardupilot_kb_path)
        
        self.searxng = SearXNGInterface(searxng_url)
        self.reasoning = IntermediaryReasoning()
        self.hybrid_queries = 0
        
        # Check SearXNG availability
        if self.searxng.health_check():
            print(f"[OK] SearXNG connected at {searxng_url}")
            self.searxng_available = True
        else:
            print(f"[WARNING] SearXNG not available at {searxng_url}")
            self.searxng_available = False
    
    def hybrid_query(self, query: str, technology: str = None) -> Dict[str, Any]:
        """Perform hybrid query with intermediary reasoning"""
        
        self.hybrid_queries += 1
        start_time = time.time()
        
        self.reasoning.log_reasoning_step("query_start", f"Hybrid query initiated: {query}")
        
        # Step 1: Static Knowledge Base Search
        self.reasoning.log_reasoning_step("static_search", "Querying static knowledge base")
        
        static_results = {}
        
        if technology:
            # Technology-specific queries
            static_results["technology"] = self.query_technology(technology)
            static_results["ardupilot_integration"] = self.query_ardupilot_integration(technology)
            
            # Check for parameters in query
            params = ["ARSPD_TYPE", "ARSPD_RATIO", "ARSPD_AUTOCAL", "EK3_ARSP_THR"]
            for param in params:
                if param.lower() in query.lower():
                    static_results[f"param_{param}"] = self.get_parameter_guidance(param)
            
            # Check for EKF tuning
            if any(word in query.lower() for word in ["ekf", "tuning", "fusion"]):
                static_results["ekf_tuning"] = self.get_ekf_tuning_guidance("airspeed")
        else:
            # General technology detection
            techs = self._detect_technologies(query)
            for tech in techs[:2]:
                static_results[f"{tech}_overview"] = self.query_technology(tech)
        
        self.reasoning.log_reasoning_step("static_complete", f"Static search returned {len(static_results)} results")
        
        # Step 2: Gap Analysis and Reasoning
        gaps = self.reasoning.analyze_knowledge_gaps(static_results, query)
        strategy = self.reasoning.decide_searxng_strategy(gaps, query)
        
        # Step 3: Dynamic Search (if needed)
        dynamic_results = {}
        
        if strategy["use_searxng"] and self.searxng_available:
            self.reasoning.log_reasoning_step("dynamic_search", f"Initiating SearXNG search: {strategy['search_type']}")
            
            for search_query in strategy["queries"]:
                # Use technical categories and engines for UAV/technical content
                search_result = self.searxng.search(
                    search_query,
                    categories=["it", "science"],
                    engines=["google", "bing", "duckduckgo"]
                )
                
                if search_result["status"] == "success":
                    dynamic_results[f"searxng_{len(dynamic_results)}"] = search_result
                
                time.sleep(0.5)  # Rate limiting
            
            self.reasoning.log_reasoning_step("dynamic_complete", f"SearXNG returned {len(dynamic_results)} result sets")
        
        # Step 4: Result Integration and Synthesis
        execution_time = time.time() - start_time
        
        hybrid_result = {
            "status": "success",
            "query": query,
            "technology": technology,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat(),
            "static_results": static_results,
            "dynamic_results": dynamic_results,
            "reasoning": {
                "gaps_identified": gaps,
                "search_strategy": strategy,
                "reasoning_steps": self.reasoning.reasoning_log[-10:],  # Last 10 steps
                "static_coverage": len(static_results),
                "dynamic_coverage": len(dynamic_results)
            },
            "synthesis": self._synthesize_results(static_results, dynamic_results, query)
        }
        
        self.reasoning.log_reasoning_step("query_complete", f"Hybrid query completed in {execution_time:.2f}s")
        
        return hybrid_result
    
    def _detect_technologies(self, query: str) -> List[str]:
        """Detect technologies mentioned in query"""
        
        tech_keywords = {
            'pitot_tubes': ['pitot', 'pitot tube', 'pitot-tube'],
            'multi_hole_probes': ['multi-hole', 'multi hole', 'probe', 'probes'],
            'anemometers': ['anemometer', 'anemometers', 'wind sensor'],
            'mems_sensors': ['mems', 'mems sensor', 'mems sensors', 'micro']
        }
        
        query_lower = query.lower()
        detected = []
        
        for tech, keywords in tech_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected.append(tech)
        
        return detected
    
    def _synthesize_results(self, static_results: Dict, dynamic_results: Dict, query: str) -> Dict[str, Any]:
        """Synthesize static and dynamic results into comprehensive response"""
        
        synthesis = {
            "primary_source": "static" if static_results else "dynamic",
            "confidence": self._calculate_confidence(static_results, dynamic_results),
            "completeness": self._assess_completeness(static_results, dynamic_results, query),
            "recommendations": []
        }
        
        # Add recommendations based on result quality
        if synthesis["confidence"] > 0.8:
            synthesis["recommendations"].append("High confidence response - comprehensive coverage achieved")
        elif synthesis["completeness"] < 0.6:
            synthesis["recommendations"].append("Consider manual verification for critical applications")
        
        if dynamic_results:
            synthesis["recommendations"].append("Dynamic results included - information is current")
        
        return synthesis
    
    def _calculate_confidence(self, static_results: Dict, dynamic_results: Dict) -> float:
        """Calculate confidence score based on result quality"""
        
        static_score = min(len(static_results) * 0.2, 0.8)  # Up to 0.8 for static
        dynamic_score = min(len(dynamic_results) * 0.1, 0.2)  # Up to 0.2 for dynamic
        
        return static_score + dynamic_score
    
    def _assess_completeness(self, static_results: Dict, dynamic_results: Dict, query: str) -> float:
        """Assess completeness of combined results"""
        
        # Simple heuristic based on result count and query complexity
        total_results = len(static_results) + len(dynamic_results)
        query_complexity = len(query.split())
        
        completeness = min(total_results / max(query_complexity * 0.5, 2), 1.0)
        
        return completeness
    
    def get_hybrid_stats(self) -> Dict[str, Any]:
        """Get hybrid search statistics"""
        
        return {
            "hybrid_queries": self.hybrid_queries,
            "searxng_available": self.searxng_available,
            "total_reasoning_steps": len(self.reasoning.reasoning_log),
            "agent_info": self.get_enhanced_agent_info()
        }

def main():
    """Demo hybrid search agent"""
    
    print("HYBRID SEARCH AGENT WITH INTERMEDIARY REASONING")
    print("=" * 80)
    print("Static Knowledge Base + SearXNG Dynamic Search")
    print("=" * 80)
    print()
    
    # Initialize hybrid agent
    agent = HybridSearchAgent()
    
    # Display initialization status
    stats = agent.get_hybrid_stats()
    print(f"Agent: {stats['agent_info']['agent_name']} v{stats['agent_info']['version']}")
    print(f"SearXNG Available: {stats['searxng_available']}")
    print(f"Hybrid Search: Ready")
    print()
    
    # Demo queries
    test_queries = [
        ("How to configure ARSPD_TYPE in ArduPilot 2024?", "pitot_tubes"),
        ("Latest EKF3 tuning for UAV airspeed sensors", None),
        ("MEMS vs pitot tube reliability comparison", "mems_sensors")
    ]
    
    for i, (query, tech) in enumerate(test_queries, 1):
        print(f"DEMO {i}: {query}")
        print("-" * 60)
        
        result = agent.hybrid_query(query, tech)
        
        print(f"Status: {result['status']}")
        print(f"Execution Time: {result['execution_time']:.2f}s")
        print(f"Static Results: {result['reasoning']['static_coverage']}")
        print(f"Dynamic Results: {result['reasoning']['dynamic_coverage']}")
        
        strategy = result['reasoning']['search_strategy']
        print(f"Search Strategy: {strategy.get('reason', 'N/A')}")
        
        if result['reasoning']['gaps_identified']:
            total_gaps = len(sum(result['reasoning']['gaps_identified'].values(), []))
            print(f"Knowledge Gaps Identified: {total_gaps}")
        
        synthesis = result['synthesis']
        print(f"Confidence: {synthesis['confidence']:.2f}")
        print(f"Completeness: {synthesis['completeness']:.2f}")
        
        print()
        if i < len(test_queries):
            print("=" * 60)
            print()
    
    print("HYBRID SEARCH CAPABILITIES DEMONSTRATED:")
    print("✓ Static knowledge base as primary source")
    print("✓ Gap analysis with intermediary reasoning")
    print("✓ Dynamic SearXNG search for updates/gaps")
    print("✓ Intelligent search strategy selection")
    print("✓ Result synthesis and confidence scoring")
    print("✓ Complete reasoning transparency")
    print("=" * 80)

if __name__ == "__main__":
    main()