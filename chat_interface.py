#!/usr/bin/env python3
"""
Stasik Agent Chat Interface
Interactive command-line interface for UAV airflow sensing knowledge queries
"""

import os
import sys
import json
from datetime import datetime
from stasik_agent import StasikAgent

class StasikChat:
    def __init__(self):
        self.agent = StasikAgent()
        self.session_start = datetime.now()
        self.query_count = 0
        
    def display_banner(self):
        """Display welcome banner"""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                    Stasik Agent Chat                     ║")
        print("║           UAV Airflow Sensing Knowledge Expert          ║")
        print("║                     Version 1.0                         ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()
        
        # Get agent info
        info = self.agent.get_agent_info()
        print(f"🤖 Agent: {info['agent_name']}")
        print(f"📊 Domain: {info['domain']}")
        print(f"✅ Status: {info['status']}")
        print(f"📚 Knowledge: {len(info['supported_technologies'])} technologies")
        print()
        
        # Display help
        self.display_help()
    
    def display_help(self):
        """Display available commands and usage"""
        print("💡 Available Commands:")
        print("  📖 overview <technology>     - Get technology overview")
        print("  🔧 applications <technology> - Get application scenarios")
        print("  ⚙️  integration <technology>  - Get integration guidance")
        print("  ⚖️  comparison <technology>   - Compare with other technologies")
        print("  🎯 analyze <sensor> <platform> - System integration analysis")
        print("  👨‍💼 guidance <topic> [context]  - Professional guidance")
        print("  ℹ️  info                      - Agent information")
        print("  📋 list                      - List supported technologies")
        print("  ❓ help                      - Show this help")
        print("  🚪 exit/quit                 - Exit chat")
        print()
        
        print("🔍 Supported Technologies:")
        technologies = self.agent.get_agent_info()['supported_technologies']
        for i, tech in enumerate(technologies, 1):
            print(f"  {i}. {tech.replace('_', ' ').title()}")
        print()
        
        print("💼 Professional Guidance Topics:")
        print("  • calibration, troubleshooting, installation, maintenance")
        print("  • Context: ardupilot, px4, mems, general")
        print()
        
        print("📝 Examples:")
        print("  > overview pitot_tubes")
        print("  > analyze mems_sensors ardupilot")  
        print("  > guidance calibration ardupilot")
        print("═" * 62)
    
    def parse_command(self, user_input):
        """Parse user command and arguments"""
        parts = user_input.strip().split()
        if not parts:
            return None, []
            
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        return command, args
    
    def handle_technology_query(self, query_type, args):
        """Handle technology-specific queries"""
        if not args:
            print("❌ Please specify a technology. Available: pitot_tubes, multi_hole_probes, anemometers, mems_sensors")
            return
            
        technology = args[0].lower()
        
        # Normalize common variations
        tech_mapping = {
            'pitot': 'pitot_tubes',
            'pitot_tube': 'pitot_tubes',
            'multi_hole': 'multi_hole_probes',
            'multi-hole': 'multi_hole_probes',
            'probe': 'multi_hole_probes',
            'probes': 'multi_hole_probes',
            'anemometer': 'anemometers',
            'wind': 'anemometers',
            'mems': 'mems_sensors',
            'mems_sensor': 'mems_sensors'
        }
        
        technology = tech_mapping.get(technology, technology)
        
        print(f"🔍 Querying {technology.replace('_', ' ').title()} - {query_type.title()}...")
        
        result = self.agent.query_technology(technology, query_type)
        self.display_query_result(result)
    
    def handle_system_analysis(self, args):
        """Handle system integration analysis"""
        if len(args) < 2:
            print("❌ Usage: analyze <sensor> <platform>")
            print("   Example: analyze pitot_tubes ardupilot")
            return
            
        sensor = args[0].lower()
        platform = args[1].lower()
        
        print(f"⚙️ Analyzing {sensor} integration with {platform}...")
        
        result = self.agent.analyze_system_integration(sensor, platform)
        self.display_integration_result(result)
    
    def handle_professional_guidance(self, args):
        """Handle professional guidance requests"""
        if not args:
            print("❌ Please specify a topic. Examples: calibration, troubleshooting, installation")
            return
            
        topic = args[0].lower()
        context = args[1].lower() if len(args) > 1 else "general"
        
        print(f"👨‍💼 Getting professional guidance on {topic} ({context})...")
        
        result = self.agent.get_professional_guidance(topic, context)
        self.display_guidance_result(result)
    
    def display_query_result(self, result):
        """Display technology query result"""
        print("═" * 60)
        
        if result['status'] != 'success':
            print(f"❌ {result.get('message', 'Query failed')}")
            if 'available_technologies' in result:
                print("📋 Available technologies:", ", ".join(result['available_technologies']))
            return
        
        print(f"✅ Technology: {result['technology'].replace('_', ' ').title()}")
        print(f"📊 Query Type: {result['query_type'].title()}")
        print(f"🕒 Timestamp: {result['timestamp']}")
        print()
        
        # Display content based on query type
        if result['query_type'] == 'overview' and 'overview' in result:
            overview = result['overview']
            print(f"📝 Description: {overview.get('description', 'N/A')}")
            print(f"🔬 Principle: {overview.get('principle', 'N/A')}")
            print(f"📈 Patent Activity: {overview.get('patent_activity', 'N/A')}")
            print(f"🏭 Professional Status: {overview.get('professional_status', 'N/A')}")
            
            if 'advantages' in overview:
                print("\n✅ Advantages:")
                for adv in overview['advantages']:
                    print(f"  • {adv}")
                    
        elif result['query_type'] == 'applications' and 'applications' in result:
            apps = result['applications']
            print("🎯 Applications:")
            for app in apps:
                print(f"  • {app.get('application', 'N/A')} - {app.get('suitability', 'N/A')}")
                
        elif result['query_type'] == 'integration' and 'integration' in result:
            integration = result['integration']
            print("⚙️ Integration Guidance:")
            for key, value in integration.items():
                print(f"  {key.title()}: {value}")
                
        elif result['query_type'] == 'comparison' and 'comparison' in result:
            comparison = result['comparison']
            print("⚖️ Technology Comparison:")
            for key, value in comparison.items():
                print(f"  {key.title()}: {value}")
        
        print("═" * 60)
    
    def display_integration_result(self, result):
        """Display integration analysis result"""
        print("═" * 60)
        
        if result['status'] != 'success':
            print(f"❌ {result.get('message', 'Analysis failed')}")
            return
            
        print(f"⚙️ System Integration Analysis")
        print(f"🎯 Sensor: {result['primary_sensor'].replace('_', ' ').title()}")
        print(f"🖥️ Platform: {result['platform'].title()}")
        print()
        
        if 'sensor_integration' in result:
            print("🔧 Sensor Integration:")
            integration = result['sensor_integration']
            for key, value in integration.items():
                if isinstance(value, list):
                    print(f"  {key.title()}:")
                    for item in value:
                        print(f"    • {item}")
                else:
                    print(f"  {key.title()}: {value}")
            print()
            
        if 'professional_insights' in result:
            print("👨‍💼 Professional Insights:")
            insights = result['professional_insights']
            for key, value in insights.items():
                if isinstance(value, list):
                    print(f"  {key.title()}:")
                    for item in value:
                        print(f"    • {item}")
                else:
                    print(f"  {key.title()}: {value}")
        
        print("═" * 60)
    
    def display_guidance_result(self, result):
        """Display professional guidance result"""
        print("═" * 60)
        
        if result['status'] != 'success':
            print(f"❌ {result.get('message', 'Guidance request failed')}")
            return
            
        print(f"👨‍💼 Professional Guidance: {result['topic'].title()}")
        print(f"🏷️ Context: {result['context'].title()}")
        print()
        
        # Display guidance content
        for key, value in result.items():
            if key in ['status', 'agent', 'topic', 'context', 'timestamp', 'source']:
                continue
                
            print(f"📋 {key.replace('_', ' ').title()}:")
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list):
                        print(f"  {subkey.replace('_', ' ').title()}:")
                        for item in subvalue:
                            print(f"    • {item}")
                    else:
                        print(f"  {subkey.replace('_', ' ').title()}: {subvalue}")
            elif isinstance(value, list):
                for item in value:
                    print(f"  • {item}")
            else:
                print(f"  {value}")
            print()
        
        print("═" * 60)
    
    def run_chat(self):
        """Main chat loop"""
        self.display_banner()
        
        print(f"🚀 Stasik Agent ready! Type 'help' for commands or 'exit' to quit.")
        print(f"💬 Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        while True:
            try:
                user_input = input("🤖 Stasik> ").strip()
                
                if not user_input:
                    continue
                    
                self.query_count += 1
                command, args = self.parse_command(user_input)
                
                if command in ['exit', 'quit', 'q']:
                    print(f"\n👋 Thanks for using Stasik Agent!")
                    print(f"📊 Session summary: {self.query_count} queries processed")
                    session_duration = datetime.now() - self.session_start
                    print(f"⏱️ Session duration: {str(session_duration).split('.')[0]}")
                    break
                    
                elif command == 'help':
                    self.display_help()
                    
                elif command == 'info':
                    info = self.agent.get_agent_info()
                    print("═" * 60)
                    for key, value in info.items():
                        if isinstance(value, list):
                            print(f"{key.replace('_', ' ').title()}:")
                            for item in value:
                                print(f"  • {item}")
                        else:
                            print(f"{key.replace('_', ' ').title()}: {value}")
                    print("═" * 60)
                    
                elif command == 'list':
                    technologies = self.agent.get_agent_info()['supported_technologies']
                    print("📋 Supported Technologies:")
                    for i, tech in enumerate(technologies, 1):
                        print(f"  {i}. {tech}")
                    
                elif command in ['overview', 'applications', 'integration', 'comparison']:
                    self.handle_technology_query(command, args)
                    
                elif command == 'analyze':
                    self.handle_system_analysis(args)
                    
                elif command == 'guidance':
                    self.handle_professional_guidance(args)
                    
                else:
                    print(f"❓ Unknown command: '{command}'. Type 'help' for available commands.")
                
                print()  # Add spacing between queries
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Exiting Stasik Agent chat...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Type 'help' for usage information.")

def main():
    """Main entry point"""
    try:
        chat = StasikChat()
        chat.run_chat()
    except Exception as e:
        print(f"❌ Failed to start Stasik Agent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()