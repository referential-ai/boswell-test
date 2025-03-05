#!/usr/bin/env python3
"""
Unit tests for the Boswell Test framework.

This file contains tests for the core functionality of the Boswell Test framework,
particularly focusing on the Boswell Quotient calculation and aggregation.
"""

import unittest
import json
from typing import Dict, Any
import boswell_test


class TestBoswellQuotient(unittest.TestCase):
    """Test cases for the Boswell Quotient calculation and related functionality."""
    
    def setUp(self):
        """Set up test data for Boswell Quotient tests."""
        # Create sample results for testing with the correct structure
        self.sample_results = {
            "essays": {
                "Model A": "Sample essay for Model A",
                "Model B": "Sample essay for Model B",
                "Model C": "Sample essay for Model C",
            },
            "summary": {
                "Model A": {
                    "median_numeric": 3.7,  # A-
                    "grades_received": ["A", "A-", "B+"]
                },
                "Model B": {
                    "median_numeric": 4.0,  # A
                    "grades_received": ["A+", "A", "A-"]
                },
                "Model C": {
                    "median_numeric": 3.3,  # B+
                    "grades_received": ["A-", "B+", "B"]
                }
            },
            "bias_analysis": {
                "overall_median": 3.7,
                "grader_bias": {
                    "Model A": {
                        "median_given": 3.7,
                        "median_bias": 0.0,  # Neutral
                        "letter_bias": "Neutral"
                    },
                    "Model B": {
                        "median_given": 4.0,
                        "median_bias": 0.3,  # Slightly lenient
                        "letter_bias": "Slightly Lenient (+1/3 grade)"
                    },
                    "Model C": {
                        "median_given": 3.4,
                        "median_bias": -0.3,  # Slightly strict
                        "letter_bias": "Slightly Strict (-1/3 grade)"
                    }
                }
            },
            "timing": {
                "model_timing": {
                    "essay": {
                        "Model A": 15.0,  # 15 seconds for essay generation
                        "Model B": 20.0,  # 20 seconds
                        "Model C": 10.0,  # 10 seconds
                    },
                    "grading": {
                        "Model A": {
                            "Model B": 10.0,
                            "Model C": 12.0,
                        },
                        "Model B": {
                            "Model A": 15.0,
                            "Model C": 18.0,
                        },
                        "Model C": {
                            "Model A": 8.0,
                            "Model B": 9.0,
                        }
                    }
                }
            }
        }
        
        # Create mock models list
        self.models = ["Model A", "Model B", "Model C"]
        
        # Sample domain results for aggregation tests
        self.domain_results = {
            "domain1": {
                "boswell_quotient": {
                    "model_scores": {
                        "Model A": {
                            "boswell_quotient": 85.0,
                            "components": {
                                "performance": 86.0,
                                "evaluation": 100.0,
                                "efficiency": 60.0,
                            },
                            "rank": 2,
                        },
                        "Model B": {
                            "boswell_quotient": 90.0,
                            "components": {
                                "performance": 93.0,
                                "evaluation": 85.0,
                                "efficiency": 90.0,
                            },
                            "rank": 1,
                        },
                        "Model C": {
                            "boswell_quotient": 78.0,
                            "components": {
                                "performance": 77.0,
                                "evaluation": 70.0,
                                "efficiency": 95.0,
                            },
                            "rank": 3,
                        },
                    },
                },
            },
            "domain2": {
                "boswell_quotient": {
                    "model_scores": {
                        "Model A": {
                            "boswell_quotient": 82.0,
                            "components": {
                                "performance": 84.0,
                                "evaluation": 90.0,
                                "efficiency": 65.0,
                            },
                            "rank": 1,
                        },
                        "Model B": {
                            "boswell_quotient": 75.0,
                            "components": {
                                "performance": 80.0,
                                "evaluation": 70.0,
                                "efficiency": 70.0,
                            },
                            "rank": 2,
                        },
                        "Model C": {
                            "boswell_quotient": 65.0,
                            "components": {
                                "performance": 60.0,
                                "evaluation": 60.0,
                                "efficiency": 85.0,
                            },
                            "rank": 3,
                        },
                    },
                },
            },
        }

    def test_boswell_quotient_calculation(self):
        """Test that the Boswell Quotient is calculated correctly for individual models."""
        # Calculate Boswell Quotient for the sample results
        quotient_results = boswell_test.calculate_boswell_quotient(self.sample_results, self.models)
        
        # Check that all models have a Boswell Quotient
        self.assertIn("model_scores", quotient_results)
        for model in self.models:
            self.assertIn(model, quotient_results["model_scores"])
            self.assertIn("boswell_quotient", quotient_results["model_scores"][model])
            
        # Check specific model scores
        model_a_score = quotient_results["model_scores"]["Model A"]["boswell_quotient"]
        model_b_score = quotient_results["model_scores"]["Model B"]["boswell_quotient"]
        model_c_score = quotient_results["model_scores"]["Model C"]["boswell_quotient"]
        
        # Check components are present
        for model in self.models:
            self.assertIn("components", quotient_results["model_scores"][model])
            components = quotient_results["model_scores"][model]["components"]
            self.assertIn("performance", components)
            # Note: Not all components may be present in all tests
            # Only check that key components exist
            self.assertGreaterEqual(len(components), 1)
        
        # Verify that weights are applied correctly
        # Performance, Evaluation, and Efficiency all have equal weighting (33.3% each)
        # Model B should have higher performance (4.0/4.3 = ~93%)
        # Model A should have better evaluation (no bias)
        # Model C should have better efficiency (faster times)
        self.assertGreater(model_b_score, model_c_score)  # B should score higher than C
        
        # Check that component weights are stored
        self.assertIn("component_weights", quotient_results)
        self.assertAlmostEqual(sum(quotient_results["component_weights"].values()), 1.0)  # Weights should sum to 1
        
        # Check that ranks are assigned (1-based)
        ranks = [quotient_results["model_scores"][model]["rank"] for model in self.models]
        self.assertEqual(min(ranks), 1)
        self.assertEqual(max(ranks), len(self.models))
        self.assertEqual(len(set(ranks)), len(self.models))  # All ranks should be unique

    def test_aggregate_boswell_quotient(self):
        """Test the aggregation of Boswell Quotient scores across multiple domains."""
        # Aggregate Boswell Quotient across domains
        aggregated = boswell_test.aggregate_boswell_quotient(self.domain_results)
        
        # Check structure of aggregated results
        self.assertIn("model_scores", aggregated)
        self.assertIn("domains_analyzed", aggregated)
        self.assertEqual(set(aggregated["domains_analyzed"]), set(self.domain_results.keys()))
        
        # Check that all models are included
        for model in ["Model A", "Model B", "Model C"]:
            self.assertIn(model, aggregated["model_scores"])
            model_data = aggregated["model_scores"][model]
            
            # Check required fields
            self.assertIn("average_boswell_quotient", model_data)
            self.assertIn("domain_scores", model_data)
            self.assertIn("domain_components", model_data)
            self.assertIn("rank", model_data)
            
            # Verify domain scores are included
            for domain in self.domain_results:
                self.assertIn(domain, model_data["domain_scores"])
                
            # Check that average is calculated correctly
            domain_scores = list(model_data["domain_scores"].values())
            expected_avg = sum(domain_scores) / len(domain_scores)
            self.assertAlmostEqual(model_data["average_boswell_quotient"], expected_avg)
            
        # Check Model A's consistency (should be higher than Model B)
        model_a = aggregated["model_scores"]["Model A"]
        model_b = aggregated["model_scores"]["Model B"]
        self.assertIn("consistency", model_a)
        self.assertIn("consistency", model_b)
        # Model A has scores of 85 and 82 (diff = 3)
        # Model B has scores of 90 and 75 (diff = 15)
        # Higher consistency means smaller difference
        self.assertGreater(model_a["consistency"], model_b["consistency"])
        
        # Check that best and worst domains are identified
        for model in ["Model A", "Model B", "Model C"]:
            model_data = aggregated["model_scores"][model]
            self.assertIn("best_domain", model_data)
            self.assertIn("worst_domain", model_data)
        
        # Model B should have domain1 as best domain
        self.assertEqual(aggregated["model_scores"]["Model B"]["best_domain"], "domain1")
        # Model C should have domain2 as worst domain
        self.assertEqual(aggregated["model_scores"]["Model C"]["worst_domain"], "domain2")
        
        # Check component aggregation
        for model in ["Model A", "Model B", "Model C"]:
            self.assertIn("aggregated_components", aggregated["model_scores"][model])
            components = aggregated["model_scores"][model]["aggregated_components"]
            # Check performance aggregation for Model A
            if model == "Model A":
                expected_performance = (86.0 + 84.0) / 2
                self.assertAlmostEqual(components["performance"], expected_performance)


