#!/usr/bin/env python3
"""
Debug Visualizer - Enhanced Tracking Display
Visual representation of the answering algorithm steps
"""

import json
from datetime import datetime
from typing import Dict, List, Any

class AlgorithmVisualizer:
    def __init__(self):
        self.symbols = {
            'step': '[>]',
            'success': '[OK]', 
            'warning': '[!]',
            'error': '[X]',
            'info': '[i]',
            'search': '[?]',
            'database': '[DB]',
            'network': '[NET]',
            'brain': '[AI]',
            'time': '[T]',
            'data': '[#]'
        }
    
    def visualize_algorithm_flow(self, tracking_data: dict, detailed: bool = True):
        """Create visual representation of algorithm flow"""
        
        print("\n" + "="*90)
        print(f"{self.symbols['brain']} STASIK ALGORITHM EXECUTION FLOW")
        print("="*90)
        
        total_time = tracking_data.get('total_time', 0)
        total_steps = tracking_data.get('total_steps', 0)
        
        print(f"{self.symbols['time']} Total Processing Time: {total_time:.3f}s")
        print(f"{self.symbols['step']} Total Steps: {total_steps}")
        print()
        
        # Create timeline visualization
        self._create_timeline(tracking_data['steps'])
        
        if detailed:
            print("\n" + "="*70)
            print(f"{self.symbols['data']} DETAILED STEP ANALYSIS")
            print("="*70)
            
            for step in tracking_data['steps']:
                self._visualize_step_details(step)
    
    def _create_timeline(self, steps: List[dict]):
        """Create timeline visualization"""
        
        print(f"{self.symbols['info']} PROCESSING TIMELINE:")
        print("-" * 50)
        
        for i, step in enumerate(steps):
            step_name = step['step_name']
            elapsed = step['elapsed_time']
            step_num = step['step_number']
            
            # Create progress bar
            bar_length = 30
            progress = min(elapsed / (steps[-1]['elapsed_time'] if steps else 1), 1.0)
            filled = int(bar_length * progress)
            bar = "=" * filled + "-" * (bar_length - filled)
            
            # Step indicator
            indicator = self._get_step_indicator(step_name)
            
            print(f"{indicator} Step {step_num:2d}: {step_name:<25} [{bar}] {elapsed:.3f}s")
        
        print()
    
    def _get_step_indicator(self, step_name: str) -> str:
        """Get appropriate indicator for step"""
        
        indicators = {
            'QUERY_RECEIVED': self.symbols['step'],
            'TECHNOLOGY_CLASSIFICATION': self.symbols['brain'],
            'INTENT_CLASSIFICATION': self.symbols['brain'],
            'SEARCH_STRATEGY': self.symbols['search'],
            'COMPREHENSIVE_ANALYSIS': self.symbols['database'],
            'RESPONSE_GENERATION': self.symbols['success']
        }
        
        return indicators.get(step_name, self.symbols['info'])
    
    def _visualize_step_details(self, step: dict):
        """Visualize detailed step information"""
        
        step_name = step['step_name']
        data = step['data']
        elapsed = step['elapsed_time']
        
        print(f"\n{self.symbols['step']} {step_name}")
        print(f"   {self.symbols['time']} Time: {elapsed:.3f}s")
        
        if step_name == "QUERY_RECEIVED":
            query = data.get('user_query', '')
            print(f"   {self.symbols['info']} Query: \"{query[:60]}{'...' if len(query) > 60 else ''}\"")
        
        elif step_name == "TECHNOLOGY_CLASSIFICATION":
            technology = data.get('selected_technology', 'Multi-domain')
            confidence = data.get('confidence', 0)
            scores = data.get('technology_scores', {})
            
            print(f"   {self.symbols['brain']} Technology: {technology}")
            print(f"   {self.symbols['data']} Confidence: {confidence}")
            
            if scores:
                print(f"   {self.symbols['search']} Keyword Scores:")
                for tech, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                    if score > 0:
                        bar = "=" * min(score, 10) + "-" * (10 - min(score, 10))
                        print(f"     • {tech}: [{bar}] {score}")
        
        elif step_name == "INTENT_CLASSIFICATION":
            intent = data.get('selected_intent', 'general')
            scores = data.get('intent_scores', {})
            
            print(f"   {self.symbols['brain']} Intent: {intent}")
            
            if scores:
                print(f"   {self.symbols['search']} Intent Scores:")
                for intent_type, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                    bar = "=" * min(score, 5) + "-" * (5 - min(score, 5))
                    print(f"     • {intent_type}: [{bar}] {score}")
        
        elif step_name == "SEARCH_STRATEGY":
            strategy = data.get('strategy', {})
            print(f"   {self.symbols['search']} Strategy:")
            for key, value in strategy.items():
                status = self.symbols['success'] if value else self.symbols['warning']
                print(f"     {status} {key}: {value}")
        
        elif step_name == "COMPREHENSIVE_ANALYSIS":
            patents = data.get('patents_analyzed', 0)
            papers = data.get('papers_analyzed', 0)
            confidence = data.get('confidence', 0)
            static_coverage = data.get('static_coverage', 0)
            dynamic_coverage = data.get('dynamic_coverage', 0)
            
            print(f"   {self.symbols['database']} Knowledge Base Analysis:")
            print(f"     • Patents analyzed: {patents}")
            print(f"     • Papers analyzed: {papers}")
            print(f"     • Static coverage: {static_coverage} sources")
            print(f"     • Dynamic coverage: {dynamic_coverage} searches")
            print(f"     • Overall confidence: {confidence:.2f}")
        
        elif step_name == "RESPONSE_GENERATION":
            sources = data.get('content_sources', [])
            complexity = data.get('response_complexity', 'unknown')
            total_items = data.get('total_items', 0)
            
            print(f"   {self.symbols['success']} Response Generation:")
            print(f"     • Content sources: {', '.join(sources)}")
            print(f"     • Response complexity: {complexity}")
            print(f"     • Total content items: {total_items}")

