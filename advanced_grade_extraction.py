#!/usr/bin/env python3
"""
Advanced Grade Extraction System

This module implements sophisticated techniques for grade extraction:
1. Multi-pass strategy for ambiguous cases
2. Contextual analysis for conclusion sections
3. Semantic grade detection
4. Fallback mechanisms

These techniques go beyond simple pattern matching to understand the
intent and context of grading feedback.
"""

import os
import re
from typing import Dict, Any, List, Tuple, Optional
from collections import Counter
import json

# Import NLTK safely with fallbacks
try:
    import nltk
    # Download required NLTK resources if not already available
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        print("Downloading NLTK POS tagger...")
        nltk.download('averaged_perceptron_tagger', quiet=True)
        
    NLTK_AVAILABLE = True
except ImportError:
    print("NLTK not available. Using simplified tokenization.")
    NLTK_AVAILABLE = False


class AdvancedGradeExtractor:
    """Advanced grade extraction system with multiple strategies."""
    
    def __init__(self):
        """Initialize the grade extractor with necessary patterns and models."""
        # Basic patterns (from original implementation)
        self.basic_patterns = [
            r"Grade:\s*([A-C][+-]?)",
            r"([A-C][+-]?)\s*grade",
            r"grade\s*(?:of|is|:)?\s*([A-C][+-]?)",
            r"grade\s*[\"']([A-C][+-]?)[\"']",
            r"([A-C][+-]?)$",
            r"final\s*grade\s*[:\-=]\s*([A-C][+-]?)",
            r"grade\s*for\s*this\s*essay\s*[:\-=]\s*([A-C][+-]?)",
            r"([A-C][+-]?)\s*grade\s*for\s*this\s*essay",
            r"assign\s*a\s*grade\s*of\s*([A-C][+-]?)",
            r"assign\s*([A-C][+-]?)",
            r"grade\s*assignment\s*[:\-=]\s*([A-C][+-]?)",
            r"overall\s*grade\s*[:\-=]\s*([A-C][+-]?)"
        ]
        
        # Enhanced patterns (from our improved version)
        self.enhanced_patterns = [
            r"Grade\s*([A-C][+-]?)\s*$",
            r"([A-C][+-]?)\s*grade\s*$",
            r"grade[^A-Za-z0-9]*([A-C][+-]?)[^A-Za-z0-9]*$",
            r"grade[^:]*?([A-C][+-]?)",
            r"^\s*([A-C][+-]?)\s*$",
            r"evaluation.*?([A-C][+-]?)",
            r"assessment.*?([A-C][+-]?)",
            r"([A-C][+-]?)\s*(?:overall|rating|score)"
        ]
        
        # Context-aware patterns for specific sections
        self.conclusion_patterns = [
            r"(?:in\s*conclusion|to\s*conclude|overall|summary|finally).*?([A-C][+-]?)",
            r"([A-C][+-]?)\s*(?:is\s*appropriate|would\s*be\s*fair|seems\s*fair|is\s*a\s*fair\s*assessment)",
            r"(?:deserve|earned|warrants|merits).*?([A-C][+-]?)",
            r"(?:final|overall|appropriate)\s*grade\s*(?:is|would\s*be).*?([A-C][+-]?)"
        ]
        
        # Load grade descriptors for semantic matching
        self.grade_descriptors = {
            "A+": ["exceptional", "outstanding", "excellent", "superb", "flawless", "perfect"],
            "A": ["excellent", "superior", "exceptional", "outstanding", "remarkable"],
            "A-": ["very good", "strong", "impressive", "solid", "thorough"],
            "B+": ["good", "above average", "commendable", "solid", "effective"],
            "B": ["good", "competent", "satisfactory", "acceptable", "adequate"],
            "B-": ["satisfactory", "acceptable", "adequate", "sufficient", "passable"],
            "C+": ["fair", "average", "passable", "moderate", "mediocre"],
            "C": ["average", "passable", "fair", "mediocre", "basic"],
            "C-": ["below average", "minimal", "basic", "weak", "limited"]
        }
        
        # Confidence thresholds
        self.high_confidence = 0.8
        self.medium_confidence = 0.5
        self.low_confidence = 0.3
        
        # Track extraction method for analysis
        self.extraction_method = None

    def extract_grade(self, feedback: str, model_name: str = "Unknown") -> Tuple[str, float, str]:
        """
        Extract a grade from feedback using multiple strategies.
        
        Returns:
            Tuple of (grade, confidence, method)
            grade: The extracted letter grade or "N/A"
            confidence: Confidence level from 0.0 to 1.0
            method: Which extraction method was used
        """
        # Initialize tracking
        self.extraction_method = None
        
        # Strategy 1: Pattern-based extraction (high confidence)
        grade, confidence = self.pattern_based_extraction(feedback)
        if grade != "N/A" and confidence >= self.high_confidence:
            return grade, confidence, self.extraction_method
        
        # Strategy 2: Contextual analysis
        grade, confidence = self.contextual_analysis(feedback)
        if grade != "N/A" and confidence >= self.medium_confidence:
            return grade, confidence, self.extraction_method
            
        # Strategy 3: Multi-pass strategy for "Grade:" with missing letter
        grade, confidence = self.handle_missing_grade_after_keyword(feedback)
        if grade != "N/A" and confidence >= self.medium_confidence:
            return grade, confidence, self.extraction_method
            
        # Strategy 4: Semantic grade detection
        grade, confidence = self.semantic_grade_detection(feedback)
        if grade != "N/A" and confidence >= self.low_confidence:
            return grade, confidence, self.extraction_method
            
        # If we get here, return the best result we found (if any)
        if grade != "N/A":
            return grade, confidence, self.extraction_method
            
        # Last resort: See if there's any letter grade anywhere in the text
        grade, confidence = self.last_resort_extraction(feedback)
        if grade != "N/A":
            return grade, confidence, self.extraction_method
            
        # No grade found with any method
        print(f"  Warning: Could not extract grade from feedback for {model_name}. Using N/A.")
        return "N/A", 0.0, "no_grade_found"

    def pattern_based_extraction(self, feedback: str) -> Tuple[str, float]:
        """Extract grade using pattern matching."""
        # Try basic patterns first (exact format has highest confidence)
        for pattern in self.basic_patterns:
            for line in feedback.split('\n'):
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    self.extraction_method = "basic_pattern"
                    return match.group(1).upper(), 1.0
        
        # Try enhanced patterns next (slightly lower confidence)
        for pattern in self.enhanced_patterns:
            for line in feedback.split('\n'):
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    self.extraction_method = "enhanced_pattern"
                    return match.group(1).upper(), 0.9
                    
        return "N/A", 0.0

    def contextual_analysis(self, feedback: str) -> Tuple[str, float]:
        """
        Analyze the context of the feedback to extract grades.
        Particularly focused on conclusion sections.
        """
        # Split into sentences
        if NLTK_AVAILABLE:
            try:
                sentences = nltk.sent_tokenize(feedback)
            except Exception as e:
                print(f"NLTK tokenization error: {e}. Falling back to simple splitting.")
                sentences = re.split(r'[.!?]+\s+', feedback)
        else:
            sentences = re.split(r'[.!?]+\s+', feedback)
        
        # Check the last few sentences (conclusions often appear at the end)
        conclusion_sentences = sentences[-5:] if len(sentences) > 5 else sentences
        conclusion_text = ' '.join(conclusion_sentences)
        
        # Look for conclusion patterns
        for pattern in self.conclusion_patterns:
            match = re.search(pattern, conclusion_text, re.IGNORECASE)
            if match:
                self.extraction_method = "contextual_conclusion"
                return match.group(1).upper(), 0.85
        
        # If no match in conclusion patterns, check if there's a standalone grade
        # in the conclusion sentences
        for sentence in conclusion_sentences:
            # This checks for isolated grade patterns like "A", "B+", etc.
            match = re.search(r'\b([A-C][+-]?)\b', sentence)
            if match:
                self.extraction_method = "contextual_standalone"
                return match.group(1).upper(), 0.7
                
        return "N/A", 0.0

    def handle_missing_grade_after_keyword(self, feedback: str) -> Tuple[str, float]:
        """
        Special handling for cases where "Grade:" appears but no grade follows.
        This is the multi-pass strategy.
        """
        # Check if "Grade:" appears in the text
        if "Grade:" not in feedback and "grade:" not in feedback:
            return "N/A", 0.0
            
        # Find the position of the Grade: keyword
        pos = max(feedback.lower().rfind("grade:"), feedback.lower().rfind("grade :"))
        if pos == -1:
            return "N/A", 0.0
            
        # Get the text after the Grade: keyword (up to 100 chars should be enough)
        after_grade = feedback[pos:pos+100]
        
        # First check for direct grade mention
        match = re.search(r'[Gg]rade:.*?([A-C][+-]?)', after_grade)
        if match:
            self.extraction_method = "multi_pass_direct"
            return match.group(1).upper(), 0.8
            
        # Then check for descriptive language
        # If the description contains multiple grade indicators, take the most common
        potential_grades = []
        for grade, descriptors in self.grade_descriptors.items():
            for descriptor in descriptors:
                if descriptor in after_grade.lower():
                    potential_grades.append(grade)
        
        if potential_grades:
            # Count occurrences
            grade_counts = Counter(potential_grades)
            most_common = grade_counts.most_common(1)[0][0]
            self.extraction_method = "multi_pass_descriptive"
            return most_common, 0.65
            
        # If still not found, check for any letter grade in text after "Grade:"
        match = re.search(r'\b([A-C][+-]?)\b', after_grade)
        if match:
            self.extraction_method = "multi_pass_proximity"
            return match.group(1).upper(), 0.6
            
        return "N/A", 0.0

    def semantic_grade_detection(self, feedback: str) -> Tuple[str, float]:
        """
        Detect grades based on semantic analysis of the feedback.
        Looks for descriptive language associated with different grades.
        """
        feedback_lower = feedback.lower()
        
        # Count grade descriptor occurrences
        grade_scores = {grade: 0 for grade in self.grade_descriptors}
        
        for grade, descriptors in self.grade_descriptors.items():
            for descriptor in descriptors:
                count = feedback_lower.count(descriptor)
                grade_scores[grade] += count
        
        # Find the grade with the highest descriptor count
        max_score = max(grade_scores.values())
        if max_score > 0:
            # Get all grades with the max score
            best_grades = [grade for grade, score in grade_scores.items() if score == max_score]
            best_grade = best_grades[0]  # Default to first if multiple
            
            # Adjust confidence based on how distinctive the signal is
            confidence = min(0.5 + (max_score / 10), 0.8)
            
            self.extraction_method = "semantic_descriptors"
            return best_grade, confidence
            
        return "N/A", 0.0

    def last_resort_extraction(self, feedback: str) -> Tuple[str, float]:
        """
        Last resort extraction when all other methods fail.
        Very low confidence but better than nothing.
        """
        # Look for any isolated letter grade pattern anywhere in the text
        matches = re.findall(r'\b([A-C][+-]?)\b', feedback)
        if matches:
            # If multiple matches, take the most frequent
            if len(matches) > 1:
                grade_counts = Counter(matches)
                most_common = grade_counts.most_common(1)[0][0]
                self.extraction_method = "last_resort_frequency"
                return most_common.upper(), 0.4
            else:
                self.extraction_method = "last_resort_single"
                return matches[0].upper(), 0.3
                
        return "N/A", 0.0
        

