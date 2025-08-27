#!/usr/bin/env python3
"""
Comprehensive Knowledge Agent - Full Integration
Accesses ALL knowledge sources: 1,100 patents + 500+ papers + professional discussions + ArduPilot
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from enhanced_stasik_agent import EnhancedStasikAgent

class ComprehensiveKnowledgeAgent(EnhancedStasikAgent):
    """Enhanced agent with access to complete knowledge base"""
    
    def __init__(self):
        super().__init__()
        
        # Update agent info
        self.agent_name = "Comprehensive Stasik"
        self.version = "3.0"
        self.domain = "UAV Airflow Sensing + Complete Knowledge Integration"
        
        # Knowledge base files
        self.knowledge_base_dir = Path("C:/Knowledge/Patents")
        self.knowledge_sources = {}
        
        # Load comprehensive knowledge base
        self.load_comprehensive_knowledge()
        
        # Update capabilities
        self.capabilities.update({
            "comprehensive_patents": True,
            "scientific_papers": True,
            "professional_discussions": True,
            "integrated_knowledge": True,
            "deep_technical_analysis": True
        })
    
    def load_comprehensive_knowledge(self):
        """Load all comprehensive knowledge sources"""
        
        print("LOADING COMPREHENSIVE KNOWLEDGE BASE")
        print("=" * 60)
        
        # Knowledge source files - RECATEGORIZED DATABASE (562 papers + 1100 properly categorized patents + 58 news)
        knowledge_files = {
            "patents_corrected": "RECATEGORIZED_KB_562papers_1100patents_58news_20250827_120248.json",  # PRIMARY: Recategorized patents + SerpAPI papers + news
            "scientific_papers_245": "COMPREHENSIVE_SCIENTIFIC_PAPERS_20250826_082749.json",  # Additional 245 papers
            # Disabled to prevent double-counting:
            # "integrated_knowledge": "MEMENTO_INTEGRATED_KNOWLEDGE_20250826_083912.json",  # Contains same 1100 patents
        }
        
        loaded_sources = 0
        total_patents = 0
        total_papers = 0
        
        for source_name, filename in knowledge_files.items():
            file_path = self.knowledge_base_dir / filename
            
            try:
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.knowledge_sources[source_name] = data
                        
                    # Count content based on data structure
                    if source_name == "patents_corrected":
                        # Handle corrected database structure (patents + papers in one file)
                        patent_count = data.get('collection_metadata', {}).get('total_patents', 0)
                        paper_count = data.get('collection_metadata', {}).get('total_papers', 0)
                        total_patents += patent_count
                        total_papers += paper_count
                        print(f"[OK] {source_name}: {patent_count} patents + {paper_count} papers loaded")
                    elif source_name == "patents_deduplicated":
                        # Handle deduplicated database structure
                        total_deduplicated = data.get('collection_metadata', {}).get('total_patents', 0)
                        total_patents += total_deduplicated
                        print(f"[OK] {source_name}: {total_deduplicated} deduplicated patents loaded")
                    elif 'patents' in data:
                        patent_count = len(data['patents'])
                        total_patents += patent_count
                        print(f"[OK] {source_name}: {patent_count} patents loaded")
                    elif 'papers' in data:
                        paper_count = len(data['papers'])
                        total_papers += paper_count
                        # Check for news articles in enhanced knowledge base
                        if 'news_articles' in data and 'articles' in data['news_articles']:
                            news_count = len(data['news_articles']['articles'])
                            print(f"[OK] {source_name}: {paper_count} papers + {news_count} news articles loaded")
                        else:
                            print(f"[OK] {source_name}: {paper_count} papers loaded")
                    elif 'entities' in data:
                        entity_count = len(data['entities'].get('patents', []))
                        total_patents += entity_count
                        print(f"[OK] {source_name}: {entity_count} entities loaded")
                        
                    loaded_sources += 1
                    
                else:
                    print(f"[WARNING] {filename} not found")
                    
            except Exception as e:
                print(f"[ERROR] Failed to load {filename}: {e}")
        
        print(f"\nCOMPREHENSIVE KNOWLEDGE LOADED:")
        print(f"- Sources Loaded: {loaded_sources}/{len(knowledge_files)}")
        print(f"- Total Patents: {total_patents}")
        print(f"- Total Papers: {total_papers}")
        print(f"- ArduPilot Integration: {'Yes' if self.ardupilot_knowledge else 'No'}")
        print("=" * 60)
        
        return loaded_sources > 0
    
    def query_technology_comprehensive(self, technology: str) -> Dict[str, Any]:
        """Query technology with comprehensive knowledge access"""
        
        response = {
            "status": "success",
            "technology": technology,
            "agent": self.agent_name,
            "timestamp": datetime.now().isoformat(),
            "comprehensive_analysis": True,
            "sources_accessed": []
        }
        
        # Normalize technology
        tech_key = self._normalize_technology_name(technology)
        
        # Search patents
        patent_results = self._search_patents_comprehensive(tech_key)
        if patent_results:
            response["patent_analysis"] = patent_results
            response["sources_accessed"].append("patents")
        
        # Search scientific papers
        paper_results = self._search_papers_comprehensive(tech_key)
        if paper_results:
            response["scientific_research"] = paper_results
            response["sources_accessed"].append("scientific_papers")
        
        # Get ArduPilot integration
        ardupilot_results = self.query_ardupilot_integration(technology)
        if ardupilot_results.get("status") == "success":
            response["ardupilot_integration"] = ardupilot_results.get("ardupilot_integration", {})
            response["sources_accessed"].append("ardupilot")
        
        # Professional insights
        professional_insights = self._get_professional_insights_comprehensive(tech_key)
        if professional_insights:
            response["professional_insights"] = professional_insights
            response["sources_accessed"].append("professional_discussions")
        
        # Technology overview with comprehensive data
        response["overview"] = self._generate_comprehensive_overview(tech_key, patent_results, paper_results)
        
        return response
    
    def _search_patents_comprehensive(self, technology: str) -> Dict[str, Any]:
        """Search comprehensive patent database"""
        
        results = {
            "total_patents_found": 0,
            "relevant_patents": [],
            "patent_categories": {},
            "recent_patents": [],
            "key_innovations": []
        }
        
        tech_keywords = {
            "pitot_tubes": ["pitot", "static pressure", "total pressure", "airspeed probe"],
            "multi_hole_probes": ["multi-hole", "five hole", "angle of attack", "sideslip"],
            "mems_sensors": ["MEMS", "micro", "silicon sensor", "microfabrication"],
            "anemometers": ["anemometer", "wind sensor", "wind measurement", "ultrasonic"],
            "cfd_analysis": ["CFD", "computational fluid dynamics", "flow simulation", "finite volume", "finite element", "turbulence modeling", "boundary layer", "flow visualization"]
        }
        
        search_terms = tech_keywords.get(technology, [technology])
        
        # Search in patent sources
        for source_name, source_data in self.knowledge_sources.items():
            patents_to_search = []
            
            # Handle different patent database structures
            if source_name == "patents_corrected" or source_name == "patents_deduplicated":
                # Corrected/deduplicated database structure
                if 'patents_by_technology' in source_data:
                    if technology in source_data['patents_by_technology']:
                        patents_to_search.extend(source_data['patents_by_technology'][technology])
                    # Also search "other" category for additional matches
                    if 'other' in source_data['patents_by_technology']:
                        patents_to_search.extend(source_data['patents_by_technology']['other'][:100])  # Limit other category
            elif 'patents' in source_data:
                patents_to_search = source_data['patents']
            elif 'entities' in source_data:
                patents_to_search = source_data['entities'].get('patents', [])
                
            # Search through patents
            for patent in patents_to_search:
                # Search in title and abstract
                title = patent.get('title', '').lower()
                abstract = patent.get('abstract', '').lower()
                
                if any(term.lower() in title or term.lower() in abstract for term in search_terms):
                    results["relevant_patents"].append({
                        "title": patent.get('title'),
                        "abstract": patent.get('abstract', '')[:200] + "...",
                        "publication_date": patent.get('publication_date') or patent.get('date'),
                        "assignees": patent.get('assignees', [])
                    })
                    results["total_patents_found"] += 1
                    
                    # Check if recent (2020+)
                    pub_date = patent.get('publication_date', '') or patent.get('date', '')
                    if any(year in pub_date for year in ['2020', '2021', '2022', '2023', '2024', '2025']):
                        results["recent_patents"].append(patent.get('title'))
        
        # Limit results for response size
        results["relevant_patents"] = results["relevant_patents"][:10]
        results["recent_patents"] = results["recent_patents"][:5]
        
        return results if results["total_patents_found"] > 0 else None
    
    def _search_papers_comprehensive(self, technology: str) -> Dict[str, Any]:
        """Search comprehensive scientific papers database"""
        
        results = {
            "total_papers_found": 0,
            "relevant_papers": [],
            "research_areas": [],
            "recent_research": [],
            "key_findings": []
        }
        
        tech_categories = {
            "pitot_tubes": ["Pitot_Tubes_UAV", "Pitot_Tubes"],
            "multi_hole_probes": ["Multi_Hole_Probes", "Multi_Sensor_Integration"],
            "mems_sensors": ["MEMS_Airflow_Sensors", "MEMS_Sensors"],
            "anemometers": ["Anemometers_UAV", "Anemometers"]
        }
        
        target_categories = tech_categories.get(technology, [technology])
        
        # Search in scientific paper sources
        for source_name, source_data in self.knowledge_sources.items():
            papers = []
            if source_name == "patents_corrected" and 'papers' in source_data:
                # Corrected database includes papers
                papers = source_data['papers']
            elif 'papers' in source_data:
                papers = source_data['papers']
                
            if papers:
                
                for paper in papers:
                    paper_category = paper.get('category', '')
                    title = paper.get('title', '').lower()
                    abstract = paper.get('abstract', '').lower()
                    
                    # Match by category or keyword search
                    category_match = any(cat in paper_category for cat in target_categories)
                    keyword_match = any(cat.lower().replace('_', ' ') in title or cat.lower().replace('_', ' ') in abstract for cat in target_categories)
                    
                    if category_match or keyword_match:
                        results["relevant_papers"].append({
                            "title": paper.get('title'),
                            "abstract": paper.get('abstract', '')[:200] + "...",
                            "year": paper.get('year', 'Unknown'),
                            "authors": paper.get('authors', [])
                        })
                        results["total_papers_found"] += 1
                        
                        # Track research areas
                        if paper.get('category') not in results["research_areas"]:
                            results["research_areas"].append(paper.get('category', 'General'))
        
        # Limit results
        results["relevant_papers"] = results["relevant_papers"][:8]
        results["research_areas"] = results["research_areas"][:5]
        
        return results if results["total_papers_found"] > 0 else None
    
    def _get_professional_insights_comprehensive(self, technology: str) -> Dict[str, Any]:
        """Get professional insights from comprehensive knowledge base"""
        
        insights = {
            "best_practices": [],
            "common_issues": [],
            "industry_trends": [],
            "professional_recommendations": []
        }
        
        # Extract from ArduPilot professional insights
        if self.ardupilot_knowledge and "professional_insights" in self.ardupilot_knowledge:
            prof_insights = self.ardupilot_knowledge["professional_insights"]
            
            insights["best_practices"] = prof_insights.get("best_practices", [])[:5]
            insights["common_issues"] = prof_insights.get("common_issues", [])[:5]
            
            if "troubleshooting_guide" in prof_insights:
                troubleshooting = prof_insights["troubleshooting_guide"]
                for category, items in troubleshooting.items():
                    insights["professional_recommendations"].extend(items[:2])
        
        # Add technology-specific insights
        tech_insights = {
            "pitot_tubes": {
                "best_practices": ["Regular blockage inspection", "Heated probe usage in icing conditions", "Proper static port placement"],
                "common_issues": ["Ice blockage", "Manufacturing defects", "Installation errors"],
                "industry_trends": ["Smart probe integration", "Multi-sensor fusion", "Self-diagnostic systems"]
            },
            "multi_hole_probes": {
                "best_practices": ["Careful calibration procedures", "Environmental testing", "Data validation protocols"],
                "common_issues": ["Calibration drift", "Port blockage", "Complex data processing"],
                "industry_trends": ["Miniaturization", "Real-time processing", "Machine learning integration"]
            },
            "mems_sensors": {
                "best_practices": ["Temperature compensation", "Regular recalibration", "Proper packaging"],
                "common_issues": ["Drift over time", "Temperature sensitivity", "Manufacturing variations"],
                "industry_trends": ["Integration with IoT", "Power optimization", "Array configurations"]
            },
            "anemometers": {
                "best_practices": ["Environmental protection", "Regular maintenance", "Multi-point measurement"],
                "common_issues": ["Weather exposure damage", "Calibration challenges", "Installation complexity"],
                "industry_trends": ["Wireless integration", "Smart grid applications", "Predictive maintenance"]
            }
        }
        
        if technology in tech_insights:
            tech_data = tech_insights[technology]
            insights["best_practices"].extend(tech_data["best_practices"])
            insights["common_issues"].extend(tech_data["common_issues"])
            insights["industry_trends"] = tech_data["industry_trends"]
        
        return insights
    
    def _generate_comprehensive_overview(self, technology: str, patent_results: Dict, paper_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive technology overview"""
        
        tech_descriptions = {
            "pitot_tubes": "Pressure-based airspeed measurement systems using Bernoulli's principle",
            "multi_hole_probes": "Advanced pressure probe systems for comprehensive flow measurement",
            "mems_sensors": "Miniaturized airflow sensors using microfabrication technology",
            "anemometers": "Wind speed and direction measurement devices"
        }
        
        tech_advantages = {
            "pitot_tubes": ["Proven reliability", "Aviation standard", "Simple operation", "Wide availability"],
            "multi_hole_probes": ["Complete flow data", "High accuracy", "Research capability", "3D measurements"],
            "mems_sensors": ["Small size", "Low power", "Integration capability", "Cost effective"],
            "anemometers": ["Versatile", "Established technology", "Multiple types available", "Weather resistant"]
        }
        
        overview = {
            "description": tech_descriptions.get(technology, f"Advanced {technology.replace('_', ' ')} technology"),
            "advantages": tech_advantages.get(technology, ["Advanced capability", "Professional grade"]),
            "patent_activity": f"{patent_results['total_patents_found'] if patent_results else 0} patents found",
            "research_activity": f"{paper_results['total_papers_found'] if paper_results else 0} research papers identified",
            "maturity_level": "Commercial" if patent_results and patent_results['total_patents_found'] > 50 else "Developing",
            "application_domains": ["UAV systems", "Aerospace", "Research", "Commercial aviation"]
        }
        
        return overview
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get comprehensive knowledge base statistics"""
        
        stats = {
            "agent_info": {
                "agent_name": self.agent_name,
                "version": self.version,
                "domain": self.domain
            },
            "knowledge_sources": {},
            "total_content": {
                "patents": 0,
                "papers": 0,
                "entities": 0
            },
            "source_status": {}
        }
        
        # Count content in each source
        for source_name, source_data in self.knowledge_sources.items():
            source_info = {}
            
            if source_name == "patents_corrected":
                # Handle corrected database with both patents and papers
                patent_count = source_data.get('collection_metadata', {}).get('total_patents', 0)
                paper_count = source_data.get('collection_metadata', {}).get('total_papers', 0)
                source_info['patents'] = patent_count
                source_info['papers'] = paper_count
                stats['total_content']['patents'] += patent_count
                stats['total_content']['papers'] += paper_count
            elif 'patents' in source_data:
                patent_count = len(source_data['patents'])
                source_info['patents'] = patent_count
                stats['total_content']['patents'] += patent_count
            elif 'papers' in source_data:
                paper_count = len(source_data['papers'])
                source_info['papers'] = paper_count
                stats['total_content']['papers'] += paper_count
            elif 'entities' in source_data:
                entity_count = len(source_data['entities'].get('patents', []))
                source_info['entities'] = entity_count
                stats['total_content']['entities'] += entity_count
            
            stats['knowledge_sources'][source_name] = source_info
            stats['source_status'][source_name] = 'loaded'
        
        # ArduPilot status
        stats['ardupilot_integration'] = bool(self.ardupilot_knowledge)
        
        return stats

def main():
    """Demo comprehensive knowledge agent"""
    
    print("COMPREHENSIVE KNOWLEDGE AGENT INITIALIZATION")
    print("=" * 80)
    
    # Initialize comprehensive agent
    agent = ComprehensiveKnowledgeAgent()
    
    # Show statistics
    stats = agent.get_comprehensive_stats()
    
    print(f"\nKNOWLEDGE BASE STATISTICS:")
    print(f"Agent: {stats['agent_info']['agent_name']} v{stats['agent_info']['version']}")
    print(f"Total Patents: {stats['total_content']['patents']}")
    print(f"Total Papers: {stats['total_content']['papers']}")
    print(f"Total Entities: {stats['total_content']['entities']}")
    print(f"ArduPilot Integration: {stats['ardupilot_integration']}")
    print()
    
    print("SOURCE BREAKDOWN:")
    for source, info in stats['knowledge_sources'].items():
        print(f"- {source}: {info}")
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE KNOWLEDGE AGENT READY")
    print("Access to 1,100+ patents + 500+ papers + professional discussions + ArduPilot")
    print("=" * 80)

if __name__ == "__main__":
    main()