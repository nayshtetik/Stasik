#!/usr/bin/env python3
"""
Enhanced Stasik Agent Integrated Natural Language Chat
GPT-5 + Enhanced Stasik Knowledge Base with ArduPilot Integration
"""

import os
import sys
import json
import re
from datetime import datetime
from enhanced_stasik_agent import EnhancedStasikAgent

try:
    import openai
except ImportError:
    print("[INFO] OpenAI library not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai>=1.0.0"])
    import openai

class IntegratedStasikChat:
    def __init__(self, api_key=None):
        """Initialize with Enhanced Stasik Agent and OpenAI API key"""
        self.agent = EnhancedStasikAgent()
        self.session_start = datetime.now()
        self.query_count = 0
        self.knowledge_usage_log = []
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
        print("=" * 62)
        print("              Stasik Agent Integrated Chat")
        print("         GPT-5 + UAV Airflow Sensing Knowledge")
        print("              With Knowledge Base Logging")
        print("                     Version 1.0")
        print("=" * 62)
        print()
        
        # Get agent info
        info = self.agent.get_agent_info()
        print(f"[Agent] {info['agent_name']}")
        print(f"[Domain] {info['domain']}")
        print(f"[Status] {info['status']}")
        print(f"[Knowledge] 1,100 patents + 500 papers + 15+ forums")
        print(f"[AI Model] GPT-5 (gpt-5-2025-08-07)")
        print(f"[Integration] Knowledge Base + GPT-5 Response Generation")
        print()
        
        print("[Interface] Natural Language - Powered by YOUR knowledge base!")
        print("[Examples]")
        print("  * What's the difference between pitot tubes and MEMS sensors?")
        print("  * How do I integrate a multi-hole probe with ArduPilot?")
        print("  * Which sensor is better for windy conditions?")
        print("  * Help me calibrate my pitot tube sensor")
        print()
        print("[Exit] Type 'exit' or 'quit' to end the session")
        print("=" * 62)
    
    def log_knowledge_usage(self, query_type, technology, result):
        """Log knowledge base usage"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query_type": query_type,
            "technology": technology,
            "status": result.get("status", "unknown"),
            "data_retrieved": bool(result.get("status") == "success")
        }
        self.knowledge_usage_log.append(log_entry)
        
        # Print usage log
        print(f"[KNOWLEDGE LOG] {query_type.upper()} query for {technology} - Status: {result.get('status', 'unknown')}")
    
    def understand_and_query_stasik(self, user_input):
        """Understand user intent and query Stasik knowledge base"""
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
        
        stasik_results = {}
        
        # Query knowledge base for detected technologies
        if detected_techs:
            print(f"[KNOWLEDGE ACCESS] Detected technologies: {', '.join(detected_techs)}")
            
            for tech in detected_techs[:2]:  # Limit to 2 technologies
                # Get overview
                overview_result = self.agent.query_technology(tech, "overview")
                self.log_knowledge_usage("overview", tech, overview_result)
                stasik_results[f"{tech}_overview"] = overview_result
                
                # Get applications if mentioned
                if any(word in user_lower for word in ['application', 'use', 'used']):
                    app_result = self.agent.query_technology(tech, "applications")
                    self.log_knowledge_usage("applications", tech, app_result)
                    stasik_results[f"{tech}_applications"] = app_result
                
                # Get ArduPilot integration if mentioned  
                if any(word in user_lower for word in ['integrate', 'integration', 'ardupilot']):
                    int_result = self.agent.query_ardupilot_integration(tech)
                    self.log_knowledge_usage("ardupilot_integration", tech, int_result)
                    stasik_results[f"{tech}_ardupilot_integration"] = int_result
                
                # Get enhanced system integration for comprehensive queries
                if any(word in user_lower for word in ['system', 'complete', 'design']):
                    platform = 'ardupilot' if 'ardupilot' in user_lower else 'px4' if 'px4' in user_lower else 'ardupilot'
                    sys_result = self.agent.analyze_enhanced_system_integration(tech, platform)
                    self.log_knowledge_usage("system_integration", f"{tech}+{platform}", sys_result)
                    stasik_results[f"{tech}_system_integration"] = sys_result
            
            # Handle comparison queries
            if len(detected_techs) >= 2 and any(word in user_lower for word in ['difference', 'compare', 'vs', 'versus', 'better', 'which']):
                print(f"[KNOWLEDGE ACCESS] Comparison query detected")
                comp_result = self.agent.query_technology(detected_techs[0], "comparison")
                self.log_knowledge_usage("comparison", f"{detected_techs[0]}_vs_others", comp_result)
                stasik_results["comparison"] = comp_result
        
        # ArduPilot parameter queries
        ardupilot_params = ['ARSPD_TYPE', 'ARSPD_RATIO', 'ARSPD_AUTOCAL', 'EK3_ARSP_THR', 'EK3_ENABLE']
        for param in ardupilot_params:
            if param.lower() in user_lower:
                param_result = self.agent.get_parameter_guidance(param)
                self.log_knowledge_usage("parameter_guidance", param, param_result)
                stasik_results[f"param_{param}"] = param_result
        
        # EKF tuning queries
        if any(word in user_lower for word in ['ekf', 'ekf3', 'tuning', 'fusion', 'wind estimation']):
            ekf_result = self.agent.get_ekf_tuning_guidance('airspeed')
            self.log_knowledge_usage("ekf_tuning", "airspeed", ekf_result)
            stasik_results["ekf_tuning"] = ekf_result
        
        # Professional guidance queries
        if any(word in user_lower for word in ['calibrate', 'calibration', 'troubleshoot', 'help', 'guidance']):
            topic = 'calibration' if 'calibrat' in user_lower else 'troubleshooting' if 'troubleshoot' in user_lower else 'general'
            context = 'ardupilot' if 'ardupilot' in user_lower else 'px4' if 'px4' in user_lower else 'general'
            guide_result = self.agent.get_professional_guidance(topic, context)
            self.log_knowledge_usage("guidance", f"{topic}_{context}", guide_result)
            stasik_results["professional_guidance"] = guide_result
        
        # If no specific technologies detected, get general overview of main technologies
        if not detected_techs and not stasik_results:
            print(f"[KNOWLEDGE ACCESS] General query - retrieving main technologies overview")
            main_techs = ['pitot_tubes', 'multi_hole_probes', 'anemometers', 'mems_sensors']
            for tech in main_techs:
                overview_result = self.agent.query_technology(tech, "overview")
                self.log_knowledge_usage("overview", tech, overview_result)
                stasik_results[f"{tech}_overview"] = overview_result
        
        return stasik_results, detected_techs
    
    def generate_gpt_response_with_knowledge(self, user_question, stasik_results, detected_techs):
        """Generate GPT-5 response using Stasik knowledge base data"""
        
        # Format knowledge base data for GPT
        knowledge_summary = "STASIK KNOWLEDGE BASE DATA:\n"
        knowledge_summary += "=" * 40 + "\n"
        
        for key, result in stasik_results.items():
            if result.get("status") == "success":
                knowledge_summary += f"\n[{key.upper()}]\n"
                
                # Format overview data
                if "overview" in result:
                    overview = result["overview"]
                    knowledge_summary += f"Description: {overview.get('description', 'N/A')}\n"
                    knowledge_summary += f"Principle: {overview.get('principle', 'N/A')}\n"
                    knowledge_summary += f"Patent Activity: {overview.get('patent_activity', 'N/A')}\n"
                    knowledge_summary += f"Professional Status: {overview.get('professional_status', 'N/A')}\n"
                    if 'advantages' in overview:
                        knowledge_summary += f"Advantages: {', '.join(overview['advantages'][:3])}\n"
                
                # Format applications data
                if "applications" in result:
                    apps = result["applications"][:3]  # First 3 applications
                    knowledge_summary += "Applications:\n"
                    for app in apps:
                        knowledge_summary += f"  • {app.get('application', 'N/A')} - {app.get('suitability', 'N/A')}\n"
                
                # Format integration data
                if "sensor_integration" in result:
                    integration = result["sensor_integration"]
                    knowledge_summary += "Integration Details:\n"
                    for k, v in integration.items():
                        if isinstance(v, list):
                            knowledge_summary += f"  {k}: {', '.join(v[:2])}\n"
                        else:
                            knowledge_summary += f"  {k}: {v}\n"
                
                # Format ArduPilot integration data
                if "ardupilot_integration" in result:
                    ardupilot = result["ardupilot_integration"]
                    knowledge_summary += "ArduPilot Integration:\n"
                    if "ardupilot_drivers" in ardupilot:
                        knowledge_summary += f"  Drivers: {', '.join(ardupilot['ardupilot_drivers'][:3])}\n"
                    if "key_parameters" in ardupilot:
                        knowledge_summary += "  Parameters:\n"
                        for param, desc in list(ardupilot["key_parameters"].items())[:3]:
                            knowledge_summary += f"    {param}: {desc}\n"
                
                # Format parameter guidance
                if "parameter_details" in result:
                    param_details = result["parameter_details"]
                    knowledge_summary += f"Parameter: {result.get('parameter', 'N/A')}\n"
                    knowledge_summary += f"Description: {param_details.get('description', 'N/A')}\n"
                    if "values" in param_details:
                        knowledge_summary += "Values:\n"
                        for value, desc in list(param_details["values"].items())[:3]:
                            knowledge_summary += f"  {value}: {desc}\n"
                
                # Format EKF tuning guidance
                if "tuning_guidance" in result:
                    ekf = result["tuning_guidance"]
                    knowledge_summary += "EKF Tuning:\n"
                    if "key_parameters" in ekf:
                        knowledge_summary += "  Key Parameters:\n"
                        for param, desc in list(ekf["key_parameters"].items())[:3]:
                            knowledge_summary += f"    {param}: {desc}\n"
                    if "tuning_sequence" in ekf:
                        knowledge_summary += "  Tuning Steps:\n"
                        for step in ekf["tuning_sequence"][:3]:
                            knowledge_summary += f"    • {step}\n"
                
                # Format professional insights
                if "professional_insights" in result:
                    insights = result["professional_insights"]
                    knowledge_summary += "Professional Insights:\n"
                    for k, v in insights.items():
                        if isinstance(v, list):
                            knowledge_summary += f"  {k}: {', '.join(v[:2])}\n"
                        else:
                            knowledge_summary += f"  {k}: {v}\n"
                
                # Format ArduPilot best practices
                if "ardupilot_best_practices" in result:
                    practices = result["ardupilot_best_practices"]
                    knowledge_summary += "Best Practices:\n"
                    for practice in practices[:3]:
                        knowledge_summary += f"  • {practice}\n"
                
                knowledge_summary += "\n"
        
        # Create system prompt that emphasizes knowledge base usage
        system_prompt = f"""You are Enhanced Stasik, a specialized UAV airflow sensing and ArduPilot integration expert. You have access to a comprehensive dual knowledge base with:
