#!/usr/bin/env python3
"""
Hybrid Comprehensive Search Agent
Combines comprehensive knowledge base (1,100+ patents + 500+ papers) with SearXNG integration
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from comprehensive_knowledge_agent import ComprehensiveKnowledgeAgent
from hybrid_search_agent import IntermediaryReasoning, SearXNGInterface

class HybridComprehensiveAgent(ComprehensiveKnowledgeAgent):
    """Hybrid agent with comprehensive knowledge + SearXNG integration"""
    
    def __init__(self, searxng_url: str = "http://localhost:8080"):
        super().__init__()
        
        # Initialize hybrid components
        self.searxng = SearXNGInterface(searxng_url)
        self.reasoning = IntermediaryReasoning()
        self.hybrid_queries = 0
        
        # Update agent info
        self.agent_name = "Hybrid Comprehensive Stasik"
        self.version = "4.0"
        self.domain = "Complete Knowledge Integration + Dynamic Search"
        
        # Check SearXNG availability
        if self.searxng.health_check():
            print(f"[OK] SearXNG connected at {searxng_url}")
            self.searxng_available = True
        else:
            print(f"[WARNING] SearXNG not available at {searxng_url}")
            self.searxng_available = False
            
        # Add hybrid capabilities
        self.capabilities.update({
            "hybrid_search": True,
            "dynamic_search": True,
            "intermediary_reasoning": True,
            "gap_analysis": True,
            "search_strategy": True
        })
    
    def hybrid_query_comprehensive(self, query: str, technology: str = None) -> Dict[str, Any]:
        """Perform hybrid query with comprehensive knowledge base"""
        
        self.hybrid_queries += 1
        start_time = time.time()
        
        self.reasoning.log_reasoning_step("query_start", f"Hybrid comprehensive query: {query}")
        
        # Step 1: Comprehensive Static Knowledge Search
        self.reasoning.log_reasoning_step("static_search", "Querying comprehensive knowledge base")
        
        static_results = {}
        
        if technology:
            # Get comprehensive technology analysis
            tech_result = self.query_technology_comprehensive(technology)
            if tech_result.get("status") == "success":
                static_results["technology_comprehensive"] = tech_result
            
            # Get ArduPilot integration
            ardupilot_result = self.query_ardupilot_integration(technology)
            if ardupilot_result.get("status") == "success":
                static_results["ardupilot_integration"] = ardupilot_result
            
            # Check for specific parameters
            params = ["ARSPD_TYPE", "ARSPD_RATIO", "ARSPD_AUTOCAL", "EK3_ARSP_THR"]
            for param in params:
                if param.lower() in query.lower():
                    param_result = self.get_parameter_guidance(param)
                    if param_result.get("status") == "success":
                        static_results[f"param_{param}"] = param_result
        else:
            # General multi-technology search
            techs = self._detect_technologies(query)
            for tech in techs[:2]:
                tech_result = self.query_technology_comprehensive(tech)
                if tech_result.get("status") == "success":
                    static_results[f"{tech}_comprehensive"] = tech_result
        
        self.reasoning.log_reasoning_step("static_complete", f"Comprehensive static search returned {len(static_results)} results")
        
        # Step 2: Enhanced Gap Analysis
        gaps = self.reasoning.analyze_knowledge_gaps(static_results, query)
        
        # Additional gap analysis for comprehensive knowledge
        self._analyze_comprehensive_gaps(gaps, static_results, query)
        
        strategy = self.reasoning.decide_searxng_strategy(gaps, query)
        
        # Step 3: Dynamic Search (if needed)
        dynamic_results = {}
        
        if strategy["use_searxng"] and self.searxng_available:
            self.reasoning.log_reasoning_step("dynamic_search", f"Initiating SearXNG search: {strategy['search_type']}")
            
            for search_query in strategy["queries"]:
                search_result = self.searxng.search(
                    search_query,
                    categories=["it", "science"],
                    engines=["google", "bing", "duckduckgo"]
                )
                
                if search_result["status"] == "success":
                    dynamic_results[f"searxng_{len(dynamic_results)}"] = search_result
                
                time.sleep(0.5)  # Rate limiting
            
            self.reasoning.log_reasoning_step("dynamic_complete", f"SearXNG returned {len(dynamic_results)} result sets")
        
        # Step 4: Enhanced Result Synthesis
        execution_time = time.time() - start_time
        
        hybrid_result = {
            "status": "success",
            "query": query,
            "technology": technology,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat(),
            "static_results": static_results,
            "dynamic_results": dynamic_results,
            "comprehensive_analysis": True,
            "knowledge_base_size": {
                "patents": sum(self.get_comprehensive_stats()["total_content"].values()),
                "papers": self.get_comprehensive_stats()["total_content"]["papers"],
                "total_sources": len(self.knowledge_sources)
            },
            "reasoning": {
                "gaps_identified": gaps,
                "search_strategy": strategy,
                "reasoning_steps": self.reasoning.reasoning_log[-10:],
                "static_coverage": len(static_results),
                "dynamic_coverage": len(dynamic_results)
            },
            "synthesis": self._synthesize_comprehensive_results(static_results, dynamic_results, query)
        }
        
        self.reasoning.log_reasoning_step("query_complete", f"Hybrid comprehensive query completed in {execution_time:.2f}s")
        
        return hybrid_result
    
    def _analyze_comprehensive_gaps(self, gaps: Dict, static_results: Dict, query: str):
        """Analyze gaps specific to comprehensive knowledge base"""
        
        # Check if comprehensive knowledge was effectively used
        comprehensive_indicators = ["patent", "research", "paper", "study", "analysis"]
        if any(indicator in query.lower() for indicator in comprehensive_indicators):
            if not any("comprehensive" in key for key in static_results.keys()):
                gaps["coverage_gaps"].append("Comprehensive analysis requested but not provided")
        
        # Check for professional discussion needs
        discussion_indicators = ["forum", "community", "discussion", "experience", "best practice"]
        if any(indicator in query.lower() for indicator in discussion_indicators):
            gaps["coverage_gaps"].append("Professional community insights needed")
        
        # Check for latest research needs
        latest_indicators = ["latest", "recent", "new", "current", "2024", "2025"]
        if any(indicator in query.lower() for indicator in latest_indicators):
            gaps["temporal_gaps"].append("Latest research and developments needed")
    
    def _synthesize_comprehensive_results(self, static_results: Dict, dynamic_results: Dict, query: str) -> Dict[str, Any]:
        """Synthesize results with comprehensive knowledge context"""
        
        synthesis = {
            "primary_source": "comprehensive_static" if static_results else "dynamic",
            "confidence": self._calculate_comprehensive_confidence(static_results, dynamic_results),
            "completeness": self._assess_comprehensive_completeness(static_results, dynamic_results, query),
            "knowledge_depth": "comprehensive" if len(static_results) >= 2 else "standard",
            "recommendations": []
        }
        
        # Enhanced recommendations based on comprehensive knowledge
        if synthesis["confidence"] > 0.8:
            synthesis["recommendations"].append("High confidence comprehensive response - suitable for professional implementation")
        
        if any("comprehensive" in key for key in static_results.keys()):
            synthesis["recommendations"].append("Response includes comprehensive patent and research analysis")
        
        if len(static_results) >= 3:
            synthesis["recommendations"].append("Multi-source validation available - high reliability")
        
        if dynamic_results:
            synthesis["recommendations"].append("Enhanced with current information from dynamic search")
        
        return synthesis
    
    def _calculate_comprehensive_confidence(self, static_results: Dict, dynamic_results: Dict) -> float:
        """Calculate confidence with comprehensive knowledge weighting"""
        
        # Higher base score for comprehensive knowledge
        static_score = min(len(static_results) * 0.25, 0.85)  # Up to 0.85 for comprehensive
        dynamic_score = min(len(dynamic_results) * 0.05, 0.15)  # Up to 0.15 for dynamic
        
        # Bonus for comprehensive technology analysis
        if any("comprehensive" in key for key in static_results.keys()):
            static_score += 0.1
        
        return min(static_score + dynamic_score, 1.0)
    
    def _assess_comprehensive_completeness(self, static_results: Dict, dynamic_results: Dict, query: str) -> float:
        """Assess completeness with comprehensive knowledge context"""
        
        total_results = len(static_results) + len(dynamic_results)
        query_complexity = len(query.split())
        
        # Enhanced scoring for comprehensive knowledge
        base_completeness = min(total_results / max(query_complexity * 0.4, 1.5), 1.0)
        
        # Bonus for comprehensive analysis
        if any("comprehensive" in key for key in static_results.keys()):
            base_completeness += 0.2
        
        return min(base_completeness, 1.0)
    
    def _detect_technologies(self, query: str) -> List[str]:
        """Detect technologies mentioned in query"""
        
        tech_keywords = {
            'pitot_tubes': ['pitot', 'pitot tube', 'pitot-tube', 'static pressure'],
            'multi_hole_probes': ['multi-hole', 'multi hole', 'probe', 'probes', '5-hole'],
            'anemometers': ['anemometer', 'anemometers', 'wind sensor', 'wind measurement'],
            'mems_sensors': ['mems', 'mems sensor', 'mems sensors', 'micro', 'silicon sensor']
        }
        
        query_lower = query.lower()
        detected = []
        
        for tech, keywords in tech_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected.append(tech)
        
        return detected
    
    def get_comprehensive_hybrid_stats(self) -> Dict[str, Any]:
        """Get comprehensive hybrid search statistics"""
        
        base_stats = self.get_comprehensive_stats()
        
        hybrid_stats = {
            "agent_info": {
                "agent_name": self.agent_name,
                "version": self.version,
                "domain": self.domain
            },
            "knowledge_base": base_stats,
            "hybrid_capabilities": {
                "searxng_available": self.searxng_available,
                "hybrid_queries": self.hybrid_queries,
                "reasoning_steps": len(self.reasoning.reasoning_log),
                "intermediary_reasoning": True
            },
            "comprehensive_features": {
                "total_patents": base_stats["total_content"]["patents"],
                "total_papers": base_stats["total_content"]["papers"], 
                "total_entities": base_stats["total_content"]["entities"],
                "source_count": len(self.knowledge_sources),
                "ardupilot_integration": base_stats["ardupilot_integration"]
            }
        }
        
        return hybrid_stats

def main():
    """Demo comprehensive hybrid search agent"""
    
    print("COMPREHENSIVE HYBRID SEARCH AGENT")
    print("=" * 80)
    print("Complete Knowledge Base + SearXNG + Intermediary Reasoning")
    print("=" * 80)
    
    # Initialize comprehensive hybrid agent
    agent = HybridComprehensiveAgent()
    
    # Display comprehensive stats
    stats = agent.get_comprehensive_hybrid_stats()
    
    print(f"\nAGENT: {stats['agent_info']['agent_name']} v{stats['agent_info']['version']}")
    print(f"COMPREHENSIVE KNOWLEDGE:")
    print(f"- Patents: {stats['comprehensive_features']['total_patents']}")
    print(f"- Papers: {stats['comprehensive_features']['total_papers']}")
    print(f"- Entities: {stats['comprehensive_features']['total_entities']}")
    print(f"- Sources: {stats['comprehensive_features']['source_count']}")
    print(f"- ArduPilot: {stats['comprehensive_features']['ardupilot_integration']}")
    print(f"- SearXNG: {stats['hybrid_capabilities']['searxng_available']}")
    print()
    
    # Demo query with comprehensive knowledge
    test_query = "How do pitot tubes measure airspeed in UAV applications?"
    print(f"DEMO QUERY: {test_query}")
    print("-" * 60)
    
    result = agent.hybrid_query_comprehensive(test_query, "pitot_tubes")
    
    print(f"Status: {result['status']}")
    print(f"Execution Time: {result['execution_time']:.2f}s")
    print(f"Static Results: {result['reasoning']['static_coverage']}")
    print(f"Dynamic Results: {result['reasoning']['dynamic_coverage']}")
    print(f"Knowledge Depth: {result['synthesis']['knowledge_depth']}")
    print(f"Confidence: {result['synthesis']['confidence']:.2f}")
    print(f"Completeness: {result['synthesis']['completeness']:.2f}")
    
    if result['synthesis']['recommendations']:
        print("Recommendations:")
        for rec in result['synthesis']['recommendations']:
            print(f"  - {rec}")
    
    print()
    print("=" * 80)
    print("COMPREHENSIVE HYBRID SEARCH AGENT OPERATIONAL")
    print("Access to complete knowledge base + dynamic search capabilities")
    print("=" * 80)

if __name__ == "__main__":
    main()