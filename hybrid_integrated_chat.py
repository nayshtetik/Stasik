#!/usr/bin/env python3
"""
Hybrid Integrated Chat with SearXNG Integration
Natural language interface using static knowledge base + dynamic SearXNG search
"""

import os
import sys
import json
import re
from datetime import datetime
from hybrid_search_agent import HybridSearchAgent

try:
    import openai
except ImportError:
    print("[INFO] OpenAI library not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai>=1.0.0"])
    import openai

class HybridIntegratedChat:
    def __init__(self, api_key=None, searxng_url="http://localhost:8080"):
        """Initialize hybrid chat with SearXNG integration"""
        
        self.agent = HybridSearchAgent(searxng_url)
        self.session_start = datetime.now()
        self.query_count = 0
        self.hybrid_usage_log = []
        self.conversation_history = []
        
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
        """Display enhanced chat banner"""
        print()
        print("=" * 80)
        print("🔍 HYBRID STASIK AGENT - INTELLIGENT SEARCH INTEGRATION")
        print("=" * 80)
        print("Enhanced UAV Airflow Sensing + ArduPilot Integration")
        print("Static Knowledge Base + Dynamic SearXNG Search")
        print()
        
        # Display agent status
        stats = self.agent.get_hybrid_stats()
        print(f"Agent: {stats['agent_info']['agent_name']} v{stats['agent_info']['version']}")
        print(f"Knowledge Sources: Static DB + ArduPilot KB + SearXNG")
        print(f"SearXNG Status: {'✓ Connected' if stats['searxng_available'] else '✗ Unavailable'}")
        print(f"Reasoning: Intermediary gap analysis enabled")
        print()
        print("Features:")
        print("• Intelligent search routing (static-first, dynamic for gaps)")
        print("• Intermediary reasoning and gap analysis")
        print("• Real-time information updates via SearXNG")
        print("• Confidence scoring and completeness assessment")
        print("• Full reasoning transparency")
        print()
        print("Ask me about UAV airflow sensors, ArduPilot integration,")
        print("parameters, EKF tuning, troubleshooting, or latest developments!")
        print()
        print("Type 'exit' to quit, 'stats' for session statistics")
        print("=" * 80)
        print()
    
    def process_user_query(self, user_question: str) -> Dict[str, Any]:
        """Process user query using hybrid search with intermediary reasoning"""
        
        self.query_count += 1
        print(f"[HYBRID SEARCH] Processing query with intermediary reasoning...")
        
        # Detect technology context
        technology = self._detect_primary_technology(user_question)
        
        if technology:
            print(f"[KNOWLEDGE ROUTING] Detected technology: {technology}")
        else:
            print(f"[KNOWLEDGE ROUTING] General query - multi-technology analysis")
        
        # Perform hybrid query with reasoning
        hybrid_result = self.agent.hybrid_query(user_question, technology)
        
        # Log hybrid usage
        self._log_hybrid_usage(user_question, hybrid_result)
        
        # Display reasoning summary
        self._display_reasoning_summary(hybrid_result)
        
        return hybrid_result
    
    def _detect_primary_technology(self, query: str) -> str:
        """Detect primary technology from query"""
        
        tech_keywords = {
            'pitot_tubes': ['pitot', 'pitot tube', 'pitot-tube', 'pressure probe'],
            'multi_hole_probes': ['multi-hole', 'multi hole', 'probe', 'probes', '5-hole'],
            'anemometers': ['anemometer', 'anemometers', 'wind sensor', 'wind measurement'],
            'mems_sensors': ['mems', 'mems sensor', 'mems sensors', 'micro', 'silicon sensor']
        }
        
        query_lower = query.lower()
        
        for tech, keywords in tech_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return tech
        
        return None
    
    def _log_hybrid_usage(self, query: str, result: Dict[str, Any]):
        """Log hybrid search usage"""
        
        usage_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "static_results": result['reasoning']['static_coverage'],
            "dynamic_results": result['reasoning']['dynamic_coverage'],
            "search_strategy": result['reasoning']['search_strategy']['reason'],
            "gaps_found": len(sum(result['reasoning']['gaps_identified'].values(), [])),
            "confidence": result['synthesis']['confidence'],
            "execution_time": result['execution_time']
        }
        
        self.hybrid_usage_log.append(usage_entry)
    
    def _display_reasoning_summary(self, result: Dict[str, Any]):
        """Display reasoning summary to user"""
        
        reasoning = result['reasoning']
        synthesis = result['synthesis']
        
        print(f"[REASONING] Gap analysis: {len(sum(reasoning['gaps_identified'].values(), []))} gaps identified")
        print(f"[SEARCH] Strategy: {reasoning['search_strategy']['reason']}")
        print(f"[COVERAGE] Static: {reasoning['static_coverage']}, Dynamic: {reasoning['dynamic_coverage']}")
        print(f"[SYNTHESIS] Confidence: {synthesis['confidence']:.2f}, Completeness: {synthesis['completeness']:.2f}")
        print()
    
    def generate_gpt_response_with_hybrid_knowledge(self, user_question: str, hybrid_result: Dict[str, Any]) -> str:
        """Generate GPT-5 response using hybrid knowledge"""
        
        # Format hybrid knowledge for GPT
        knowledge_summary = self._format_hybrid_knowledge(hybrid_result)
        
        # Create enhanced system prompt
        system_prompt = f"""You are Enhanced Stasik, an expert UAV airflow sensing and ArduPilot integration consultant with hybrid knowledge access.

HYBRID KNOWLEDGE ARCHITECTURE:
- Static Knowledge Base: 1,100 authentic patents + 500 scientific papers + ArduPilot documentation
- Dynamic Search: Real-time information via SearXNG meta-search engine
- Intermediary Reasoning: Gap analysis and intelligent search routing

SEARCH REASONING FOR THIS QUERY:
- Static Coverage: {hybrid_result['reasoning']['static_coverage']} results
- Dynamic Coverage: {hybrid_result['reasoning']['dynamic_coverage']} results  
- Search Strategy: {hybrid_result['reasoning']['search_strategy']['reason']}
- Knowledge Gaps: {len(sum(hybrid_result['reasoning']['gaps_identified'].values(), []))} identified
- Confidence Score: {hybrid_result['synthesis']['confidence']:.2f}

KNOWLEDGE BASE DATA:
{knowledge_summary}

User Question: "{user_question}"

IMPORTANT INSTRUCTIONS:
1. Use BOTH static and dynamic knowledge sources in your response
2. Reference specific technical details from the knowledge base
3. Mention when information comes from recent/dynamic sources
4. Indicate confidence level based on knowledge completeness  
5. Provide practical, implementable guidance
6. Include ArduPilot parameter values and integration specifics when relevant
7. Acknowledge any knowledge limitations or gaps

Generate a comprehensive, authoritative response demonstrating expertise in both UAV sensors and ArduPilot systems."""

        try:
            print("[GPT-5] Generating response with hybrid knowledge...")
            response = self.client.chat.completions.create(
                model="gpt-5-2025-08-07",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Based on the hybrid knowledge analysis above, please answer: {user_question}"}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"[WARNING] GPT response generation error: {e}")
            return self._format_hybrid_fallback_response(hybrid_result, user_question)
    
    def _format_hybrid_knowledge(self, hybrid_result: Dict[str, Any]) -> str:
        """Format hybrid knowledge for GPT prompt"""
        
        knowledge_summary = "HYBRID KNOWLEDGE SYNTHESIS:\\n"
        knowledge_summary += "=" * 50 + "\\n\\n"
        
        # Static knowledge results
        if hybrid_result['static_results']:
            knowledge_summary += "STATIC KNOWLEDGE BASE RESULTS:\\n"
            knowledge_summary += "-" * 30 + "\\n"
            
            for key, result in hybrid_result['static_results'].items():
                if result.get("status") == "success":
                    knowledge_summary += f"\\n[{key.upper()}]\\n"
                    
                    # Format overview data
                    if "overview" in result:
                        overview = result["overview"]
                        knowledge_summary += f"Description: {overview.get('description', 'N/A')}\\n"
                        knowledge_summary += f"Patent Activity: {overview.get('patent_activity', 'N/A')}\\n"
                        if 'advantages' in overview:
                            knowledge_summary += f"Advantages: {', '.join(overview['advantages'][:3])}\\n"
                    
                    # Format ArduPilot integration
                    if "ardupilot_integration" in result:
                        ardupilot = result["ardupilot_integration"]
                        knowledge_summary += "ArduPilot Integration:\\n"
                        if "key_parameters" in ardupilot:
                            for param, desc in list(ardupilot["key_parameters"].items())[:3]:
                                knowledge_summary += f"  {param}: {desc}\\n"
                    
                    # Format parameter details
                    if "parameter_details" in result:
                        param_details = result["parameter_details"]
                        knowledge_summary += f"Parameter: {result.get('parameter')}\\n"
                        knowledge_summary += f"Description: {param_details.get('description')}\\n"
                        if "values" in param_details:
                            knowledge_summary += "Values:\\n"
                            for value, desc in list(param_details["values"].items())[:3]:
                                knowledge_summary += f"  {value}: {desc}\\n"
        
        # Dynamic search results
        if hybrid_result['dynamic_results']:
            knowledge_summary += "\\nDYNAMIC SEARCH RESULTS (SearXNG):\\n"
            knowledge_summary += "-" * 30 + "\\n"
            
            for key, result in hybrid_result['dynamic_results'].items():
                if result.get("status") == "success" and "results" in result:
                    search_results = result["results"].get("results", [])[:3]  # Top 3
                    knowledge_summary += f"\\nQuery: {result.get('query', 'N/A')}\\n"
                    
                    for i, search_result in enumerate(search_results, 1):
                        title = search_result.get('title', 'N/A')[:100]
                        content = search_result.get('content', 'N/A')[:200]
                        knowledge_summary += f"  {i}. {title}\\n"
                        knowledge_summary += f"     {content}...\\n"
        
        knowledge_summary += "\\n" + "=" * 50
        
        return knowledge_summary
    
    def _format_hybrid_fallback_response(self, hybrid_result: Dict[str, Any], question: str) -> str:
        """Fallback response using hybrid results"""
        
        response = f"[HYBRID KNOWLEDGE RESPONSE]\\n\\n"
        response += f"Query: {question}\\n"
        response += f"Search Strategy: {hybrid_result['reasoning']['search_strategy']['reason']}\\n\\n"
        
        # Static results
        if hybrid_result['static_results']:
            response += "Static Knowledge Base Results:\\n"
            for key, result in hybrid_result['static_results'].items():
                if result.get("status") == "success":
                    response += f"• {key}: Available\\n"
        
        # Dynamic results  
        if hybrid_result['dynamic_results']:
            response += f"\\nDynamic Search Results: {len(hybrid_result['dynamic_results'])} result sets\\n"
        
        response += f"\\nConfidence: {hybrid_result['synthesis']['confidence']:.2f}\\n"
        response += f"Completeness: {hybrid_result['synthesis']['completeness']:.2f}\\n"
        
        return response
    
    def display_session_stats(self):
        """Display enhanced session statistics"""
        
        print("\\n[HYBRID SESSION STATISTICS]")
        print("-" * 50)
        
        agent_stats = self.agent.get_hybrid_stats()
        
        print(f"Session Duration: {datetime.now() - self.session_start}")
        print(f"Total Queries: {self.query_count}")
        print(f"Hybrid Searches: {agent_stats['hybrid_queries']}")
        print(f"Reasoning Steps: {agent_stats['total_reasoning_steps']}")
        
        if self.hybrid_usage_log:
            # Calculate averages
            avg_static = sum(log['static_results'] for log in self.hybrid_usage_log) / len(self.hybrid_usage_log)
            avg_dynamic = sum(log['dynamic_results'] for log in self.hybrid_usage_log) / len(self.hybrid_usage_log)
            avg_confidence = sum(log['confidence'] for log in self.hybrid_usage_log) / len(self.hybrid_usage_log)
            avg_execution = sum(log['execution_time'] for log in self.hybrid_usage_log) / len(self.hybrid_usage_log)
            
            print(f"Average Static Results: {avg_static:.1f}")
            print(f"Average Dynamic Results: {avg_dynamic:.1f}")
            print(f"Average Confidence: {avg_confidence:.2f}")
            print(f"Average Execution Time: {avg_execution:.2f}s")
        
        print(f"SearXNG Status: {'Connected' if agent_stats['searxng_available'] else 'Unavailable'}")
        print()
    
    def run_chat(self):
        """Run hybrid integrated chat"""
        
        self.display_banner()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\\nThank you for using Hybrid Stasik Agent!")
                    self.display_session_stats()
                    break
                
                if user_input.lower() == 'stats':
                    self.display_session_stats()
                    continue
                
                if not user_input:
                    continue
                
                print()
                
                # Process with hybrid search
                hybrid_result = self.process_user_query(user_input)
                
                # Generate GPT response
                response = self.generate_gpt_response_with_hybrid_knowledge(user_input, hybrid_result)
                
                print("[STASIK]", response)
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
    """Main function for hybrid integrated chat"""
    
    try:
        chat = HybridIntegratedChat()
        chat.run_chat()
    except Exception as e:
        print(f"Failed to initialize hybrid chat: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()