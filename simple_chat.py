#!/usr/bin/env python3
"""
Simple Stasik Chat Interface
Direct knowledge base access without GPT dependency
"""

from stasik_agent import StasikAgent
from datetime import datetime

class SimpleStasikChat:
    def __init__(self):
        self.agent = StasikAgent()
        self.session_start = datetime.now()
        self.query_count = 0
    
    def display_banner(self):
        """Display welcome banner"""
        print("=" * 60)
        print("                 Simple Stasik Chat")
        print("           UAV Airflow Sensing Expert")
        print("            Direct Knowledge Access")
        print("=" * 60)
        print()
        
        info = self.agent.get_agent_info()
        print(f"[Agent] {info['agent_name']} v{info['version']}")
        print(f"[Domain] {info['domain']}")
        print(f"[Status] {info['status']}")
        print(f"[Knowledge] 1,100 patents + 500 papers + 15+ forums")
        print()
        
        print("[Commands]")
        print("  compare <tech1> <tech2>  - Compare two technologies")
        print("  overview <technology>    - Get technology overview")
        print("  integrate <tech> <platform> - Integration analysis")
        print("  guidance <topic>         - Professional guidance")
        print("  list                     - List technologies")
        print("  exit                     - Quit")
        print()
        
        print("[Technologies] pitot_tubes, multi_hole_probes, anemometers, mems_sensors")
        print("=" * 60)
    
    def compare_technologies(self, tech1, tech2):
        """Compare two technologies directly"""
        print(f"\n[Comparison] {tech1.replace('_', ' ').title()} vs {tech2.replace('_', ' ').title()}")
        print("-" * 50)
        
        # Get overviews of both technologies
        result1 = self.agent.query_technology(tech1, "overview")
        result2 = self.agent.query_technology(tech2, "overview")
        
        if result1['status'] == 'success' and result2['status'] == 'success':
            overview1 = result1['overview']
            overview2 = result2['overview']
            
            print(f"\n[{tech1.replace('_', ' ').title()}]")
            print(f"  Description: {overview1['description']}")
            print(f"  Principle: {overview1['principle']}")
            print(f"  Patent Activity: {overview1['patent_activity']}")
            print(f"  Professional Status: {overview1['professional_status']}")
            
            print(f"\n[{tech2.replace('_', ' ').title()}]")
            print(f"  Description: {overview2['description']}")
            print(f"  Principle: {overview2['principle']}")
            print(f"  Patent Activity: {overview2['patent_activity']}")
            print(f"  Professional Status: {overview2['professional_status']}")
            
            # Extract patent numbers for comparison
            patent1 = overview1['patent_activity'].split()[0] if overview1['patent_activity'] else "N/A"
            patent2 = overview2['patent_activity'].split()[0] if overview2['patent_activity'] else "N/A"
            
            print(f"\n[Key Differences]")
            print(f"  Patent Activity: {tech1.replace('_', ' ').title()} ({patent1}) vs {tech2.replace('_', ' ').title()} ({patent2})")
            
            # Determine maturity
            status1 = overview1['professional_status'].lower()
            status2 = overview2['professional_status'].lower()
            
            if "specialized" in status1 and "challenges" in status2:
                print(f"  Maturity: {tech1.replace('_', ' ').title()} is more specialized, {tech2.replace('_', ' ').title()} is emerging")
            elif "standard" in status1 and "challenges" in status2:
                print(f"  Maturity: {tech1.replace('_', ' ').title()} is established, {tech2.replace('_', ' ').title()} is emerging")
            
            # Application focus
            if "comprehensive" in overview1['description'] and "miniaturized" in overview2['description']:
                print(f"  Application: {tech1.replace('_', ' ').title()} for advanced research, {tech2.replace('_', ' ').title()} for compact systems")
        else:
            print("[ERROR] Could not retrieve technology information")
    
    def show_overview(self, technology):
        """Show technology overview"""
        result = self.agent.query_technology(technology, "overview")
        
        if result['status'] == 'success':
            overview = result['overview']
            print(f"\n[Overview] {technology.replace('_', ' ').title()}")
            print("-" * 40)
            print(f"Description: {overview['description']}")
            print(f"Principle: {overview['principle']}")
            print(f"Patent Activity: {overview['patent_activity']}")
            print(f"Professional Status: {overview['professional_status']}")
            
            if 'advantages' in overview:
                print("Advantages:")
                for adv in overview['advantages']:
                    print(f"  • {adv}")
        else:
            print(f"[ERROR] {result.get('message', 'Unknown error')}")
    
    def show_integration(self, technology, platform):
        """Show integration analysis"""
        result = self.agent.analyze_system_integration(technology, platform)
        
        if result['status'] == 'success':
            print(f"\n[Integration] {technology.replace('_', ' ').title()} + {platform.title()}")
            print("-" * 40)
            
            if 'sensor_integration' in result:
                integration = result['sensor_integration']
                print("Integration Details:")
                for key, value in integration.items():
                    if isinstance(value, list):
                        print(f"  {key.replace('_', ' ').title()}:")
                        for item in value[:3]:  # Show first 3 items
                            print(f"    • {item}")
                    else:
                        print(f"  {key.replace('_', ' ').title()}: {value}")
        else:
            print(f"[ERROR] {result.get('message', 'Unknown error')}")
    
    def show_guidance(self, topic):
        """Show professional guidance"""
        result = self.agent.get_professional_guidance(topic, "general")
        
        if result['status'] == 'success':
            print(f"\n[Professional Guidance] {topic.title()}")
            print("-" * 40)
            print(f"Topic: {result['topic']}")
            print("Guidance available from professional communities")
        else:
            print(f"[ERROR] {result.get('message', 'Unknown error')}")
    
    def parse_command(self, user_input):
        """Parse user command"""
        parts = user_input.strip().split()
        if not parts:
            return None, []
        return parts[0].lower(), parts[1:]
    
    def run_chat(self):
        """Main chat loop"""
        self.display_banner()
        
        print("[Ready] Ask about UAV airflow sensors!")
        print(f"[Session] Started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        while True:
            try:
                user_input = input("[You] > ").strip()
                
                if not user_input:
                    continue
                
                self.query_count += 1
                command, args = self.parse_command(user_input)
                
                if command in ['exit', 'quit', 'bye']:
                    print(f"\n[Goodbye] Thanks for using Stasik!")
                    print(f"[Stats] {self.query_count} queries processed")
                    break
                
                elif command == 'compare':
                    if len(args) >= 2:
                        self.compare_technologies(args[0], args[1])
                    else:
                        print("[Usage] compare <tech1> <tech2>")
                        print("[Example] compare multi_hole_probes mems_sensors")
                
                elif command == 'overview':
                    if args:
                        self.show_overview(args[0])
                    else:
                        print("[Usage] overview <technology>")
                        print("[Example] overview pitot_tubes")
                
                elif command == 'integrate':
                    if len(args) >= 2:
                        self.show_integration(args[0], args[1])
                    else:
                        print("[Usage] integrate <technology> <platform>")
                        print("[Example] integrate mems_sensors ardupilot")
                
                elif command == 'guidance':
                    if args:
                        self.show_guidance(args[0])
                    else:
                        print("[Usage] guidance <topic>")
                        print("[Example] guidance calibration")
                
                elif command == 'list':
                    technologies = ["pitot_tubes", "multi_hole_probes", "anemometers", "mems_sensors"]
                    print("[Technologies]")
                    for i, tech in enumerate(technologies, 1):
                        print(f"  {i}. {tech}")
                
                else:
                    print(f"[Unknown] Command '{command}' not recognized")
                    print("[Help] Available commands: compare, overview, integrate, guidance, list, exit")
                
                print()
                
            except KeyboardInterrupt:
                print(f"\n\n[Exit] Goodbye!")
                break
            except Exception as e:
                print(f"[ERROR] {e}")

def main():
    chat = SimpleStasikChat()
    chat.run_chat()

if __name__ == "__main__":
    main()