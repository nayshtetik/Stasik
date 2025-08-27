#!/usr/bin/env python3
"""
Enhanced Stasik Agent with ArduPilot Knowledge Integration
UAV Airflow Sensing Knowledge Agent + ArduPilot Documentation
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from stasik_agent import StasikAgent

class EnhancedStasikAgent(StasikAgent):
    def __init__(self, ardupilot_kb_path=None):
        """Initialize enhanced Stasik agent with ArduPilot knowledge"""
        super().__init__()
        
        # Load ArduPilot knowledge base
        self.ardupilot_kb_path = Path(ardupilot_kb_path) if ardupilot_kb_path else Path("C:/Knowledge/Patents/ardupilot_knowledge.json")
        self.ardupilot_knowledge = {}
        self.load_ardupilot_knowledge()
        
        # Update agent info
        self.agent_name = "Enhanced Stasik"
        self.version = "2.0"
        self.domain = "UAV Airflow Sensing Technologies + ArduPilot Integration"
        
        # Add ArduPilot-specific capabilities
        self.capabilities.update({
            "ardupilot_integration": True,
            "parameter_guidance": True,
            "ekf_tuning": True,
            "sensor_configuration": True,
            "flight_testing": True,
            "troubleshooting_advanced": True
        })
    
    def load_ardupilot_knowledge(self):
        """Load ArduPilot knowledge base"""
        try:
            if self.ardupilot_kb_path.exists():
                with open(self.ardupilot_kb_path, 'r', encoding='utf-8') as f:
                    self.ardupilot_knowledge = json.load(f)
                print(f"[OK] ArduPilot knowledge base loaded from {self.ardupilot_kb_path}")
                return True
            else:
                print(f"[WARNING] ArduPilot knowledge base not found at {self.ardupilot_kb_path}")
                return False
        except Exception as e:
            print(f"[ERROR] Failed to load ArduPilot knowledge base: {e}")
            return False
    
    def query_ardupilot_integration(self, technology: str, platform: str = "ardupilot") -> Dict[str, Any]:
        """Query ArduPilot-specific integration information"""
        
        if not self.ardupilot_knowledge:
            return {
                "status": "error",
                "message": "ArduPilot knowledge base not available"
            }
        
        # Normalize technology name
        tech_key = self._normalize_technology_name(technology)
        
        response = {
            "status": "success",
            "technology": tech_key,
            "platform": platform,
            "agent": self.agent_name,
            "timestamp": datetime.now().isoformat(),
            "source": "ArduPilot Knowledge Base Integration"
        }
        
        # Get ArduPilot-specific integration data
        if "stasik_ardupilot_mapping" in self.ardupilot_knowledge:
            mapping = self.ardupilot_knowledge["stasik_ardupilot_mapping"]
            
            if tech_key in mapping:
                response["ardupilot_integration"] = mapping[tech_key]
            else:
                response["ardupilot_integration"] = {
                    "status": "Limited support",
                    "note": f"No specific ArduPilot integration found for {tech_key}",
                    "general_approach": "Custom driver development may be required"
                }
        
        # Add parameter information
        if "parameters" in self.ardupilot_knowledge:
            params = self.ardupilot_knowledge["parameters"]
            relevant_params = []
            
            # Include airspeed parameters for most sensors
            if tech_key in ["pitot_tubes", "mems_sensors"]:
                relevant_params.extend(params.get("airspeed_parameters", []))
            
            # Include EKF parameters for all sensors
            relevant_params.extend(params.get("ekf_parameters", []))
            
            response["relevant_parameters"] = relevant_params[:10]  # Limit to 10 most relevant
        
        # Add professional insights
        if "professional_insights" in self.ardupilot_knowledge:
            insights = self.ardupilot_knowledge["professional_insights"]
            response["ardupilot_best_practices"] = insights.get("best_practices", [])
            response["common_issues"] = insights.get("common_issues", [])
        
        return response
    
    def get_parameter_guidance(self, parameter_name: str) -> Dict[str, Any]:
        """Get detailed parameter guidance"""
        
        response = {
            "status": "success",
            "parameter": parameter_name,
            "agent": self.agent_name,
            "timestamp": datetime.now().isoformat(),
            "source": "ArduPilot Parameter Database"
        }
        
        # Parameter-specific guidance
        parameter_guide = {
            "ARSPD_TYPE": {
                "description": "Airspeed sensor type selection",
                "values": {
                    "0": "Disabled",
                    "1": "PX4/Pixhawk airspeed sensor",
                    "2": "3DR airspeed sensor", 
                    "3": "SpeedyBee airspeed sensor",
                    "8": "Analog airspeed sensor",
                    "15": "DLVR airspeed sensor"
                },
                "tuning_notes": "Select based on physical sensor hardware",
                "related_params": ["ARSPD_RATIO", "ARSPD_AUTOCAL"]
            },
            "ARSPD_RATIO": {
                "description": "Airspeed calibration ratio",
                "typical_range": "1.8 to 2.2",
                "tuning_notes": "Adjust based on calibration flight data",
                "calibration_procedure": "Enable ARSPD_AUTOCAL and perform calibration flight",
                "related_params": ["ARSPD_AUTOCAL", "ARSPD_TYPE"]
            },
            "ARSPD_AUTOCAL": {
                "description": "Automatic airspeed calibration",
                "values": {"0": "Disabled", "1": "Enabled"},
                "tuning_notes": "Enable for automatic ratio calibration during flight",
                "related_params": ["ARSPD_RATIO"]
            },
            "EK3_ARSP_THR": {
                "description": "EKF3 airspeed fusion threshold",
                "typical_range": "5.0 to 10.0",
                "tuning_notes": "Lower values increase airspeed influence on EKF",
                "related_params": ["EK3_ENABLE", "EK3_WIND_P_NSE"]
            }
        }
        
        if parameter_name in parameter_guide:
            response["parameter_details"] = parameter_guide[parameter_name]
        else:
            response["parameter_details"] = {
                "description": f"Parameter {parameter_name} found in ArduPilot system",
                "note": "Detailed guidance not available in current knowledge base",
                "recommendation": "Consult ArduPilot documentation for specific details"
            }
        
        return response
    
    def get_ekf_tuning_guidance(self, sensor_type: str = "airspeed") -> Dict[str, Any]:
        """Get EKF tuning guidance for airflow sensors"""
        
        response = {
            "status": "success",
            "sensor_type": sensor_type,
            "agent": self.agent_name,
            "timestamp": datetime.now().isoformat(),
            "source": "ArduPilot EKF Integration Knowledge"
        }
        
        ekf_guidance = {
            "airspeed": {
                "key_parameters": {
                    "EK3_ENABLE": "Enable EKF3 (recommended over EKF2)",
                    "EK3_ARSP_THR": "Airspeed measurement noise threshold",
                    "EK3_WIND_P_NSE": "Wind process noise",
                    "EK3_DRAG_BCOEF_X": "Ballistic coefficient X-axis",
                    "EK3_DRAG_BCOEF_Y": "Ballistic coefficient Y-axis"
                },
                "tuning_sequence": [
                    "Enable EK3_ENABLE = 1",
                    "Set ARSPD_TYPE to match physical sensor",
                    "Enable ARSPD_AUTOCAL = 1",
                    "Perform calibration flight",
                    "Monitor EKF innovations in flight logs",
                    "Adjust EK3_ARSP_THR based on sensor noise",
                    "Tune wind estimation parameters if needed"
                ],
                "validation_checks": [
                    "Compare airspeed vs ground speed correlation",
                    "Check EKF innovation sequences",
                    "Verify wind estimation convergence",
                    "Monitor sensor health indicators"
                ]
            }
        }
        
        if sensor_type in ekf_guidance:
            response["tuning_guidance"] = ekf_guidance[sensor_type]
        
        return response
    
    def analyze_enhanced_system_integration(self, primary_sensor: str, platform: str = "ardupilot", 
                                          requirements: Dict[str, Any] = None) -> Dict[str, Any]:
        """Enhanced system integration analysis with ArduPilot specifics"""
        
        # Get base integration analysis
        base_analysis = super().analyze_system_integration(primary_sensor, platform, requirements)
        
        if base_analysis["status"] != "success":
            return base_analysis
        
        # Enhance with ArduPilot-specific information
        ardupilot_integration = self.query_ardupilot_integration(primary_sensor, platform)
        
        if ardupilot_integration["status"] == "success":
            base_analysis["ardupilot_specifics"] = {
                "integration_details": ardupilot_integration.get("ardupilot_integration", {}),
                "relevant_parameters": ardupilot_integration.get("relevant_parameters", []),
                "best_practices": ardupilot_integration.get("ardupilot_best_practices", []),
                "common_issues": ardupilot_integration.get("common_issues", [])
            }
        
        # Add EKF tuning guidance
        ekf_guidance = self.get_ekf_tuning_guidance("airspeed")
        if ekf_guidance["status"] == "success":
            base_analysis["ekf_tuning"] = ekf_guidance.get("tuning_guidance", {})
        
        base_analysis["enhanced"] = True
        base_analysis["agent"] = self.agent_name
        
        return base_analysis
    
    def _get_troubleshooting_guidance(self, issue_type: str = "general") -> Dict[str, Any]:
        """Get troubleshooting guidance for common airspeed sensor issues"""
        
        response = {
            "status": "success",
            "issue_type": issue_type,
            "agent": self.agent_name,
            "timestamp": datetime.now().isoformat(),
            "source": "Enhanced Troubleshooting Database"
        }
        
        troubleshooting_database = {
            "erratic_readings": {
                "common_causes": [
                    "Airspeed sensor blockage (insects, ice, debris)",
                    "Poor electrical connections or wiring issues",
                    "EKF fusion threshold too sensitive (EK3_ARSP_THR too low)",
                    "Sensor calibration drift or incorrect ARSPD_RATIO",
                    "Temperature compensation issues"
                ],
                "diagnostic_steps": [
                    "Check ARSP message in flight logs for sensor status",
                    "Compare airspeed vs GPS ground speed correlation",
                    "Inspect sensor ports for blockage or damage",
                    "Verify sensor wiring and connections",
                    "Monitor EKF innovation sequences for outliers"
                ],
                "solutions": [
                    "Clean sensor ports and check for blockage",
                    "Recalibrate airspeed sensor (ARSPD_AUTOCAL=1)",
                    "Adjust EKF fusion threshold (EK3_ARSP_THR)",
                    "Replace sensor if hardware fault detected"
                ]
            },
            "sensor_failure": {
                "symptoms": [
                    "No airspeed readings in telemetry",
                    "Constant zero or maximum values",
                    "ArduPilot switches to synthetic airspeed",
                    "EKF navigation warnings"
                ],
                "immediate_actions": [
                    "Enable synthetic airspeed fallback",
                    "Switch to manual flight mode if safe",
                    "Monitor GPS ground speed for reference",
                    "Land as soon as safely possible"
                ],
                "prevention": [
                    "Implement dual airspeed sensor redundancy",
                    "Regular pre-flight sensor health checks",
                    "Periodic calibration validation",
                    "Environmental protection for sensors"
                ]
            },
            "calibration_drift": {
                "causes": [
                    "Temperature cycling effects",
                    "Mechanical stress on sensor housing",
                    "Humidity and environmental exposure",
                    "Sensor aging and component drift"
                ],
                "detection": [
                    "Airspeed vs ground speed correlation analysis",
                    "Cross-validation with multiple flight conditions",
                    "EKF innovation trend analysis",
                    "Historical calibration parameter tracking"
                ],
                "correction": [
                    "Perform new calibration flight",
                    "Update ARSPD_RATIO based on flight data",
                    "Consider temperature compensation",
                    "Replace sensor if drift is excessive"
                ]
            }
        }
        
        if issue_type in troubleshooting_database:
            response["guidance"] = troubleshooting_database[issue_type]
        else:
            response["guidance"] = {
                "note": f"Specific guidance for {issue_type} not found",
                "general_approach": "Consult ArduPilot troubleshooting documentation",
                "available_categories": list(troubleshooting_database.keys())
            }
        
        return response
    
    def get_enhanced_agent_info(self) -> Dict[str, Any]:
        """Get enhanced agent information including ArduPilot capabilities"""
        
        base_info = super().get_agent_info()
        
        # Update with enhanced capabilities
        base_info.update({
            "agent_name": self.agent_name,
            "version": self.version,
            "domain": self.domain,
            "enhancement": "ArduPilot Integration",
            "ardupilot_knowledge_loaded": bool(self.ardupilot_knowledge),
            "additional_capabilities": {
                "ardupilot_parameter_guidance": True,
                "ekf_tuning_assistance": True,
                "sensor_driver_recommendations": True,
                "flight_testing_procedures": True,
                "troubleshooting_diagnostics": True
            }
        })
        
        # Add ArduPilot knowledge base statistics
        if self.ardupilot_knowledge:
            ardupilot_stats = {
                "parameters_covered": len(self.ardupilot_knowledge.get("parameters", {}).get("airspeed_parameters", [])),
                "integration_mappings": len(self.ardupilot_knowledge.get("stasik_ardupilot_mapping", {})),
                "professional_insights": len(self.ardupilot_knowledge.get("professional_insights", {}).get("best_practices", [])),
                "knowledge_base_timestamp": self.ardupilot_knowledge.get("timestamp", "Unknown")
            }
            base_info["ardupilot_knowledge_stats"] = ardupilot_stats
        
        return base_info

def main():
    """Main function for enhanced Stasik agent testing"""
    
    print("=" * 80)
    print("Enhanced Stasik Agent with ArduPilot Integration")
    print("=" * 80)
    print()
    
    # Initialize enhanced agent
    enhanced_stasik = EnhancedStasikAgent()
    
    # Display agent info
    info = enhanced_stasik.get_enhanced_agent_info()
    print(f"Agent: {info['agent_name']} v{info['version']}")
    print(f"Domain: {info['domain']}")
    print(f"ArduPilot Knowledge Loaded: {info['ardupilot_knowledge_loaded']}")
    print()
    
    if info.get('ardupilot_knowledge_stats'):
        stats = info['ardupilot_knowledge_stats']
        print("ArduPilot Knowledge Statistics:")
        print(f"  Parameters Covered: {stats['parameters_covered']}")
        print(f"  Integration Mappings: {stats['integration_mappings']}")
        print(f"  Professional Insights: {stats['professional_insights']}")
        print()
    
    # Test ArduPilot integration query
    print("=" * 60)
    print("Testing ArduPilot Integration Query: Pitot Tubes")
    print("=" * 60)
    
    integration_result = enhanced_stasik.query_ardupilot_integration("pitot_tubes")
    if integration_result['status'] == 'success':
        print(f"Technology: {integration_result['technology']}")
        print(f"Platform: {integration_result['platform']}")
        
        if 'ardupilot_integration' in integration_result:
            ardupilot_info = integration_result['ardupilot_integration']
            print("\nArduPilot Integration Details:")
            if 'key_parameters' in ardupilot_info:
                print("  Key Parameters:")
                for param, desc in list(ardupilot_info['key_parameters'].items())[:3]:
                    print(f"    {param}: {desc}")
        
        if 'ardupilot_best_practices' in integration_result:
            practices = integration_result['ardupilot_best_practices']
            print(f"\n  Best Practices ({len(practices)} total):")
            for practice in practices[:3]:
                print(f"    • {practice}")
    print()
    
    # Test parameter guidance
    print("=" * 60)
    print("Testing Parameter Guidance: ARSPD_TYPE")
    print("=" * 60)
    
    param_result = enhanced_stasik.get_parameter_guidance("ARSPD_TYPE")
    if param_result['status'] == 'success':
        details = param_result['parameter_details']
        print(f"Parameter: {param_result['parameter']}")
        print(f"Description: {details['description']}")
        if 'values' in details:
            print("Values:")
            for value, desc in list(details['values'].items())[:3]:
                print(f"  {value}: {desc}")
    print()
    
    print("=" * 80)
    print("Enhanced Stasik Agent Testing Complete")
    print("Ready for enhanced UAV airflow sensing + ArduPilot guidance!")
    print("=" * 80)

if __name__ == "__main__":
    main()