class TestGradeConversion(unittest.TestCase):
    """Test cases for grade conversion functions."""
    
    def test_grade_to_percentage(self):
        """Test the conversion of numeric grades to percentages."""
        # Test A+ grade
        self.assertEqual(boswell_test.grade_to_percentage(4.3), 100)
        
        # Test A grade
        self.assertEqual(boswell_test.grade_to_percentage(4.0), 93)
        
        # Test B+ grade
        self.assertEqual(boswell_test.grade_to_percentage(3.3), 87)
        
        # Test C grade 
        self.assertEqual(boswell_test.grade_to_percentage(2.0), 73)
        
        # Test F grade
        self.assertEqual(boswell_test.grade_to_percentage(0.0), 0)
        
        # Test in-between values
        self.assertGreater(boswell_test.grade_to_percentage(3.85), 90)  # Between A and A-
        self.assertLess(boswell_test.grade_to_percentage(3.85), 97)     # Between A and A-
        
    def test_percentage_to_letter_grade(self):
        """Test the conversion of percentages to letter grades."""
        # Test perfect score
        self.assertEqual(boswell_test.percentage_to_letter_grade(100), "A+")
        
        # Test A range
        self.assertEqual(boswell_test.percentage_to_letter_grade(95), "A")
        self.assertEqual(boswell_test.percentage_to_letter_grade(91), "A-")
        
        # Test B range
        self.assertEqual(boswell_test.percentage_to_letter_grade(88), "B+")
        self.assertEqual(boswell_test.percentage_to_letter_grade(85), "B")
        self.assertEqual(boswell_test.percentage_to_letter_grade(81), "B-")
        
        # Test C range
        self.assertEqual(boswell_test.percentage_to_letter_grade(78), "C+")
        self.assertEqual(boswell_test.percentage_to_letter_grade(75), "C")
        self.assertEqual(boswell_test.percentage_to_letter_grade(71), "C-")
        
        # Test D range
        self.assertEqual(boswell_test.percentage_to_letter_grade(68), "D+")
        self.assertEqual(boswell_test.percentage_to_letter_grade(65), "D")
        self.assertEqual(boswell_test.percentage_to_letter_grade(61), "D-")
        
        # Test F range
        self.assertEqual(boswell_test.percentage_to_letter_grade(59), "F")
        self.assertEqual(boswell_test.percentage_to_letter_grade(0), "F")
    
    def test_bidirectional_conversion(self):
        """Test that converting from grade to percentage and back works correctly."""
        grades = [4.3, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]
        expected_letters = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]
        
        for i, grade in enumerate(grades):
            percentage = boswell_test.grade_to_percentage(grade)
            letter = boswell_test.percentage_to_letter_grade(percentage)
            self.assertEqual(letter, expected_letters[i])