def analyze_failed_extractions(logs_dir="logs/grade_extraction"):
    """
    Apply the advanced grade extractor to failed extraction logs.
    
    Returns:
        Analysis of results with different extraction methods
    """
    print(f"Analyzing logs in: {logs_dir}")
    extractor = AdvancedGradeExtractor()
    
    results = []
    
    if not os.path.exists(logs_dir):
        print(f"Error: Directory {logs_dir} does not exist")
        return results
        
    log_files = [f for f in os.listdir(logs_dir) if f.endswith("_failed_extraction.txt")]
    
    if not log_files:
        print(f"No log files found in {logs_dir}")
        return results
        
    print(f"Found {len(log_files)} log files")
    
    for filename in log_files:
        filepath = os.path.join(logs_dir, filename)
        
        # Extract model name from filename
        model_match = re.search(r'(\d+)_(.+)_failed_extraction\.txt', filename)
        if not model_match:
            print(f"Skipping {filename} - doesn't match expected format")
            continue
            
        model_name = model_match.group(2)
        print(f"Processing: {model_name}")
        
        with open(filepath, 'r') as f:
            try:
                content = f.read()
                
                # Skip header lines to get to the actual feedback
                feedback_start = content.find("Feedback content:")
                if feedback_start >= 0:
                    feedback = content[feedback_start + len("Feedback content:"):]
                    
                    # Apply advanced extraction
                    grade, confidence, method = extractor.extract_grade(feedback, model_name)
                    
                    results.append({
                        "model": model_name,
                        "original_grade": "N/A",
                        "advanced_grade": grade,
                        "confidence": confidence,
                        "method": method,
                        "improvement": grade != "N/A"
                    })
                    
                    print(f"  Result: {grade} (confidence: {confidence:.2f}, method: {method})")
                else:
                    print(f"  Feedback content not found in {filename}")
            except Exception as e:
                print(f"  Error processing {filename}: {e}")
    
    return results


