#!/usr/bin/env python3
"""
Stasik Agent Natural Language Chat Interface
Natural language interface using GPT-4 for query understanding and Stasik knowledge
"""

import os
import sys
import json
import re
from datetime import datetime
from stasik_agent import StasikAgent

try:
    import openai
except ImportError:
    print("❌ OpenAI library not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai>=1.0.0"])
    import openai

class StasikNaturalChat:
    def __init__(self, api_key=None):
        """Initialize with OpenAI API key"""
        self.agent = StasikAgent()
        self.session_start = datetime.now()
        self.query_count = 0
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
        """Display welcome banner"""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║              Stasik Agent Natural Chat                  ║")
        print("║         UAV Airflow Sensing Knowledge Expert            ║")
        print("║              GPT-5 + Stasik Knowledge                   ║")
        print("║                     Version 1.0                         ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()
        
        # Get agent info
        info = self.agent.get_agent_info()
        print(f"🤖 Agent: {info['agent_name']}")
        print(f"📊 Domain: {info['domain']}")
        print(f"✅ Status: {info['status']}")
        print(f"📚 Knowledge: 1,100 patents + 500 papers + 15+ forums")
        print(f"🧠 AI Model: GPT-5 (gpt-5-2025-08-07)")
        print()
        
        print("💬 Natural Language Interface - Ask me anything about UAV airflow sensors!")
        print("📝 Examples:")
        print("  • What's the difference between pitot tubes and MEMS sensors?")
        print("  • How do I integrate a multi-hole probe with ArduPilot?")
        print("  • What are the best anemometers for small UAVs?")
        print("  • Help me calibrate my pitot tube sensor")
        print("  • Which sensor is better for windy conditions?")
        print()
        print("🚪 Type 'exit' or 'quit' to end the session")
        print("═" * 62)
    
    def understand_query(self, user_input):
        """Use GPT-5 to understand user intent and extract Stasik query parameters"""
        
        system_prompt = f"""You are a query understanding assistant for Stasik, a UAV airflow sensing knowledge agent.

Stasik's Knowledge Base:
- 1,100 authentic patents from Google BigQuery
- 500 scientific papers 
- Professional insights from 15+ communities
- Theoretical physics framework

Supported Technologies:
1. pitot_tubes - Pressure-based airspeed measurement
2. multi_hole_probes - Advanced directional flow measurement  
3. anemometers - Wind speed and direction sensors
4. mems_sensors - Miniaturized airflow sensing devices

Available Query Types:
1. overview - Technology description, principles, advantages
2. applications - Use cases and suitability
3. integration - Hardware/software integration guidance
4. comparison - Compare technologies

Available Methods:
1. query_technology(technology, query_type) - Get technology information
2. analyze_system_integration(sensor, platform, requirements) - System analysis
3. get_professional_guidance(topic, context) - Expert guidance

Platforms: ardupilot, px4, custom
Guidance Topics: calibration, troubleshooting, installation, maintenance

Analyze the user's question and return a JSON response with:
{{
    "intent": "query_technology|system_analysis|professional_guidance|comparison|general",
    "method": "query_technology|analyze_system_integration|get_professional_guidance",
    "parameters": {{
        "technology": "pitot_tubes|multi_hole_probes|anemometers|mems_sensors",
        "query_type": "overview|applications|integration|comparison",
        "sensor": "sensor_name",
        "platform": "ardupilot|px4|custom",
        "topic": "guidance_topic",
        "context": "context"
    }},
    "explanation": "Brief explanation of what the user is asking",
    "requires_comparison": true/false,
    "technologies_to_compare": ["tech1", "tech2"]
}}

If the question is about comparing technologies, set requires_comparison to true and list the technologies.
If unclear, ask for clarification.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-5-2025-08-07",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User question: {user_input}"}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                return json.loads(result)
            except:
                # If JSON parsing fails, extract key information with regex
                return self.fallback_intent_parsing(user_input, result)
                
        except Exception as e:
            print(f"⚠️ GPT processing error: {e}")
            return self.fallback_intent_parsing(user_input, "")
    
    def fallback_intent_parsing(self, user_input, gpt_response=""):
        """Fallback intent parsing using keyword matching"""
        user_lower = user_input.lower()
        
        # Technology detection
        tech_keywords = {
            'pitot_tubes': ['pitot', 'pitot tube', 'pitot-tube'],
            'multi_hole_probes': ['multi-hole', 'multi hole', 'probe', 'probes'],
            'anemometers': ['anemometer', 'anemometers', 'wind sensor'],
            'mems_sensors': ['mems', 'mems sensor', 'mems sensors', 'micro']
        }
        
        detected_techs = []
        for tech, keywords in tech_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                detected_techs.append(tech)
        
        # Intent detection
        if any(word in user_lower for word in ['difference', 'compare', 'vs', 'versus', 'better', 'which']):
            if len(detected_techs) >= 2:
                return {
                    "intent": "comparison",
                    "method": "query_technology", 
                    "parameters": {"technology": detected_techs[0], "query_type": "comparison"},
                    "explanation": f"Comparing {detected_techs[0]} with other technologies",
                    "requires_comparison": True,
                    "technologies_to_compare": detected_techs
                }
        
        if any(word in user_lower for word in ['integrate', 'integration', 'ardupilot', 'px4']):
            platform = 'ardupilot' if 'ardupilot' in user_lower else 'px4' if 'px4' in user_lower else 'custom'
            if detected_techs:
                return {
                    "intent": "system_analysis",
                    "method": "analyze_system_integration",
                    "parameters": {"sensor": detected_techs[0], "platform": platform},
                    "explanation": f"System integration analysis for {detected_techs[0]} with {platform}"
                }
        
        if any(word in user_lower for word in ['calibrate', 'calibration', 'troubleshoot', 'help', 'guidance']):
            topic = 'calibration' if 'calibrat' in user_lower else 'troubleshooting' if 'troubleshoot' in user_lower else 'general'
            context = 'ardupilot' if 'ardupilot' in user_lower else 'px4' if 'px4' in user_lower else 'general'
            return {
                "intent": "professional_guidance",
                "method": "get_professional_guidance",
                "parameters": {"topic": topic, "context": context},
                "explanation": f"Professional guidance on {topic}"
            }
        
        # Default to overview if technology detected
        if detected_techs:
            return {
                "intent": "query_technology",
                "method": "query_technology",
                "parameters": {"technology": detected_techs[0], "query_type": "overview"},
                "explanation": f"Technology overview for {detected_techs[0]}"
            }
        
        return {
            "intent": "unclear",
            "method": None,
            "parameters": {},
            "explanation": "Could not understand the question clearly"
        }
    
    def execute_stasik_query(self, intent_data):
        """Execute the appropriate Stasik agent method based on intent"""
        method = intent_data.get('method')
        params = intent_data.get('parameters', {})
        
        try:
            if method == 'query_technology':
                return self.agent.query_technology(
                    params.get('technology', ''),
                    params.get('query_type', 'overview')
                )
            elif method == 'analyze_system_integration':
                return self.agent.analyze_system_integration(
                    params.get('sensor', ''),
                    params.get('platform', 'custom'),
                    params.get('requirements', {})
                )
            elif method == 'get_professional_guidance':
                return self.agent.get_professional_guidance(
                    params.get('topic', 'general'),
                    params.get('context', 'general')
                )
            else:
                return {"status": "error", "message": "Unknown method"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def generate_natural_response(self, user_question, stasik_result, intent_data):
        """Use GPT-5 to generate natural language response from Stasik data"""
        
        system_prompt = f"""You are Stasik, an expert UAV airflow sensing knowledge agent. You have access to:
- 1,100 authentic patents from Google BigQuery 
- 500 scientific papers
- Professional insights from 15+ technical communities
- Advanced theoretical physics framework

Your personality:
- Professional but friendly UAV/drone expert
- Provide detailed technical information when appropriate
- Use specific data from your knowledge base
- Be practical and implementation-focused
- Reference patents, professional insights, and real-world applications

User asked: "{user_question}"
Intent: {intent_data.get('explanation', 'General query')}

Stasik Knowledge Base Result:
{json.dumps(stasik_result, indent=2)}

Generate a natural, conversational response that:
1. Directly answers the user's question
2. Uses the specific data from Stasik's knowledge base
3. Provides practical insights and recommendations
4. Mentions relevant patents/professional insights when appropriate
5. Stays focused on UAV airflow sensing technologies
6. Is helpful for implementation and decision-making

Keep response comprehensive but readable (2-4 paragraphs).
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-5-2025-08-07",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Generate natural response based on the Stasik data provided."}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️ GPT response generation error: {e}")
            # Fallback to structured display
            return self.fallback_response(stasik_result)
    
    def fallback_response(self, stasik_result):
        """Fallback response formatting if GPT fails"""
        if stasik_result.get('status') != 'success':
            return f"❌ {stasik_result.get('message', 'Query failed')}"
        
        response = f"✅ Query successful!\n\n"
        
        # Format based on result type
        if 'overview' in stasik_result:
            overview = stasik_result['overview']
            response += f"📝 {overview.get('description', 'N/A')}\n"
            response += f"🔬 Principle: {overview.get('principle', 'N/A')}\n"
            response += f"📈 Patent Activity: {overview.get('patent_activity', 'N/A')}\n"
        
        if 'professional_insights' in stasik_result:
            response += "\n👨‍💼 Professional Insights Available"
            
        return response
    
    def process_comparison_query(self, intent_data):
        """Handle comparison queries by getting data for multiple technologies"""
        technologies = intent_data.get('technologies_to_compare', [])
        
        if len(technologies) < 2:
            return {"status": "error", "message": "Need at least 2 technologies to compare"}
        
        comparison_data = {}
        for tech in technologies[:2]:  # Compare first 2 technologies
            result = self.agent.query_technology(tech, "overview")
            if result.get('status') == 'success':
                comparison_data[tech] = result
        
        return {
            "status": "success",
            "comparison_type": "multi_technology",
            "technologies": list(comparison_data.keys()),
            "data": comparison_data
        }
    
    def run_chat(self):
        """Main natural language chat loop"""
        self.display_banner()
        
        print(f"🚀 Stasik Natural Language Interface ready!")
        print(f"💬 Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                    
                self.query_count += 1
                
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print(f"\n👋 Thanks for using Stasik Agent!")
                    print(f"📊 Session summary: {self.query_count} queries processed")
                    session_duration = datetime.now() - self.session_start
                    print(f"⏱️ Session duration: {str(session_duration).split('.')[0]}")
                    break
                
                print("🤔 Understanding your question...")
                
                # Understand user intent
                intent_data = self.understand_query(user_input)
                
                if intent_data.get('intent') == 'unclear':
                    print("❓ I'm not sure what you're asking about. Could you please:")
                    print("  • Mention a specific technology (pitot tubes, MEMS sensors, etc.)")
                    print("  • Ask about integration with ArduPilot or PX4")  
                    print("  • Request calibration or troubleshooting help")
                    continue
                
                print(f"🎯 {intent_data.get('explanation', 'Processing query...')}")
                
                # Handle comparison queries specially
                if intent_data.get('requires_comparison'):
                    stasik_result = self.process_comparison_query(intent_data)
                else:
                    stasik_result = self.execute_stasik_query(intent_data)
                
                if stasik_result.get('status') != 'success':
                    print(f"❌ {stasik_result.get('message', 'Query failed')}")
                    continue
                
                print("🧠 Generating response...")
                
                # Generate natural language response
                natural_response = self.generate_natural_response(
                    user_input, stasik_result, intent_data
                )
                
                print(f"\n🤖 Stasik: {natural_response}")
                print("─" * 60)
                
                # Store in conversation history
                self.conversation_history.append({
                    'user': user_input,
                    'intent': intent_data,
                    'stasik_result': stasik_result,
                    'response': natural_response,
                    'timestamp': datetime.now().isoformat()
                })
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Exiting Stasik Natural Language Chat...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Please try rephrasing your question.")

def main():
    """Main entry point"""
    # Check for API key in command line argument
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    try:
        chat = StasikNaturalChat(api_key=api_key)
        chat.run_chat()
    except Exception as e:
        print(f"❌ Failed to start Stasik Natural Language Chat: {e}")
        print("\nUsage:")
        print("  python natural_chat.py [OPENAI_API_KEY]")
        print("  OR set OPENAI_API_KEY environment variable")
        sys.exit(1)

if __name__ == "__main__":
    main()