class TestReportGeneration(unittest.TestCase):
    """Test cases for report generation functionality."""
    
    def setUp(self):
        """Set up test data for report generation tests."""
        # Sample aggregated data for testing report generation
        self.aggregated_data = {
            "model_scores": {
                "Model A": {
                    "average_boswell_quotient": 83.5,
                    "domain_scores": {"domain1": 85.0, "domain2": 82.0},
                    "domain_components": {
                        "domain1": {"performance": 86.0, "evaluation": 100.0, "efficiency": 60.0},
                        "domain2": {"performance": 84.0, "evaluation": 90.0, "efficiency": 65.0}
                    },
                    "aggregated_components": {
                        "performance": 85.0,
                        "evaluation": 95.0,
                        "efficiency": 62.5
                    },
                    "rank": 1,
                    "consistency": 97.0,
                    "best_domain": "domain1",
                    "worst_domain": "domain2"
                },
                "Model B": {
                    "average_boswell_quotient": 82.5,
                    "domain_scores": {"domain1": 90.0, "domain2": 75.0},
                    "domain_components": {
                        "domain1": {"performance": 93.0, "evaluation": 85.0, "efficiency": 90.0},
                        "domain2": {"performance": 80.0, "evaluation": 70.0, "efficiency": 70.0}
                    },
                    "aggregated_components": {
                        "performance": 86.5,
                        "evaluation": 77.5,
                        "efficiency": 80.0
                    },
                    "rank": 2,
                    "consistency": 85.0,
                    "best_domain": "domain1",
                    "worst_domain": "domain2"
                }
            },
            "domains_analyzed": ["domain1", "domain2"],
            "component_weights": {
                "performance": 0.333,
                "evaluation": 0.333,
                "efficiency": 0.334
            }
        }
        
        # Domain descriptions for report generation
        self.domain_descriptions = {
            "domain1": "Computer Science",
            "domain2": "Political Science"
        }

    def test_aggregate_report_generation(self):
        """Test that the aggregate report is generated correctly."""
        report = boswell_test.generate_aggregate_boswell_report(
            self.aggregated_data, 
            self.domain_descriptions
        )
        
        # Check that the report is generated and is a string
        self.assertIsInstance(report, str)
        self.assertTrue(len(report) > 0)
        
        # Check that key sections are included
        self.assertIn("# Aggregate Boswell Quotient Analysis", report)
        self.assertIn("## Overall Model Rankings", report)
        self.assertIn("## Top Performing Models", report)
        self.assertIn("## Domain-Specific Leaders", report)
        
        # Check that domain names are included
        for domain_name in self.domain_descriptions.values():
            self.assertIn(domain_name, report)
            
        # Check that model names are included
        for model_name in self.aggregated_data["model_scores"]:
            self.assertIn(model_name, report)
    
    def test_boswell_quotient_table_generation(self):
        """Test the generation of Boswell Quotient tables."""
        # Create a sample data structure for the quotient results
        sample_quotient_results = {
            "model_scores": {
                "Model A": {
                    "boswell_quotient": 85.7,
                    "components": {
                        "performance": 88.3,
                        "evaluation": 93.2,
                        "efficiency": 68.9
                    },
                    "rank": 1
                },
                "Model B": {
                    "boswell_quotient": 79.2,
                    "components": {
                        "performance": 80.5,
                        "evaluation": 75.0,
                        "efficiency": 82.1
                    },
                    "rank": 2
                },
                "Model C": {
                    "boswell_quotient": 71.4,
                    "components": {
                        "performance": 72.0,
                        "evaluation": 65.8,
                        "efficiency": 79.0
                    },
                    "rank": 3
                }
            },
            "component_weights": {
                "performance": 0.333,
                "evaluation": 0.333,
                "efficiency": 0.334
            }
        }
        
        # Generate table
        table = boswell_test.generate_boswell_quotient_table(sample_quotient_results)
        
        # Check that the table is generated and is a string
        self.assertIsInstance(table, str)
        self.assertTrue(len(table) > 0)
        
        # Check that table structure is correct
        lines = table.strip().split('\n')
        self.assertEqual(len(lines), 5)  # Header, separator, and 3 data rows
        
        # Check header
        self.assertTrue(lines[0].startswith("| Rank | Model | Boswell Quotient"))
        
        # Check that all models are included
        for model in sample_quotient_results["model_scores"]:
            self.assertIn(model, table)
            
        # Check that ranks and scores are included
        for model, data in sample_quotient_results["model_scores"].items():
            self.assertIn(f"| {data['rank']} | {model} | {data['boswell_quotient']:.1f}", table)
            
        # Check component values - format should match what we specified
        self.assertIn("88.3", table)  # Model A performance
        self.assertIn("75.0", table)  # Model B evaluation
        self.assertIn("79.0", table)  # Model C efficiency


if __name__ == "__main__":
    unittest.main()