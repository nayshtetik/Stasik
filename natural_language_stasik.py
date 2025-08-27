#!/usr/bin/env python3
"""
Natural Language Stasik Agent
Seamless natural language interface with comprehensive knowledge base access
No technical machinery visible - just natural conversation with deep knowledge
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
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai>=1.0.0"])
    import openai

class NaturalLanguageStasik:
    def __init__(self, api_key=None):
        """Initialize natural language Stasik with seamless knowledge access"""
        
        # Initialize comprehensive knowledge agent (silent)
        self.knowledge_agent = HybridComprehensiveAgent()
        
        # Set up OpenAI client
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
        else:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("Error: OpenAI API key required. Set OPENAI_API_KEY environment variable.")
                sys.exit(1)
            self.client = openai.OpenAI(api_key=api_key)
        
        # Conversation history
        self.conversation_history = []
        
        # Initialize silently - get agent ready
        try:
            # Test comprehensive knowledge access
            test_result = self.knowledge_agent.hybrid_query_comprehensive("test", "pitot_tubes")
            self.knowledge_ready = test_result.get('status') == 'success'
        except:
            self.knowledge_ready = False
    
    def display_banner(self):
        """Display clean natural language banner"""
        print()
        print("=" * 80)
        print("STASIK - UAV AIRFLOW SENSING EXPERT")
        print("=" * 80)
        print("I'm Stasik, your expert consultant on UAV airflow sensing technologies.")
        print("I have comprehensive knowledge of patents, research, and professional practices")
        print("in pitot tubes, multi-hole probes, MEMS sensors, anemometers, and ArduPilot.")
        print()
        print("Ask me anything about airflow sensors, troubleshooting, or system integration!")
        print("Type 'exit' to quit")
        print("=" * 80)
        print()
    
    def understand_and_respond(self, user_question: str) -> str:
        """Natural language understanding and comprehensive response generation"""
        
        if not self.knowledge_ready:
            return "I'm having trouble accessing my knowledge base right now. Please try again."
        
        # Step 1: Natural language understanding - extract intent and technology focus
        technology_focus = self._extract_technology_focus(user_question)
        query_intent = self._classify_query_intent(user_question)
        
        # Step 2: Silently gather comprehensive knowledge
        try:
            knowledge_result = self.knowledge_agent.hybrid_query_comprehensive(
                user_question, technology_focus
            )
        except Exception as e:
            return "I encountered an issue accessing my knowledge base. Let me try a different approach."
        
        if knowledge_result.get('status') != 'success':
            return "I'm having difficulty processing your question right now."
        
        # Step 3: Create comprehensive knowledge context for LLM
        knowledge_context = self._synthesize_knowledge_context(knowledge_result, user_question)
        
        # Step 4: Generate natural language response using GPT with full knowledge context
        response = self._generate_natural_response(user_question, knowledge_context, query_intent)
        
        return response
    
    def _extract_technology_focus(self, question: str) -> str:
        """Extract primary technology focus from natural language question"""
        
        question_lower = question.lower()
        
        # Technology indicators with confidence scoring
        tech_indicators = {
            'pitot_tubes': {
                'keywords': ['pitot', 'pitot tube', 'static pressure', 'total pressure', 'dynamic pressure'],
                'score': 0
            },
            'multi_hole_probes': {
                'keywords': ['multi-hole', 'multi hole', '5-hole', '3-hole', 'probe', 'angle of attack', 'sideslip'],
                'score': 0
            },
            'mems_sensors': {
                'keywords': ['mems', 'micro', 'silicon', 'microfabrication', 'chip', 'semiconductor'],
                'score': 0
            },
            'anemometers': {
                'keywords': ['anemometer', 'wind sensor', 'wind measurement', 'ultrasonic', 'wind speed'],
                'score': 0
            },
            'cfd_analysis': {
                'keywords': ['cfd', 'computational fluid dynamics', 'flow simulation', 'flow modeling', 'finite volume', 'finite element', 'ansys fluent', 'openfoam', 'turbulence modeling', 'reynolds', 'navier-stokes', 'boundary layer', 'flow visualization'],
                'score': 0
            }
        }
        
        # Score each technology based on keyword matches
        for tech, data in tech_indicators.items():
            for keyword in data['keywords']:
                if keyword in question_lower:
                    data['score'] += 1
                    # Boost score if keyword appears multiple times
                    data['score'] += question_lower.count(keyword) - 1
        
        # Return technology with highest score, or None if no clear match
        max_score = max(data['score'] for data in tech_indicators.values())
        if max_score == 0:
            return None
        
        for tech, data in tech_indicators.items():
            if data['score'] == max_score:
                return tech
        
        return None
    
    def _classify_query_intent(self, question: str) -> str:
        """Classify the intent/type of the user's question"""
        
        question_lower = question.lower()
        
        intent_patterns = {
            'comparison': ['difference', 'compare', 'vs', 'versus', 'better', 'advantage', 'disadvantage'],
            'how_to': ['how to', 'how do', 'how can', 'procedure', 'process', 'method', 'steps'],
            'troubleshooting': ['problem', 'issue', 'error', 'fix', 'troubleshoot', 'debug', 'not working'],
            'parameter': ['parameter', 'config', 'configuration', 'setting', 'value', 'tune', 'calibrate'],
            'latest': ['latest', 'recent', 'new', 'current', '2024', '2025', 'innovation', 'development'],
            'research': ['research', 'study', 'paper', 'analysis', 'investigation', 'experiment'],
            'professional': ['best practice', 'professional', 'industry', 'standard', 'recommendation'],
            'integration': ['integrate', 'integration', 'ardupilot', 'ekf', 'fusion', 'combine']
        }
        
        intent_scores = {}
        for intent, patterns in intent_patterns.items():
            score = sum(1 for pattern in patterns if pattern in question_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if not intent_scores:
            return 'general'
        
        return max(intent_scores, key=intent_scores.get)
    
    def _synthesize_knowledge_context(self, knowledge_result: dict, question: str) -> str:
        """Synthesize comprehensive knowledge into natural context"""
        
        context_parts = []
        
        # Extract patent knowledge
        patents_analyzed = 0
        papers_analyzed = 0
        recent_patents = []
        key_research = []
        professional_insights = {}
        
        for source_key, source_data in knowledge_result.get('static_results', {}).items():
            if source_data.get('status') != 'success':
                continue
                
            # Patent analysis
            if 'patent_analysis' in source_data:
                patent_data = source_data['patent_analysis']
                patents_analyzed += patent_data.get('total_patents_found', 0)
                
                recent_patents.extend(patent_data.get('recent_patents', []))
                
                for patent in patent_data.get('relevant_patents', [])[:3]:
                    context_parts.append(f"Patent: {patent.get('title')} ({patent.get('publication_date')})")
            
            # Research analysis
            if 'scientific_research' in source_data:
                research_data = source_data['scientific_research']
                papers_analyzed += research_data.get('total_papers_found', 0)
                
                for paper in research_data.get('relevant_papers', [])[:3]:
                    key_research.append(f"{paper.get('title')} ({paper.get('year')})")
            
            # Professional insights
            if 'professional_insights' in source_data:
                professional_insights = source_data['professional_insights']
            
            # Technology overview
            if 'overview' in source_data:
                overview = source_data['overview']
                context_parts.append(f"Technology: {overview.get('description')}")
                if overview.get('advantages'):
                    context_parts.append(f"Advantages: {', '.join(overview['advantages'][:4])}")
        
        # Add research context
        if key_research:
            context_parts.append(f"Recent research includes: {'; '.join(key_research[:3])}")
        
        # Add professional context
        if professional_insights:
            if professional_insights.get('best_practices'):
                context_parts.append(f"Professional best practices: {'; '.join(professional_insights['best_practices'][:3])}")
            if professional_insights.get('common_issues'):
                context_parts.append(f"Common issues: {'; '.join(professional_insights['common_issues'][:3])}")
        
        # Add current information from dynamic search
        current_info = []
        for dynamic_key, dynamic_data in knowledge_result.get('dynamic_results', {}).items():
            if dynamic_data.get('status') == 'success':
                results = dynamic_data.get('results', {}).get('results', [])[:2]
                for result in results:
                    if 'ardupilot' in result.get('title', '').lower() or 'uav' in result.get('content', '').lower():
                        current_info.append(f"Current: {result.get('title')} - {result.get('content', '')[:100]}")
        
        if current_info:
            context_parts.extend(current_info[:2])
        
        # Create comprehensive context
        knowledge_context = f"""
Based on analysis of {patents_analyzed} patents and {papers_analyzed} research papers:

{chr(10).join(context_parts)}

This represents comprehensive knowledge from patent databases, scientific research, and professional practice in UAV airflow sensing technologies.
"""
        
        return knowledge_context
    
    def _generate_natural_response(self, question: str, knowledge_context: str, intent: str) -> str:
        """Generate natural language response using comprehensive knowledge"""
        
        # Create intent-specific system prompt
        system_prompts = {
            'comparison': "You are Stasik, a UAV airflow sensing expert. Provide a clear, detailed comparison based on the comprehensive knowledge provided. Focus on practical differences, advantages, and use cases.",
            'how_to': "You are Stasik, a UAV airflow sensing expert. Provide step-by-step guidance and practical procedures based on the comprehensive knowledge provided.",
            'troubleshooting': "You are Stasik, a UAV airflow sensing expert. Provide practical troubleshooting guidance and solutions based on the comprehensive knowledge and professional experience provided.",
            'parameter': "You are Stasik, a UAV airflow sensing expert. Provide specific parameter guidance and configuration advice based on the comprehensive knowledge provided.",
            'latest': "You are Stasik, a UAV airflow sensing expert. Discuss the latest developments and innovations based on recent patents, research, and current information provided.",
            'research': "You are Stasik, a UAV airflow sensing expert. Provide research-based insights and technical analysis based on the comprehensive scientific knowledge provided.",
            'professional': "You are Stasik, a UAV airflow sensing expert. Share professional insights and industry best practices based on the comprehensive knowledge provided.",
            'integration': "You are Stasik, a UAV airflow sensing expert. Provide detailed integration guidance and technical implementation advice based on the comprehensive knowledge provided.",
            'general': "You are Stasik, a UAV airflow sensing expert. Provide comprehensive, authoritative information based on the extensive knowledge provided."
        }
        
        system_prompt = system_prompts.get(intent, system_prompts['general'])
        
        full_system_prompt = f"""{system_prompt}

IMPORTANT GUIDELINES:
- Respond naturally as Stasik, the expert consultant
- Use the comprehensive knowledge provided to give authoritative answers
- Include specific technical details, patent insights, and research findings when relevant
- Mention recent developments when discussing current topics
- Provide practical, implementable advice
- Be conversational but professional
- Don't mention the knowledge base structure or technical processes
- Focus on answering the user's question comprehensively

COMPREHENSIVE KNOWLEDGE CONTEXT:
{knowledge_context}

User Question: "{question}"

Provide a comprehensive, natural response as Stasik, the UAV airflow sensing expert."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-5-2025-08-07",
                messages=[
                    {"role": "system", "content": full_system_prompt},
                    {"role": "user", "content": question}
                ]
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback response using knowledge context directly
            return f"""Based on my comprehensive analysis of patents and research in UAV airflow sensing:

{knowledge_context}

Regarding your question about "{question}", this involves advanced sensor technologies that require careful consideration of multiple factors including system integration, calibration procedures, and environmental conditions. 

Would you like me to elaborate on any specific aspect of this technology?"""
    
    def run_natural_chat(self):
        """Run natural language chat interface"""
        
        self.display_banner()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\nThank you for consulting with Stasik! Feel free to return anytime for UAV airflow sensing expertise.")
                    break
                
                if not user_input:
                    continue
                
                print("\nStasik: ", end="")
                
                # Generate natural language response
                response = self.understand_and_respond(user_input)
                
                print(response)
                print()
                
                # Store conversation
                self.conversation_history.append({
                    "user": user_input,
                    "stasik": response,
                    "timestamp": datetime.now().isoformat()
                })
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nI apologize, I encountered an issue: {e}")
                print("Please try rephrasing your question.\n")

def main():
    """Main function for natural language Stasik"""
    try:
        stasik = NaturalLanguageStasik()
        stasik.run_natural_chat()
    except Exception as e:
        print(f"Failed to initialize Stasik: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()