class DebugQueryLogger:
    def __init__(self, log_file="debug_queries.json"):
        self.log_file = log_file
        self.session_logs = []
    
    def log_query_session(self, query: str, result: dict, tracking: dict):
        """Log complete query session"""
        
        session_log = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "processing_time": tracking.get('total_time', 0),
            "steps_count": tracking.get('total_steps', 0),
            "result_summary": {
                "status": result.get('status', 'unknown'),
                "confidence": result.get('synthesis', {}).get('confidence', 0),
                "patents_found": 0,
                "papers_found": 0,
                "sources_accessed": len(result.get('static_results', {}))
            },
            "algorithm_steps": tracking.get('steps', []),
            "performance_metrics": self._extract_performance_metrics(result, tracking)
        }
        
        # Count patents and papers
        for static_result in result.get('static_results', {}).values():
            if 'patent_analysis' in static_result:
                session_log["result_summary"]["patents_found"] += static_result['patent_analysis'].get('total_patents_found', 0)
            if 'scientific_research' in static_result:
                session_log["result_summary"]["papers_found"] += static_result['scientific_research'].get('total_papers_found', 0)
        
        self.session_logs.append(session_log)
        
        # Save to file
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save debug log: {e}")
    
    def _extract_performance_metrics(self, result: dict, tracking: dict) -> dict:
        """Extract performance metrics"""
        
        steps = tracking.get('steps', [])
        
        metrics = {
            "total_time": tracking.get('total_time', 0),
            "step_times": {},
            "knowledge_base_efficiency": 0,
            "search_effectiveness": 0
        }
        
        # Extract step timing
        for step in steps:
            step_name = step['step_name']
            step_time = step['elapsed_time']
            
            if len(steps) > 1:
                prev_time = steps[steps.index(step) - 1]['elapsed_time'] if steps.index(step) > 0 else 0
                step_duration = step_time - prev_time
                metrics["step_times"][step_name] = step_duration
        
        # Calculate efficiency metrics
        total_content = 0
        for static_result in result.get('static_results', {}).values():
            if 'patent_analysis' in static_result:
                total_content += static_result['patent_analysis'].get('total_patents_found', 0)
            if 'scientific_research' in static_result:
                total_content += static_result['scientific_research'].get('total_papers_found', 0)
        
        if metrics["total_time"] > 0:
            metrics["knowledge_base_efficiency"] = total_content / metrics["total_time"]
        
        metrics["search_effectiveness"] = min(total_content / 10, 1.0)  # Normalized to 0-1
        
        return metrics
    
    def get_session_statistics(self) -> dict:
        """Get session statistics"""
        
        if not self.session_logs:
            return {"message": "No queries logged yet"}
        
        total_queries = len(self.session_logs)
        avg_time = sum(log["processing_time"] for log in self.session_logs) / total_queries
        avg_confidence = sum(log["result_summary"]["confidence"] for log in self.session_logs) / total_queries
        
        total_patents = sum(log["result_summary"]["patents_found"] for log in self.session_logs)
        total_papers = sum(log["result_summary"]["papers_found"] for log in self.session_logs)
        
        return {
            "total_queries": total_queries,
            "average_processing_time": avg_time,
            "average_confidence": avg_confidence,
            "total_patents_analyzed": total_patents,
            "total_papers_analyzed": total_papers,
            "most_recent_query": self.session_logs[-1]["query"]
        }

def main():
    """Demo visualization functions"""
    
    # Example tracking data for demonstration
    example_tracking = {
        "total_steps": 6,
        "total_time": 2.456,
        "steps": [
            {
                "step_number": 1,
                "step_name": "QUERY_RECEIVED",
                "elapsed_time": 0.001,
                "data": {"user_query": "How do MEMS sensors work in UAV applications?"}
            },
            {
                "step_number": 2,
                "step_name": "TECHNOLOGY_CLASSIFICATION",
                "elapsed_time": 0.045,
                "data": {
                    "selected_technology": "mems_sensors",
                    "confidence": 3,
                    "technology_scores": {"mems_sensors": 3, "pitot_tubes": 0, "anemometers": 0}
                }
            },
            {
                "step_number": 3,
                "step_name": "INTENT_CLASSIFICATION",
                "elapsed_time": 0.078,
                "data": {
                    "selected_intent": "how_to",
                    "intent_scores": {"how_to": 2, "general": 0}
                }
            },
            {
                "step_number": 4,
                "step_name": "SEARCH_STRATEGY",
                "elapsed_time": 0.095,
                "data": {
                    "strategy": {
                        "static_search": True,
                        "dynamic_search": True,
                        "technology_focused": True
                    }
                }
            },
            {
                "step_number": 5,
                "step_name": "COMPREHENSIVE_ANALYSIS",
                "elapsed_time": 2.234,
                "data": {
                    "patents_analyzed": 12,
                    "papers_analyzed": 8,
                    "confidence": 0.75,
                    "static_coverage": 2,
                    "dynamic_coverage": 1
                }
            },
            {
                "step_number": 6,
                "step_name": "RESPONSE_GENERATION",
                "elapsed_time": 2.456,
                "data": {
                    "content_sources": ["patents", "papers", "professional"],
                    "response_complexity": "medium",
                    "total_items": 8
                }
            }
        ]
    }
    
    visualizer = AlgorithmVisualizer()
    visualizer.visualize_algorithm_flow(example_tracking, detailed=True)

if __name__ == "__main__":
    main()