def run_advanced_analysis():
    """Run the advanced grade extraction analysis."""
    print("=" * 70)
    print("ADVANCED GRADE EXTRACTION ANALYSIS")
    print("=" * 70)
    
    results = analyze_failed_extractions()
    
    if not results:
        print("\nNo results to analyze")
        return
    
    improved_count = sum(1 for r in results if r["improvement"])
    total_count = len(results)
    
    # Create method statistics
    method_counts = Counter(r["method"] for r in results)
    total_methods = sum(method_counts.values())
    
    print("\nSUMMARY:")
    print(f"Analyzed {total_count} failed extraction files")
    print(f"Grades recovered: {improved_count}/{total_count} ({improved_count/total_count*100:.1f}%)")
    
    print("\nExtraction methods:")
    for method, count in method_counts.most_common():
        percent = count / total_methods * 100
        print(f"  {method}: {count} ({percent:.1f}%)")
    
    print("\nDetailed results:")
    for r in results:
        improvement_text = "✓ IMPROVED" if r["improvement"] else "✗ UNCHANGED"
        print(f"- {r['model']}: {r['original_grade']} -> {r['advanced_grade']} " +
              f"(conf: {r['confidence']:.2f}, method: {r['method']}) {improvement_text}")
    
    avg_confidence = sum(r["confidence"] for r in results) / len(results)
    print(f"\nAverage confidence: {avg_confidence:.2f}")
    
    print("\nKey findings:")
    if improved_count > 0:
        print(f"1. Advanced techniques recovered {improved_count}/{total_count} grades " +
              f"({improved_count/total_count*100:.1f}%) from previously failed extractions")
        
        # List most effective methods
        effective_methods = [r["method"] for r in results if r["improvement"]]
        method_effectiveness = Counter(effective_methods)
        if method_effectiveness:
            top_method, top_count = method_effectiveness.most_common(1)[0]
            print(f"2. Most effective technique: '{top_method}' " +
                  f"(recovered {top_count}/{improved_count} grades)")
    else:
        print("1. No grades were recovered with advanced techniques")
    
    # Generate recommendations
    print("\nRecommendations for implementation:")
    
    if "contextual_conclusion" in method_counts:
        print("""
1. Implement contextual analysis for conclusions:
   ```python
   def extract_from_conclusion(feedback):
       sentences = feedback.split('.')[-5:]  # Last 5 sentences
       conclusion_text = ' '.join(sentences)
       for pattern in conclusion_patterns:
           match = re.search(pattern, conclusion_text, re.IGNORECASE)
           if match:
               return match.group(1).upper()
       return None
   ```
        """)
        
    if "multi_pass_direct" in method_counts or "multi_pass_proximity" in method_counts:
        print("""
2. Implement multi-pass strategy for handling "Grade:" without a grade:
   ```python
   def handle_missing_grade(feedback):
       if "Grade:" in feedback:
           pos = feedback.find("Grade:")
           after_grade = feedback[pos:pos+100]
           match = re.search(r'[A-C][+-]?', after_grade)
           if match:
               return match.group(0).upper()
       return None
   ```
        """)
        
    if "semantic_descriptors" in method_counts:
        print("""
3. Consider semantic grade detection based on descriptive language:
   ```python
   grade_descriptors = {
       "A": ["excellent", "outstanding", "exceptional"],
       "B": ["good", "competent", "satisfactory"],
       "C": ["average", "fair", "passable"]
   }
   
   def semantic_grade_detection(feedback):
       # Implementation that counts descriptor occurrences
       # and determines most likely grade based on language
   ```
        """)


if __name__ == "__main__":
    run_advanced_analysis()