#!/usr/bin/env python3
"""
Test suite for Stasik UAV Airflow Sensing Knowledge Agent
"""

import unittest
import json
import tempfile
import os
from unittest.mock import patch, mock_open
from stasik_agent import StasikAgent

class TestStasikAgent(unittest.TestCase):
    """Test cases for Stasik Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = StasikAgent()
        
        # Mock knowledge base data
        self.mock_knowledge_base = {
            "knowledge_base": {
                "entities": {
                    "patent_001": {"type": "patent", "technology": "pitot_tubes"},
                    "paper_001": {"type": "paper", "technology": "mems_sensors"}
                },
                "concepts": {
                    "pitot_tube": {"type": "sensor", "category": "pressure_based"},
                    "mems_sensor": {"type": "sensor", "category": "miniaturized"}
                }
            },
            "ontology": {
                "technologies": ["pitot_tubes", "multi_hole_probes", "anemometers", "mems_sensors"]
            },
            "semantic_mappings": {
                "synonyms": {
                    "UAV": ["drone", "unmanned_aerial_vehicle"]
                }
            },
            "case_patterns": {
                "technology_evolution": {"pitot_tubes": "mature", "mems_sensors": "emerging"}
            }
        }
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.agent_name, "Stasik")
        self.assertEqual(self.agent.version, "1.0")
        self.assertEqual(self.agent.domain, "UAV Airflow Sensing Technologies")
        self.assertIn("pitot_tubes", self.agent.technologies)
        self.assertIn("mems_sensors", self.agent.technologies)
    
    def test_agent_info(self):
        """Test get_agent_info method"""
        info = self.agent.get_agent_info()
        
        self.assertEqual(info["agent_name"], "Stasik")
        self.assertEqual(info["version"], "1.0")
        self.assertEqual(info["domain"], "UAV Airflow Sensing Technologies")
        self.assertIn("capabilities", info)
        self.assertIn("supported_technologies", info)
        self.assertIn("knowledge_sources", info)
        self.assertEqual(info["status"], "Production Ready")
    
    def test_technology_query_success(self):
        """Test successful technology query"""
        result = self.agent.query_technology("pitot tubes", "overview")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["technology"], "pitot_tubes")
        self.assertEqual(result["query_type"], "overview")
        self.assertEqual(result["agent"], "Stasik")
        self.assertIn("overview", result)
    
    def test_technology_query_invalid(self):
        """Test invalid technology query"""
        result = self.agent.query_technology("invalid_sensor", "overview")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("not in Stasik's knowledge base", result["message"])
        self.assertIn("available_technologies", result)
    
    def test_normalize_technology_name(self):
        """Test technology name normalization"""
        self.assertEqual(self.agent._normalize_technology_name("pitot"), "pitot_tubes")
        self.assertEqual(self.agent._normalize_technology_name("Pitot Tube"), "pitot_tubes")
        self.assertEqual(self.agent._normalize_technology_name("multi-hole"), "multi_hole_probes")
        self.assertEqual(self.agent._normalize_technology_name("MEMS"), "mems_sensors")
        self.assertEqual(self.agent._normalize_technology_name("anemometer"), "anemometers")
    
    def test_technology_overview(self):
        """Test technology overview generation"""
        overview = self.agent._get_technology_overview("pitot_tubes")
        
        self.assertIn("description", overview)
        self.assertIn("principle", overview)
        self.assertIn("advantages", overview)
        self.assertIn("applications", overview)
        self.assertIn("patent_activity", overview)
        self.assertIn("professional_status", overview)
    
    def test_technology_applications(self):
        """Test technology applications query"""
        applications = self.agent._get_technology_applications("pitot_tubes")
        
        self.assertIsInstance(applications, list)
        self.assertGreater(len(applications), 0)
        
        for app in applications:
            self.assertIn("application", app)
            self.assertIn("suitability", app)
            self.assertIn("notes", app)
    
    def test_integration_guidance(self):
        """Test integration guidance generation"""
        guidance = self.agent._get_integration_guidance("pitot_tubes")
        
        self.assertIn("hardware", guidance)
        self.assertIn("software", guidance)
        self.assertIn("installation", guidance)
        self.assertIn("calibration", guidance)
        self.assertIn("maintenance", guidance)
    
    def test_system_integration_analysis(self):
        """Test system integration analysis"""
        result = self.agent.analyze_system_integration(
            primary_sensor="pitot_tube",
            platform="ardupilot",
            requirements={"accuracy": "high"}
        )
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["agent"], "Stasik")
        self.assertEqual(result["analysis_type"], "system_integration")
        self.assertEqual(result["primary_sensor"], "pitot_tube")
        self.assertEqual(result["platform"], "ardupilot")
        self.assertIn("sensor_integration", result)
        self.assertIn("platform_guidance", result)
        self.assertIn("professional_insights", result)
        self.assertIn("challenges_solutions", result)
    
    def test_professional_guidance_calibration(self):
        """Test professional guidance for calibration"""
        result = self.agent.get_professional_guidance("calibration", "ardupilot")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["agent"], "Stasik")
        self.assertEqual(result["topic"], "calibration")
        self.assertEqual(result["context"], "ardupilot")
        self.assertIn("calibration_guidance", result)
    
    def test_professional_guidance_troubleshooting(self):
        """Test professional guidance for troubleshooting"""
        result = self.agent.get_professional_guidance("troubleshooting", "general")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("troubleshooting", result)
    
    def test_professional_guidance_autopilot(self):
        """Test professional guidance for autopilot integration"""
        result = self.agent.get_professional_guidance("ardupilot integration", "px4")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("autopilot_integration", result)
    
    def test_professional_guidance_mems(self):
        """Test professional guidance for MEMS sensors"""
        result = self.agent.get_professional_guidance("mems calibration", "general")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("mems_insights", result)
    
    def test_calibration_guidance(self):
        """Test specific calibration guidance"""
        guidance = self.agent._get_calibration_guidance()
        
        self.assertIn("pitot_tube_calibration", guidance)
        self.assertIn("general_best_practices", guidance)
        self.assertIn("professional_insights", guidance)
        
        pitot_cal = guidance["pitot_tube_calibration"]
        self.assertIn("startup_procedure", pitot_cal)
        self.assertIn("environmental_factors", pitot_cal)
        self.assertIn("parameters", pitot_cal)
        self.assertIn("validation", pitot_cal)
    
    def test_professional_insights(self):
        """Test professional insights generation"""
        insights = self.agent._get_professional_insights("pitot_tube", "ardupilot")
        
        self.assertIn("common_challenges", insights)
        self.assertIn("best_practices", insights)
        self.assertIn("community_recommendations", insights)
        
        self.assertIsInstance(insights["common_challenges"], list)
        self.assertIsInstance(insights["best_practices"], list)
        self.assertIsInstance(insights["community_recommendations"], list)
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_knowledge_base_success(self, mock_exists, mock_file):
        """Test successful knowledge base loading"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = json.dumps(self.mock_knowledge_base)
        
        agent = StasikAgent()
        result = agent.load_knowledge_base("test_knowledge.json")
        
        self.assertTrue(result)
        self.assertIn("entities", agent.knowledge_base)
        self.assertIn("concepts", agent.knowledge_base)
    
    @patch("pathlib.Path.exists")
    def test_load_knowledge_base_file_not_found(self, mock_exists):
        """Test knowledge base loading with missing file"""
        mock_exists.return_value = False
        
        agent = StasikAgent()
        result = agent.load_knowledge_base("nonexistent.json")
        
        self.assertFalse(result)
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_load_knowledge_base_invalid_json(self, mock_exists, mock_file):
        """Test knowledge base loading with invalid JSON"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = "invalid json"
        
        agent = StasikAgent()
        result = agent.load_knowledge_base("invalid.json")
        
        self.assertFalse(result)

class TestStasikAgentIntegration(unittest.TestCase):
    """Integration tests for Stasik Agent"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.agent = StasikAgent()
    
    def test_all_technologies_supported(self):
        """Test that all core technologies are supported"""
        core_technologies = ["pitot_tubes", "multi_hole_probes", "anemometers", "mems_sensors"]
        
        for tech in core_technologies:
            result = self.agent.query_technology(tech, "overview")
            self.assertEqual(result["status"], "success", f"Technology {tech} not supported")
    
    def test_query_type_coverage(self):
        """Test that all query types work for each technology"""
        query_types = ["overview", "applications", "integration", "comparison"]
        
        for query_type in query_types:
            result = self.agent.query_technology("pitot_tubes", query_type)
            self.assertEqual(result["status"], "success", f"Query type {query_type} failed")
    
    def test_professional_guidance_topics(self):
        """Test that all professional guidance topics work"""
        topics = ["calibration", "troubleshooting", "ardupilot integration", "mems setup"]
        
        for topic in topics:
            result = self.agent.get_professional_guidance(topic)
            self.assertEqual(result["status"], "success", f"Guidance topic {topic} failed")
    
    def test_integration_analysis_platforms(self):
        """Test integration analysis for different platforms"""
        platforms = ["ardupilot", "px4", "custom"]
        
        for platform in platforms:
            result = self.agent.analyze_system_integration("pitot_tube", platform)
            self.assertEqual(result["status"], "success", f"Platform {platform} analysis failed")

