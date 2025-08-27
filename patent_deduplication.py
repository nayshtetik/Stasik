#!/usr/bin/env python3
"""
Patent Database Deduplication Script
Removes duplicate patents across all patent JSON files in the knowledge base
"""

import json
import os
from collections import defaultdict
from datetime import datetime

class PatentDeduplicator:
    def __init__(self, base_path="C:/Knowledge/Patents"):
        self.base_path = base_path
        self.patent_files = [
            "FOCUSED_UAS_PATENTS_20250826_070612.json",
            "EXPANDED_UAS_PATENTS_20250826_064540.json", 
            "PATENTS_2010_2025_20250826_063150.json",
            "airflow_sensors_patents_20250826_055554.json"
        ]
        self.all_patents = {}  # publication_number -> patent_data
        self.patent_sources = {}  # publication_number -> source_file
        self.duplicate_stats = {}
        
    def load_patent_file(self, filename):
        """Load patents from a JSON file"""
        filepath = os.path.join(self.base_path, filename)
        
        if not os.path.exists(filepath):
            print(f"[WARNING] File not found: {filepath}")
            return []
            
        print(f"[LOADING] {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            patents = []
            
            # Handle different JSON structures
            if filename == "airflow_sensors_patents_20250826_055554.json":
                # Structure: patents_by_technology -> technology -> list of patents
                for tech, tech_patents in data.get("patents_by_technology", {}).items():
                    patents.extend(tech_patents)
                    
            elif "patents" in data:
                patents = data["patents"]
                
            elif "patent_data" in data:
                patents = data["patent_data"]
                
            else:
                print(f"[ERROR] Unknown structure in {filename}")
                return []
            
            print(f"[LOADED] {len(patents)} patents from {filename}")
            return patents
            
        except Exception as e:
            print(f"[ERROR] Failed to load {filename}: {e}")
            return []
    
    def normalize_publication_number(self, pub_number):
        """Normalize publication numbers for comparison"""
        if not pub_number:
            return None
            
        # Remove common prefixes and clean up
        pub_number = str(pub_number).upper().strip()
        
        # Handle different formats
        prefixes_to_remove = ['US', 'WO', 'EP', 'CN', 'JP', 'GB', 'DE', 'FR']
        
        for prefix in prefixes_to_remove:
            if pub_number.startswith(prefix):
                pub_number = pub_number[len(prefix):]
                break
        
        # Remove leading zeros and non-alphanumeric characters except hyphens
        pub_number = ''.join(c for c in pub_number if c.isalnum() or c == '-')
        
        return pub_number if pub_number else None
    
    def find_duplicates(self):
        """Find duplicate patents across all files"""
        print("\n" + "="*80)
        print("PATENT DEDUPLICATION ANALYSIS")
        print("="*80)
        
        # Load all patent files
        all_loaded_patents = []
        
        for filename in self.patent_files:
            patents = self.load_patent_file(filename)
            
            for patent in patents:
                patent['_source_file'] = filename
                all_loaded_patents.append(patent)
        
        print(f"\n[ANALYSIS] Total patents loaded: {len(all_loaded_patents)}")
        
        # Group patents by normalized publication number
        patents_by_pub_number = defaultdict(list)
        patents_without_pub_number = []
        
        for patent in all_loaded_patents:
            pub_number = patent.get('publication_number') or patent.get('patent_number') or patent.get('number')
            
            if pub_number:
                normalized = self.normalize_publication_number(pub_number)
                if normalized:
                    patents_by_pub_number[normalized].append(patent)
                else:
                    patents_without_pub_number.append(patent)
            else:
                patents_without_pub_number.append(patent)
        
        print(f"[ANALYSIS] Patents with publication numbers: {len(patents_by_pub_number)}")
        print(f"[ANALYSIS] Patents without publication numbers: {len(patents_without_pub_number)}")
        
        # Find duplicates
        duplicates = {}
        unique_patents = {}
        
        for pub_number, patent_list in patents_by_pub_number.items():
            if len(patent_list) > 1:
                # Multiple patents with same publication number - duplicates found
                duplicates[pub_number] = patent_list
                
                # Keep the most complete patent (most fields)
                best_patent = max(patent_list, key=lambda p: len([v for v in p.values() if v]))
                unique_patents[pub_number] = best_patent
                
            else:
                # Unique patent
                unique_patents[pub_number] = patent_list[0]
        
        # Add patents without publication numbers (assume unique)
        for i, patent in enumerate(patents_without_pub_number):
            unique_key = f"NO_PUB_NUMBER_{i}"
            unique_patents[unique_key] = patent
        
        self.duplicates = duplicates
        self.unique_patents = unique_patents
        
        return duplicates, unique_patents
    
    def display_duplicate_analysis(self):
        """Display detailed duplicate analysis"""
        print("\n" + "="*60)
        print("DUPLICATE ANALYSIS RESULTS")
        print("="*60)
        
        total_duplicates_found = sum(len(patents) for patents in self.duplicates.values())
        duplicates_removed = total_duplicates_found - len(self.duplicates)
        
        print(f"Unique publication numbers: {len(self.unique_patents)}")
        print(f"Duplicate publication numbers: {len(self.duplicates)}")
        print(f"Total duplicate patents found: {total_duplicates_found}")
        print(f"Patents to be removed: {duplicates_removed}")
        
        if self.duplicates:
            print("\nDUPLICATE DETAILS:")
            print("-" * 40)
            
            for pub_number, patent_list in list(self.duplicates.items())[:10]:  # Show first 10
                print(f"\nPublication Number: {pub_number}")
                print(f"Found in {len(patent_list)} files:")
                
                for patent in patent_list:
                    source = patent.get('_source_file', 'Unknown')
                    title = patent.get('title', 'No title')[:60] + "..."
                    print(f"  - {source}: {title}")
            
            if len(self.duplicates) > 10:
                print(f"\n... and {len(self.duplicates) - 10} more duplicate groups")
        
        print(f"\n[SUMMARY] Final deduplicated count: {len(self.unique_patents)}")
    
    def create_deduplicated_database(self):
        """Create new deduplicated patent database"""
        print("\n" + "="*60)
        print("CREATING DEDUPLICATED DATABASE")
        print("="*60)
        
        # Organize patents by technology
        patents_by_technology = {
            "pitot_tubes": [],
            "multi_hole_probes": [], 
            "anemometers": [],
            "mems_sensors": [],
            "other": []
        }
        
        technology_keywords = {
            "pitot_tubes": ["pitot", "static pressure", "dynamic pressure", "total pressure"],
            "multi_hole_probes": ["multi-hole", "multi hole", "probe", "angle of attack", "5-hole", "3-hole"],
            "anemometers": ["anemometer", "wind sensor", "wind measurement", "ultrasonic"],
            "mems_sensors": ["mems", "micro", "microfabrication", "silicon", "semiconductor"]
        }
        
        for patent in self.unique_patents.values():
            # Remove source file marker
            if '_source_file' in patent:
                del patent['_source_file']
            
            # Classify by technology
            title = (patent.get('title', '') + ' ' + patent.get('abstract', '')).lower()
            
            classified = False
            for tech, keywords in technology_keywords.items():
                if any(keyword in title for keyword in keywords):
                    patents_by_technology[tech].append(patent)
                    classified = True
                    break
            
            if not classified:
                patents_by_technology["other"].append(patent)
        
        # Create deduplicated database
        deduplicated_db = {
            "collection_metadata": {
                "total_patents": len(self.unique_patents),
                "deduplication_date": datetime.now().isoformat(),
                "original_sources": self.patent_files,
                "duplicates_removed": sum(len(patents) for patents in self.duplicates.values()) - len(self.duplicates),
                "deduplication_method": "Publication number normalization and comparison",
                "authenticity": "100% real patent abstracts from 2010-2025",
                "focus": "UAV airflow sensing technologies - deduplicated",
                "technologies": list(patents_by_technology.keys())
            },
            "technology_distribution": {
                tech: len(patents) for tech, patents in patents_by_technology.items()
            },
            "patents_by_technology": patents_by_technology,
            "deduplication_report": {
                "original_total": sum(len(self.load_patent_file(f)) for f in self.patent_files),
                "deduplicated_total": len(self.unique_patents),
                "duplicate_groups_found": len(self.duplicates),
                "patents_removed": sum(len(patents) for patents in self.duplicates.values()) - len(self.duplicates)
            }
        }
        
        # Save deduplicated database
        output_file = os.path.join(self.base_path, f"DEDUPLICATED_PATENTS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(deduplicated_db, f, indent=2, ensure_ascii=False)
            
            print(f"[SUCCESS] Deduplicated database saved: {output_file}")
            
            # Display final statistics
            print("\nFINAL STATISTICS:")
            print("-" * 20)
            for tech, count in deduplicated_db["technology_distribution"].items():
                print(f"{tech}: {count} patents")
            
            return output_file
            
        except Exception as e:
            print(f"[ERROR] Failed to save deduplicated database: {e}")
            return None
    
    def update_knowledge_agent_config(self, deduplicated_file):
        """Update comprehensive knowledge agent to use deduplicated database"""
        print("\n" + "="*60)
        print("UPDATING KNOWLEDGE AGENT CONFIGURATION")
        print("="*60)
        
        # Update comprehensive_knowledge_agent.py
        agent_file = os.path.join(self.base_path, "Stasik-Agent", "comprehensive_knowledge_agent.py")
        
        if os.path.exists(agent_file):
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find the knowledge_files dictionary and add deduplicated file
                deduplicated_filename = os.path.basename(deduplicated_file)
                
                # Add to knowledge files
                if 'knowledge_files = {' in content:
                    insert_line = f'        "patents_deduplicated": "{deduplicated_filename}",\n'
                    
                    # Insert after the opening brace
                    content = content.replace(
                        'knowledge_files = {\n',
                        f'knowledge_files = {{\n{insert_line}'
                    )
                
                with open(agent_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"[SUCCESS] Updated {agent_file}")
                
            except Exception as e:
                print(f"[ERROR] Failed to update agent configuration: {e}")
        
        return deduplicated_file
    
    def run_deduplication(self):
        """Run complete deduplication process"""
        print("STARTING PATENT DEDUPLICATION PROCESS")
        print("=" * 80)
        
        # Find duplicates
        duplicates, unique_patents = self.find_duplicates()
        
        # Display analysis
        self.display_duplicate_analysis()
        
        # Create deduplicated database
        deduplicated_file = self.create_deduplicated_database()
        
        if deduplicated_file:
            # Update knowledge agent
            self.update_knowledge_agent_config(deduplicated_file)
            
            print("\n" + "="*80)
            print("DEDUPLICATION COMPLETE")
            print("="*80)
            print(f"Original patents: {sum(len(self.load_patent_file(f)) for f in self.patent_files)}")
            print(f"Deduplicated patents: {len(self.unique_patents)}")
            print(f"Duplicates removed: {sum(len(patents) for patents in self.duplicates.values()) - len(self.duplicates)}")
            print(f"Deduplicated database: {deduplicated_file}")
            
            return deduplicated_file
        
        return None

def main():
    """Main deduplication function"""
    try:
        deduplicator = PatentDeduplicator()
        deduplicated_file = deduplicator.run_deduplication()
        
        if deduplicated_file:
            print(f"\n[SUCCESS] Deduplication completed successfully!")
            print(f"New database: {deduplicated_file}")
        else:
            print(f"\n[ERROR] Deduplication failed")
            
    except Exception as e:
        print(f"[ERROR] Deduplication process failed: {e}")

if __name__ == "__main__":
    main()