- 1,100 authentic patents from Google BigQuery 
- 500 scientific papers  
- Professional insights from 15+ technical communities
- Complete ArduPilot documentation and parameter guidance
- EKF tuning and sensor fusion expertise
- Advanced theoretical physics framework

IMPORTANT: You MUST base your response primarily on the provided Enhanced Stasik knowledge base data below. Reference specific details from the knowledge base, including patent statistics, ArduPilot parameters, EKF tuning guidance, and technical integration details.

{knowledge_summary}

User asked: "{user_question}"

Generate a comprehensive response that:
1. Uses SPECIFIC data from the Enhanced Stasik knowledge base above
2. References patent statistics, ArduPilot parameters, and EKF tuning details  
3. Provides technical implementation details from the dual knowledge base
4. Mentions both UAV sensor technology AND ArduPilot integration specifics
5. Includes ArduPilot parameter values, driver recommendations, and best practices
6. Stays focused on UAV airflow sensing + ArduPilot integration applications
7. Provides practical implementation guidance based on the enhanced knowledge base

Be conversational but authoritative, demonstrating expertise in both UAV sensors and ArduPilot systems.
"""

        try:
            print("[GPT-5] Generating response with knowledge base data...")
            response = self.client.chat.completions.create(
                model="gpt-5-2025-08-07",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Based on the Stasik knowledge base data provided, answer: {user_question}"}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"[WARNING] GPT response generation error: {e}")
            # Fallback to knowledge base summary
            return self.format_knowledge_fallback(stasik_results)
    
    def format_knowledge_fallback(self, stasik_results):
        """Fallback response using direct knowledge base data"""
        response = "[KNOWLEDGE BASE RESPONSE]\n\n"
        
        for key, result in stasik_results.items():
            if result.get("status") == "success":
                response += f"{key.replace('_', ' ').title()}:\n"
                
                if "overview" in result:
                    overview = result["overview"]
                    response += f"  • {overview.get('description', 'N/A')}\n"
                    response += f"  • Principle: {overview.get('principle', 'N/A')}\n"
                    response += f"  • Patent Activity: {overview.get('patent_activity', 'N/A')}\n"
                    response += f"  • Status: {overview.get('professional_status', 'N/A')}\n"
                
                response += "\n"
        
        response += "This data comes from Stasik's knowledge base of 1,100 patents, 500 papers, and 15+ professional communities."
        return response
    
    def display_knowledge_usage_summary(self):
        """Display session knowledge usage summary"""
        if self.knowledge_usage_log:
            print("\n[KNOWLEDGE USAGE SUMMARY]")
            print("-" * 40)
            success_queries = sum(1 for log in self.knowledge_usage_log if log["data_retrieved"])
            total_queries = len(self.knowledge_usage_log)
            print(f"Total Knowledge Queries: {total_queries}")
            print(f"Successful Retrievals: {success_queries}")
            print(f"Knowledge Base Usage: {(success_queries/total_queries*100):.1f}%")
            
            # Query type breakdown
            query_types = {}
            for log in self.knowledge_usage_log:
                qt = log["query_type"]
                query_types[qt] = query_types.get(qt, 0) + 1
            
            print("\nQuery Type Breakdown:")
            for qtype, count in query_types.items():
                print(f"  {qtype}: {count}")
            print("-" * 40)
    
    def run_chat(self):
        """Main integrated chat loop"""
        self.display_banner()
        
        print("[Ready] Ask about UAV airflow sensors - powered by your knowledge base!")
        print(f"[Session] Started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        while True:
            try:
                user_input = input("[You] > ").strip()
                
                if not user_input:
                    continue
                    
                self.query_count += 1
                
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print(f"\n[Goodbye] Thanks for using Stasik Agent!")
                    print(f"[Stats] Session summary: {self.query_count} queries processed")
                    session_duration = datetime.now() - self.session_start
                    print(f"[Duration] Session time: {str(session_duration).split('.')[0]}")
                    self.display_knowledge_usage_summary()
                    break
                
                print("[Processing] Querying Stasik knowledge base...")
                
                # Query Stasik knowledge base
                stasik_results, detected_techs = self.understand_and_query_stasik(user_input)
                
                if not stasik_results:
                    print("[Help] I couldn't find relevant information in my knowledge base.")
                    print("Try mentioning: pitot tubes, multi-hole probes, anemometers, MEMS sensors")
                    continue
                
                print(f"[KNOWLEDGE RETRIEVED] {len(stasik_results)} knowledge base entries")
                
                # Generate GPT response with knowledge base data
                natural_response = self.generate_gpt_response_with_knowledge(
                    user_input, stasik_results, detected_techs
                )
                
                print(f"\n[Stasik] {natural_response}")
                print("-" * 60)
                
                # Store in conversation history
                self.conversation_history.append({
                    'user': user_input,
                    'stasik_results': stasik_results,
                    'response': natural_response,
                    'timestamp': datetime.now().isoformat()
                })
                
            except KeyboardInterrupt:
                print(f"\n\n[Exit] Exiting Stasik Integrated Chat...")
                self.display_knowledge_usage_summary()
                break
            except Exception as e:
                print(f"[ERROR] Error: {e}")
                print("[Help] Please try rephrasing your question.")

def main():
    """Main entry point"""
    # Check for API key in command line argument
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    try:
        chat = IntegratedStasikChat(api_key=api_key)
        chat.run_chat()
    except Exception as e:
        print(f"[ERROR] Failed to start Stasik Integrated Chat: {e}")
        print("\nUsage:")
        print("  python integrated_chat.py [OPENAI_API_KEY]")
        print("  OR set OPENAI_API_KEY environment variable")
        sys.exit(1)

if __name__ == "__main__":
    main()