class TestStasikAgentPerformance(unittest.TestCase):
    """Performance tests for Stasik Agent"""
    
    def setUp(self):
        """Set up performance test fixtures"""
        self.agent = StasikAgent()
    
    def test_query_response_time(self):
        """Test that queries respond within reasonable time"""
        import time
        
        start_time = time.time()
        result = self.agent.query_technology("pitot_tubes", "overview")
        end_time = time.time()
        
        self.assertEqual(result["status"], "success")
        self.assertLess(end_time - start_time, 1.0, "Query took too long")
    
    def test_multiple_queries_performance(self):
        """Test performance with multiple consecutive queries"""
        import time
        
        queries = [
            ("pitot_tubes", "overview"),
            ("mems_sensors", "applications"),
            ("anemometers", "integration"),
            ("multi_hole_probes", "comparison")
        ]
        
        start_time = time.time()
        for tech, query_type in queries:
            result = self.agent.query_technology(tech, query_type)
            self.assertEqual(result["status"], "success")
        end_time = time.time()
        
        avg_time = (end_time - start_time) / len(queries)
        self.assertLess(avg_time, 0.5, "Average query time too high")

if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestStasikAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestStasikAgentIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestStasikAgentPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Stasik Agent Test Suite Results")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split(chr(10))[-2]}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split(chr(10))[-2]}")
    
    print(f"{'='*60}")