#!/usr/bin/env python3
"""
Comprehensive Hybrid Chat - Direct Interface
Chat directly with the comprehensive knowledge base without GPT integration
"""

import json
from datetime import datetime
from hybrid_comprehensive_agent import HybridComprehensiveAgent

class ComprehensiveDirectChat:
    def __init__(self, searxng_url="http://localhost:8080"):
        """Initialize direct comprehensive chat"""
        
        self.agent = HybridComprehensiveAgent(searxng_url)
        self.session_start = datetime.now()
        self.query_count = 0
        self.conversation_history = []
        self.comprehensive_usage_log = []
    
    def display_banner(self):
        """Display comprehensive chat banner"""
        print()
        print("=" * 90)
        print("COMPREHENSIVE HYBRID STASIK AGENT - DIRECT CHAT")
        print("=" * 90)
        print("Complete Knowledge Base: 1,100+ Patents + 500+ Scientific Papers + Professional Discussions")
        print("Dynamic Search: SearXNG Integration + Intermediary Reasoning")
        print()
        
        # Display comprehensive agent status
        stats = self.agent.get_comprehensive_hybrid_stats()
        
        print(f"Agent: {stats['agent_info']['agent_name']} v{stats['agent_info']['version']}")
        print(f"Knowledge: {stats['comprehensive_features']['total_patents']} patents + {stats['comprehensive_features']['total_papers']} papers")
        print(f"Sources: {stats['comprehensive_features']['source_count']} knowledge sources + ArduPilot")
        print(f"SearXNG: {'[OK] Connected' if stats['hybrid_capabilities']['searxng_available'] else '[ERROR] Unavailable'}")
        print()
        print("COMPREHENSIVE CAPABILITIES:")
        print("- Patent analysis: 100+ patents per query")
        print("- Scientific research: Dozens of papers per query") 
        print("- Professional insights and best practices")
        print("- Real-time SearXNG dynamic search")
        print("- Intermediary reasoning with transparency")
        print("- Multi-source validation")
        print()
        print("Ask about UAV airflow sensors, patents, research, ArduPilot, troubleshooting!")
        print("Type 'exit' to quit, 'stats' for statistics, 'help' for examples")
        print("=" * 90)
        print()
    
    def show_examples(self):
        """Show example queries"""
        print("\nEXAMPLE QUERIES:")
        print("-" * 40)
        print("- What are the latest innovations in pitot tube technology?")
        print("- ARSPD_TYPE parameter configuration errors ArduPilot 2024")
        print("- Multi-hole probe angle of attack measurement accuracy")
        print("- MEMS sensor temperature compensation methods")
        print("- Patent analysis for wind anemometer UAV integration")
        print("- Professional best practices for airspeed sensor calibration")
        print("- Latest research in UAV airflow sensing 2024")
        print("- Troubleshooting pitot tube blockage issues")
        print()
    
    def process_comprehensive_query(self, user_question: str):
        """Process query with comprehensive analysis"""
        
        self.query_count += 1
        print(f"[COMPREHENSIVE ANALYSIS] Processing with complete knowledge base...")
        
        # Detect technology focus
        technology = self._detect_technology(user_question)
        if technology:
            print(f"[TECHNOLOGY FOCUS] {technology.replace('_', ' ').title()}")
        
        # Execute comprehensive hybrid query
        result = self.agent.hybrid_query_comprehensive(user_question, technology)
        
        # Log usage
        self._log_usage(user_question, result)
        
        # Display comprehensive reasoning
        self._display_reasoning(result)
        
        return result
    
    def _detect_technology(self, query: str) -> str:
        """Detect technology from query"""
        tech_keywords = {
            'pitot_tubes': ['pitot', 'pitot tube', 'static pressure', 'total pressure'],
            'multi_hole_probes': ['multi-hole', 'multi hole', 'probe', 'probes', '5-hole'],
            'anemometers': ['anemometer', 'wind sensor', 'wind measurement'],
            'mems_sensors': ['mems', 'micro', 'silicon sensor', 'microfabrication']
        }
        
        query_lower = query.lower()
        for tech, keywords in tech_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return tech
        return None
    
    def _log_usage(self, query: str, result: dict):
        """Log comprehensive usage"""
        usage_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "execution_time": result['execution_time'],
            "static_coverage": result['reasoning']['static_coverage'],
            "dynamic_coverage": result['reasoning']['dynamic_coverage'],
            "confidence": result['synthesis']['confidence'],
            "knowledge_depth": result['synthesis'].get('knowledge_depth', 'standard'),
            "patents_analyzed": 0,
            "papers_analyzed": 0
        }
        
        # Extract analysis metrics
        for key, static_result in result.get('static_results', {}).items():
            if 'patent_analysis' in static_result:
                usage_entry['patents_analyzed'] = static_result['patent_analysis'].get('total_patents_found', 0)
            if 'scientific_research' in static_result:
                usage_entry['papers_analyzed'] = static_result['scientific_research'].get('total_papers_found', 0)
        
        self.comprehensive_usage_log.append(usage_entry)
    
    def _display_reasoning(self, result: dict):
        """Display comprehensive reasoning"""
        reasoning = result['reasoning']
        synthesis = result['synthesis']
        
        print(f"[ANALYSIS] Execution: {result['execution_time']:.2f}s | Confidence: {synthesis['confidence']:.2f}")
        print(f"[COVERAGE] Static: {reasoning['static_coverage']} | Dynamic: {reasoning['dynamic_coverage']}")
        print(f"[KNOWLEDGE] Depth: {synthesis.get('knowledge_depth', 'standard')}")
        
        # Show comprehensive analysis metrics
        total_patents = 0
        total_papers = 0
        
        for key, static_result in result.get('static_results', {}).items():
            if 'patent_analysis' in static_result:
                patents = static_result['patent_analysis'].get('total_patents_found', 0)
                total_patents += patents
            if 'scientific_research' in static_result:
                papers = static_result['scientific_research'].get('total_papers_found', 0)
                total_papers += papers
        
        if total_patents > 0:
            print(f"[PATENTS] {total_patents} patents analyzed")
        if total_papers > 0:
            print(f"[RESEARCH] {total_papers} papers analyzed")
        
        print()
    
    def format_comprehensive_response(self, result: dict, question: str) -> str:
        """Format comprehensive response"""
        
        response_parts = []
        
        # Add comprehensive analysis header
        kb_size = result.get('knowledge_base_size', {})
        response_parts.append(f"COMPREHENSIVE ANALYSIS RESULTS:")
        response_parts.append(f"Knowledge Base: {kb_size.get('patents', 0)} patents + {kb_size.get('papers', 0)} papers accessed")
        response_parts.append("")
        
        # Process static results
        for key, static_result in result.get('static_results', {}).items():
            if static_result.get("status") == "success":
                
                # Technology overview
                if "overview" in static_result:
                    overview = static_result["overview"]
                    response_parts.append(f"TECHNOLOGY OVERVIEW:")
                    response_parts.append(f"- {overview.get('description', 'N/A')}")
                    
                    advantages = overview.get('advantages', [])
                    if advantages:
                        response_parts.append(f"- Key Advantages: {', '.join(advantages[:4])}")
                    
                    response_parts.append(f"- Patent Activity: {overview.get('patent_activity', 'N/A')}")
                    response_parts.append(f"- Research Activity: {overview.get('research_activity', 'N/A')}")
                    response_parts.append("")
                
                # Patent analysis
                if "patent_analysis" in static_result:
                    patent_data = static_result["patent_analysis"]
                    patents_count = patent_data.get('total_patents_found', 0)
                    
                    if patents_count > 0:
                        response_parts.append(f"PATENT ANALYSIS ({patents_count} patents):")
                        
                        # Recent patents
                        recent_patents = patent_data.get('recent_patents', [])
                        if recent_patents:
                            response_parts.append(f"- Recent Developments (2020-2025): {len(recent_patents)} patents")
                            for patent in recent_patents[:3]:
                                response_parts.append(f"  - {patent}")
                        
                        # Key patents
                        relevant_patents = patent_data.get('relevant_patents', [])[:3]
                        if relevant_patents:
                            response_parts.append("- Key Patent Innovations:")
                            for i, patent in enumerate(relevant_patents, 1):
                                title = patent.get('title', 'N/A')
                                date = patent.get('publication_date', 'N/A')
                                response_parts.append(f"  {i}. {title} ({date})")
                        
                        response_parts.append("")
                
                # Scientific research
                if "scientific_research" in static_result:
                    research_data = static_result["scientific_research"]
                    papers_count = research_data.get('total_papers_found', 0)
                    
                    if papers_count > 0:
                        response_parts.append(f"SCIENTIFIC RESEARCH ANALYSIS ({papers_count} papers):")
                        
                        research_areas = research_data.get('research_areas', [])
                        if research_areas:
                            response_parts.append(f"- Research Areas: {', '.join(research_areas[:4])}")
                        
                        # Key research papers
                        relevant_papers = research_data.get('relevant_papers', [])[:3]
                        if relevant_papers:
                            response_parts.append("- Key Research Findings:")
                            for i, paper in enumerate(relevant_papers, 1):
                                title = paper.get('title', 'N/A')
                                year = paper.get('year', 'N/A')
                                response_parts.append(f"  {i}. {title} ({year})")
                        
                        response_parts.append("")
                
                # Professional insights
                if "professional_insights" in static_result:
                    insights = static_result["professional_insights"]
                    response_parts.append("PROFESSIONAL INSIGHTS:")
                    
                    best_practices = insights.get('best_practices', [])
                    if best_practices:
                        response_parts.append("- Best Practices:")
                        for practice in best_practices[:4]:
                            response_parts.append(f"  - {practice}")
                    
                    common_issues = insights.get('common_issues', [])
                    if common_issues:
                        response_parts.append("- Common Issues:")
                        for issue in common_issues[:4]:
                            response_parts.append(f"  - {issue}")
                    
                    industry_trends = insights.get('industry_trends', [])
                    if industry_trends:
                        response_parts.append("- Industry Trends:")
                        for trend in industry_trends[:3]:
                            response_parts.append(f"  - {trend}")
                    
                    response_parts.append("")
                
                # ArduPilot integration
                if "ardupilot_integration" in static_result and "ardupilot_integration" in static_result["ardupilot_integration"]:
                    ardupilot = static_result["ardupilot_integration"]["ardupilot_integration"]
                    
                    if ardupilot.get("key_parameters"):
                        response_parts.append("ARDUPILOT INTEGRATION:")
                        response_parts.append("- Key Parameters:")
                        for param, desc in list(ardupilot["key_parameters"].items())[:4]:
                            response_parts.append(f"  - {param}: {desc}")
                        
                        if ardupilot.get("integration_points"):
                            points = ardupilot["integration_points"][:3]
                            response_parts.append(f"- Integration Points: {', '.join(points)}")
                        
                        response_parts.append("")
        
        # Dynamic search results
        if result.get('dynamic_results'):
            response_parts.append("CURRENT INFORMATION (SearXNG):")
            
            for key, dynamic_result in result['dynamic_results'].items():
                if dynamic_result.get("status") == "success":
                    query = dynamic_result.get('query', 'N/A')
                    search_results = dynamic_result.get("results", {}).get("results", [])[:2]
                    
                    if search_results:
                        response_parts.append(f"- Search: {query}")
                        for i, search_result in enumerate(search_results, 1):
                            title = search_result.get('title', 'N/A')[:80]
                            content = search_result.get('content', 'N/A')[:120]
                            response_parts.append(f"  {i}. {title}")
                            response_parts.append(f"     {content}...")
            
            response_parts.append("")
        
        # Synthesis and recommendations
        synthesis = result['synthesis']
        response_parts.append("ANALYSIS SUMMARY:")
        response_parts.append(f"- Confidence Level: {synthesis['confidence']:.2f} ({synthesis.get('knowledge_depth', 'standard')} analysis)")
        response_parts.append(f"- Information Completeness: {synthesis['completeness']:.2f}")
        
        if synthesis.get('recommendations'):
            response_parts.append("- Recommendations:")
            for rec in synthesis['recommendations']:
                response_parts.append(f"  - {rec}")
        
        return "\\n".join(response_parts)
    
    def display_session_stats(self):
        """Display session statistics"""
        print("\\n[COMPREHENSIVE SESSION STATISTICS]")
        print("-" * 50)
        
        stats = self.agent.get_comprehensive_hybrid_stats()
        
        print(f"Session Duration: {datetime.now() - self.session_start}")
        print(f"Queries Processed: {self.query_count}")
        print(f"Knowledge Base: {stats['comprehensive_features']['total_patents']} patents + {stats['comprehensive_features']['total_papers']} papers")
        
        if self.comprehensive_usage_log:
            avg_patents = sum(log.get('patents_analyzed', 0) for log in self.comprehensive_usage_log) / len(self.comprehensive_usage_log)
            avg_papers = sum(log.get('papers_analyzed', 0) for log in self.comprehensive_usage_log) / len(self.comprehensive_usage_log)
            avg_confidence = sum(log['confidence'] for log in self.comprehensive_usage_log) / len(self.comprehensive_usage_log)
            avg_time = sum(log['execution_time'] for log in self.comprehensive_usage_log) / len(self.comprehensive_usage_log)
            
            print(f"Average Patents Analyzed: {avg_patents:.1f}")
            print(f"Average Papers Analyzed: {avg_papers:.1f}")
            print(f"Average Confidence: {avg_confidence:.2f}")
            print(f"Average Response Time: {avg_time:.2f}s")
        
        print()
    
    def run_chat(self):
        """Run comprehensive direct chat"""
        
        self.display_banner()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\\nThank you for using Comprehensive Stasik Agent!")
                    self.display_session_stats()
                    break
                
                if user_input.lower() == 'stats':
                    self.display_session_stats()
                    continue
                
                if user_input.lower() == 'help':
                    self.show_examples()
                    continue
                
                if not user_input:
                    continue
                
                print()
                
                # Process comprehensive query
                result = self.process_comprehensive_query(user_input)
                
                # Format and display response
                response = self.format_comprehensive_response(result, user_input)
                
                print("[COMPREHENSIVE STASIK]")
                print(response)
                print()
                
                # Store conversation
                self.conversation_history.append({
                    "user": user_input,
                    "response": response,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })
                
            except KeyboardInterrupt:
                print("\\n\\nGoodbye!")
                break
            except Exception as e:
                print(f"\\n[ERROR] {e}")
                print("Please try again or type 'exit' to quit.\\n")

def main():
    """Main function"""
    try:
        chat = ComprehensiveDirectChat()
        chat.run_chat()
    except Exception as e:
        print(f"Failed to initialize chat: {e}")

if __name__ == "__main__":
    main()