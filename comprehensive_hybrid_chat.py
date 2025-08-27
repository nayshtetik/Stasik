#!/usr/bin/env python3
"""
Comprehensive Hybrid Chat Interface
Natural language interface with GPT-5 integration using complete knowledge base
"""

import os
import sys
import json
import re
from datetime import datetime
from hybrid_comprehensive_agent import HybridComprehensiveAgent

try:
    import openai
except ImportError:
    print("[INFO] OpenAI library not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai>=1.0.0"])
    import openai

class ComprehensiveHybridChat:
    def __init__(self, api_key=None, searxng_url="http://localhost:8080"):
        """Initialize comprehensive hybrid chat with GPT-5 integration"""
        
        self.agent = HybridComprehensiveAgent(searxng_url)
        self.session_start = datetime.now()
        self.query_count = 0
        self.conversation_history = []
        self.comprehensive_usage_log = []
        
        # Set up OpenAI client
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
        else:
            # Try to get from environment
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("[ERROR] OpenAI API key required. Set OPENAI_API_KEY environment variable or pass as parameter.")
                sys.exit(1)
            self.client = openai.OpenAI(api_key=api_key)
            
        # Test API connection
        try:
            self.client.models.list()
            print("[OK] OpenAI API connection successful")
        except Exception as e:
            print(f"[ERROR] OpenAI API connection failed: {e}")
            sys.exit(1)
    
    def display_banner(self):
        """Display comprehensive chat banner"""
        print()
        print("=" * 90)
        print("🚀 COMPREHENSIVE HYBRID STASIK AGENT - COMPLETE KNOWLEDGE INTEGRATION")
        print("=" * 90)
        print("Enhanced UAV Airflow Sensing + Complete Knowledge Base + Dynamic Search")
        print("1,100+ Patents + 500+ Scientific Papers + Professional Discussions + ArduPilot")
        print()
        
        # Display comprehensive agent status
        stats = self.agent.get_comprehensive_hybrid_stats()
        
        print(f"Agent: {stats['agent_info']['agent_name']} v{stats['agent_info']['version']}")
        print(f"Knowledge Base: {stats['comprehensive_features']['total_patents']} patents + {stats['comprehensive_features']['total_papers']} papers")
        print(f"Sources: {stats['comprehensive_features']['source_count']} knowledge sources + ArduPilot integration")
        print(f"SearXNG Status: {'✓ Connected' if stats['hybrid_capabilities']['searxng_available'] else '✗ Unavailable'}")
        print(f"GPT-5 Integration: ✓ Operational")
        print()
        print("COMPREHENSIVE CAPABILITIES:")
        print("• Deep patent analysis with 100+ patents per query")
        print("• Scientific research synthesis with dozens of papers")
        print("• Professional insights and best practices")
        print("• Real-time information updates via SearXNG")
        print("• Intermediary reasoning with full transparency")
        print("• Research-grade technical responses")
        print("• Multi-source validation and confidence scoring")
        print()
        print("Ask me about UAV airflow sensors, ArduPilot integration, latest research,")
        print("patent analysis, professional best practices, or technical troubleshooting!")
        print()
        print("Type 'exit' to quit, 'stats' for session statistics")
        print("=" * 90)
        print()
    
    def process_comprehensive_query(self, user_question: str):
        """Process user query using comprehensive hybrid search"""
        
        self.query_count += 1
        print(f"[COMPREHENSIVE SEARCH] Processing with complete knowledge base...")
        
        # Detect technology context
        technology = self._detect_primary_technology(user_question)
        
        if technology:
            print(f"[KNOWLEDGE ROUTING] Technology focus: {technology}")
        else:
            print(f"[KNOWLEDGE ROUTING] Multi-technology analysis")
        
        # Perform comprehensive hybrid query
        hybrid_result = self.agent.hybrid_query_comprehensive(user_question, technology)
        
        # Log comprehensive usage
        self._log_comprehensive_usage(user_question, hybrid_result)
        
        # Display comprehensive reasoning summary
        self._display_comprehensive_reasoning(hybrid_result)
        
        return hybrid_result
    
    def _detect_primary_technology(self, query: str) -> str:
        """Detect primary technology from query"""
        
        tech_keywords = {
            'pitot_tubes': ['pitot', 'pitot tube', 'pitot-tube', 'pressure probe', 'static pressure'],
            'multi_hole_probes': ['multi-hole', 'multi hole', 'probe', 'probes', '5-hole', '3-hole'],
            'anemometers': ['anemometer', 'anemometers', 'wind sensor', 'wind measurement', 'ultrasonic'],
            'mems_sensors': ['mems', 'mems sensor', 'mems sensors', 'micro', 'silicon sensor', 'microfabrication']
        }
        
        query_lower = query.lower()
        
        for tech, keywords in tech_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return tech
        
        return None
    
    def _log_comprehensive_usage(self, query: str, result: dict):
        """Log comprehensive hybrid usage with detailed metrics"""
        
        usage_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "comprehensive_analysis": result.get('comprehensive_analysis', False),
            "knowledge_base_size": result.get('knowledge_base_size', {}),
            "static_coverage": result['reasoning']['static_coverage'],
            "dynamic_coverage": result['reasoning']['dynamic_coverage'],
            "knowledge_depth": result['synthesis'].get('knowledge_depth', 'standard'),
            "confidence": result['synthesis']['confidence'],
            "completeness": result['synthesis']['completeness'],
            "execution_time": result['execution_time'],
            "sources_accessed": len(result.get('static_results', {})) + len(result.get('dynamic_results', {}))
        }
        
        # Add patent and paper analysis metrics
        for key, static_result in result.get('static_results', {}).items():
            if 'patent_analysis' in static_result:
                usage_entry['patents_analyzed'] = static_result['patent_analysis'].get('total_patents_found', 0)
            if 'scientific_research' in static_result:
                usage_entry['papers_analyzed'] = static_result['scientific_research'].get('total_papers_found', 0)
        
        self.comprehensive_usage_log.append(usage_entry)
    
    def _display_comprehensive_reasoning(self, result: dict):
        """Display comprehensive reasoning summary"""
        
        reasoning = result['reasoning']
        synthesis = result['synthesis']
        kb_size = result.get('knowledge_base_size', {})
        
        print(f"[KNOWLEDGE BASE] {kb_size.get('patents', 0)} patents + {kb_size.get('papers', 0)} papers accessed")
        print(f"[GAP ANALYSIS] {len(sum(reasoning['gaps_identified'].values(), []))} gaps identified")
        print(f"[SEARCH STRATEGY] {reasoning['search_strategy']['reason']}")
        print(f"[COVERAGE] Static: {reasoning['static_coverage']}, Dynamic: {reasoning['dynamic_coverage']}")
        print(f"[SYNTHESIS] Depth: {synthesis.get('knowledge_depth', 'standard')}, Confidence: {synthesis['confidence']:.2f}")
        
        # Show comprehensive analysis metrics
        for key, static_result in result.get('static_results', {}).items():
            if 'patent_analysis' in static_result:
                patents_found = static_result['patent_analysis'].get('total_patents_found', 0)
                if patents_found > 0:
                    print(f"[PATENTS] {patents_found} relevant patents analyzed")
            
            if 'scientific_research' in static_result:
                papers_found = static_result['scientific_research'].get('total_papers_found', 0)
                if papers_found > 0:
                    print(f"[RESEARCH] {papers_found} scientific papers analyzed")
        
        print()
    
    def generate_comprehensive_gpt_response(self, user_question: str, hybrid_result: dict) -> str:
        """Generate GPT-5 response using comprehensive hybrid knowledge"""
        
        # Format comprehensive knowledge for GPT
        knowledge_summary = self._format_comprehensive_knowledge(hybrid_result)
        
        # Create enhanced system prompt for comprehensive knowledge
        system_prompt = f"""You are Enhanced Comprehensive Stasik, the world's leading expert on UAV airflow sensing and ArduPilot integration with complete knowledge access.

COMPREHENSIVE HYBRID KNOWLEDGE ARCHITECTURE:
- Static Knowledge Base: 1,100+ authentic patents + 500+ scientific papers + professional discussions + ArduPilot documentation
- Dynamic Search: Real-time information via SearXNG meta-search engine
- Intermediary Reasoning: Advanced gap analysis and intelligent search routing
- Multi-source Validation: Patent + research + professional + current data synthesis

COMPREHENSIVE SEARCH ANALYSIS FOR THIS QUERY:
- Knowledge Base Size: {hybrid_result.get('knowledge_base_size', {}).get('patents', 0)} patents + {hybrid_result.get('knowledge_base_size', {}).get('papers', 0)} papers accessed
- Static Coverage: {hybrid_result['reasoning']['static_coverage']} comprehensive sources
- Dynamic Coverage: {hybrid_result['reasoning']['dynamic_coverage']} current sources
- Search Strategy: {hybrid_result['reasoning']['search_strategy']['reason']}
- Knowledge Depth: {hybrid_result['synthesis'].get('knowledge_depth', 'standard')}
- Confidence Score: {hybrid_result['synthesis']['confidence']:.2f}
- Analysis Completeness: {hybrid_result['synthesis']['completeness']:.2f}

COMPREHENSIVE KNOWLEDGE SYNTHESIS:
{knowledge_summary}

User Question: "{user_question}"

EXPERT RESPONSE REQUIREMENTS:
1. Leverage the COMPLETE knowledge base - patents, research papers, and professional insights
2. Reference specific technical details from patent analysis and scientific research
3. Include quantitative metrics (e.g., "Analysis of 118 patents shows...", "Research across 78 papers indicates...")
4. Mention recent developments from 2020-2025 when available
5. Provide professional-grade, implementable guidance
6. Include ArduPilot parameter values and integration specifics when relevant
7. Cite patent numbers, research findings, and professional best practices
8. Indicate confidence level and knowledge completeness
9. Acknowledge any limitations or gaps in the comprehensive analysis
10. Provide research-grade technical depth suitable for professional implementation

Generate an authoritative, comprehensive response demonstrating deep expertise across patents, research, and professional practice."""

        try:
            print("[GPT-5] Generating comprehensive response with complete knowledge base...")
            response = self.client.chat.completions.create(
                model="gpt-5-2025-08-07",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Based on the comprehensive knowledge analysis above, provide a detailed expert response to: {user_question}"}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"[WARNING] GPT response generation error: {e}")
            return self._format_comprehensive_fallback_response(hybrid_result, user_question)
    
    def _format_comprehensive_knowledge(self, hybrid_result: dict) -> str:
        """Format comprehensive knowledge for GPT prompt"""
        
        knowledge_summary = "COMPREHENSIVE HYBRID KNOWLEDGE SYNTHESIS:\\n"
        knowledge_summary += "=" * 60 + "\\n\\n"
        
        # Comprehensive static knowledge results
        if hybrid_result['static_results']:
            knowledge_summary += "COMPREHENSIVE STATIC KNOWLEDGE ANALYSIS:\\n"
            knowledge_summary += "-" * 40 + "\\n"
            
            for key, result in hybrid_result['static_results'].items():
                if result.get("status") == "success":
                    knowledge_summary += f"\\n[{key.upper().replace('_', ' ')}]\\n"
                    
                    # Patent analysis
                    if "patent_analysis" in result:
                        patent_data = result["patent_analysis"]
                        knowledge_summary += f"Patent Analysis: {patent_data.get('total_patents_found', 0)} relevant patents\\n"
                        
                        recent_patents = patent_data.get('recent_patents', [])
                        if recent_patents:
                            knowledge_summary += f"Recent Patents (2020-2025): {len(recent_patents)}\\n"
                        
                        relevant_patents = patent_data.get('relevant_patents', [])[:3]
                        for i, patent in enumerate(relevant_patents, 1):
                            title = patent.get('title', 'N/A')[:80]
                            knowledge_summary += f"  Patent {i}: {title}\\n"
                    
                    # Scientific research
                    if "scientific_research" in result:
                        research_data = result["scientific_research"]
                        knowledge_summary += f"Scientific Research: {research_data.get('total_papers_found', 0)} papers analyzed\\n"
                        
                        research_areas = research_data.get('research_areas', [])
                        if research_areas:
                            knowledge_summary += f"Research Areas: {', '.join(research_areas[:3])}\\n"
                        
                        relevant_papers = research_data.get('relevant_papers', [])[:2]
                        for i, paper in enumerate(relevant_papers, 1):
                            title = paper.get('title', 'N/A')[:80]
                            knowledge_summary += f"  Paper {i}: {title}\\n"
                    
                    # Professional insights
                    if "professional_insights" in result:
                        insights = result["professional_insights"]
                        
                        best_practices = insights.get('best_practices', [])
                        if best_practices:
                            knowledge_summary += f"Professional Best Practices ({len(best_practices)}): {', '.join(best_practices[:3])}\\n"
                        
                        common_issues = insights.get('common_issues', [])
                        if common_issues:
                            knowledge_summary += f"Common Issues ({len(common_issues)}): {', '.join(common_issues[:3])}\\n"
                    
                    # Technology overview
                    if "overview" in result:
                        overview = result["overview"]
                        knowledge_summary += f"Technology: {overview.get('description', 'N/A')}\\n"
                        knowledge_summary += f"Patent Activity: {overview.get('patent_activity', 'N/A')}\\n"
                        knowledge_summary += f"Research Activity: {overview.get('research_activity', 'N/A')}\\n"
                        
                        advantages = overview.get('advantages', [])
                        if advantages:
                            knowledge_summary += f"Key Advantages: {', '.join(advantages[:3])}\\n"
        
        # Dynamic search results
        if hybrid_result['dynamic_results']:
            knowledge_summary += "\\nDYNAMIC SEARCH RESULTS (SearXNG):\\n"
            knowledge_summary += "-" * 30 + "\\n"
            
            for key, result in hybrid_result['dynamic_results'].items():
                if result.get("status") == "success" and "results" in result:
                    search_results = result["results"].get("results", [])[:2]
                    knowledge_summary += f"\\nQuery: {result.get('query', 'N/A')}\\n"
                    
                    for i, search_result in enumerate(search_results, 1):
                        title = search_result.get('title', 'N/A')[:100]
                        content = search_result.get('content', 'N/A')[:150]
                        knowledge_summary += f"  {i}. {title}\\n"
                        knowledge_summary += f"     {content}...\\n"
        
        knowledge_summary += "\\n" + "=" * 60
        
        return knowledge_summary
    
    def _format_comprehensive_fallback_response(self, hybrid_result: dict, question: str) -> str:
        """Fallback response using comprehensive hybrid results"""
        
        response = f"[COMPREHENSIVE HYBRID KNOWLEDGE RESPONSE]\\n\\n"
        response += f"Query: {question}\\n"
        response += f"Knowledge Base: {hybrid_result.get('knowledge_base_size', {}).get('patents', 0)} patents + {hybrid_result.get('knowledge_base_size', {}).get('papers', 0)} papers\\n"
        response += f"Search Strategy: {hybrid_result['reasoning']['search_strategy']['reason']}\\n\\n"
        
        # Comprehensive static results
        if hybrid_result['static_results']:
            response += "Comprehensive Knowledge Analysis:\\n"
            
            for key, result in hybrid_result['static_results'].items():
                if result.get("status") == "success":
                    response += f"• {key}: Available\\n"
                    
                    if 'patent_analysis' in result:
                        patents = result['patent_analysis'].get('total_patents_found', 0)
                        response += f"  - {patents} patents analyzed\\n"
                    
                    if 'scientific_research' in result:
                        papers = result['scientific_research'].get('total_papers_found', 0)
                        response += f"  - {papers} research papers analyzed\\n"
        
        # Dynamic results  
        if hybrid_result['dynamic_results']:
            response += f"\\nDynamic Search Results: {len(hybrid_result['dynamic_results'])} result sets\\n"
        
        response += f"\\nKnowledge Depth: {hybrid_result['synthesis'].get('knowledge_depth', 'standard')}\\n"
        response += f"Confidence: {hybrid_result['synthesis']['confidence']:.2f}\\n"
        response += f"Completeness: {hybrid_result['synthesis']['completeness']:.2f}\\n"
        
        return response
    
    def display_comprehensive_session_stats(self):
        """Display comprehensive session statistics"""
        
        print("\\n[COMPREHENSIVE HYBRID SESSION STATISTICS]")
        print("-" * 60)
        
        agent_stats = self.agent.get_comprehensive_hybrid_stats()
        
        print(f"Session Duration: {datetime.now() - self.session_start}")
        print(f"Total Queries: {self.query_count}")
        print(f"Hybrid Searches: {agent_stats['hybrid_capabilities']['hybrid_queries']}")
        print(f"Reasoning Steps: {agent_stats['hybrid_capabilities']['reasoning_steps']}")
        
        # Knowledge base statistics
        print(f"Knowledge Base: {agent_stats['comprehensive_features']['total_patents']} patents + {agent_stats['comprehensive_features']['total_papers']} papers")
        print(f"Sources: {agent_stats['comprehensive_features']['source_count']} knowledge sources")
        
        if self.comprehensive_usage_log:
            # Calculate comprehensive averages
            avg_patents = sum(log.get('patents_analyzed', 0) for log in self.comprehensive_usage_log) / len(self.comprehensive_usage_log)
            avg_papers = sum(log.get('papers_analyzed', 0) for log in self.comprehensive_usage_log) / len(self.comprehensive_usage_log)
            avg_confidence = sum(log['confidence'] for log in self.comprehensive_usage_log) / len(self.comprehensive_usage_log)
            avg_execution = sum(log['execution_time'] for log in self.comprehensive_usage_log) / len(self.comprehensive_usage_log)
            
            print(f"Average Patents Analyzed: {avg_patents:.1f}")
            print(f"Average Papers Analyzed: {avg_papers:.1f}")
            print(f"Average Confidence: {avg_confidence:.2f}")
            print(f"Average Execution Time: {avg_execution:.2f}s")
        
        print(f"SearXNG Status: {'Connected' if agent_stats['hybrid_capabilities']['searxng_available'] else 'Unavailable'}")
        print()
    
    def run_comprehensive_chat(self):
        """Run comprehensive hybrid chat"""
        
        self.display_banner()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\\nThank you for using Comprehensive Hybrid Stasik Agent!")
                    self.display_comprehensive_session_stats()
                    break
                
                if user_input.lower() == 'stats':
                    self.display_comprehensive_session_stats()
                    continue
                
                if not user_input:
                    continue
                
                print()
                
                # Process with comprehensive hybrid search
                hybrid_result = self.process_comprehensive_query(user_input)
                
                # Generate comprehensive GPT response
                response = self.generate_comprehensive_gpt_response(user_input, hybrid_result)
                
                print("[COMPREHENSIVE STASIK]", response)
                print()
                
                # Store conversation
                self.conversation_history.append({
                    "user": user_input,
                    "assistant": response,
                    "hybrid_result": hybrid_result,
                    "timestamp": datetime.now().isoformat()
                })
                
            except KeyboardInterrupt:
                print("\\n\\nChat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\\n[ERROR] {e}")
                print("Please try again or type 'exit' to quit.\\n")

def main():
    """Main function for comprehensive hybrid chat"""
    
    try:
        chat = ComprehensiveHybridChat()
        chat.run_comprehensive_chat()
    except Exception as e:
        print(f"Failed to initialize comprehensive hybrid chat: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()