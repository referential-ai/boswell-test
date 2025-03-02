"""
Timing report functionality.
"""

from typing import Dict, Any


def generate_timing_report(results: Dict[str, Any]) -> str:
    """Generate a detailed timing report for the run."""
    timing_data = results["timing"]
    
    report = []
    report.append("# Boswell Test Timing Report\n")
    report.append(f"Run timestamp: {results['run_timestamp']}\n")
    report.append(f"Domain: {results['domain']['name']}\n")
    
    report.append("## Summary\n")
    
    # Format step durations
    durations = timing_data["step_durations"]
    total = durations["total"]
    
    # Handle case where total might be zero
    if total <= 0:
        # If total is zero, just show the durations without percentages
        report.append(f"- **Total run time**: 0.0s")
        report.append(f"- **Essay generation**: {durations['essay_generation']:.1f}s")
        report.append(f"- **Grading**: {durations['grading']:.1f}s")
        report.append(f"- **Analysis**: {durations['analysis']:.1f}s")
        report.append(f"- **File generation**: {durations['file_generation']:.1f}s\n")
    else:
        # Format durations manually - don't rely on 'formatted' which might not exist yet
        minutes, seconds = divmod(total, 60)
        formatted_total = f"{int(minutes)}m {seconds:.1f}s"
        
        report.append(f"- **Total run time**: {formatted_total}")
        report.append(f"- **Essay generation**: {durations['essay_generation']:.1f}s ({durations['essay_generation']/total*100:.1f}%)")
        report.append(f"- **Grading**: {durations['grading']:.1f}s ({durations['grading']/total*100:.1f}%)")
        report.append(f"- **Analysis**: {durations['analysis']:.1f}s ({durations['analysis']/total*100:.1f}%)")
        report.append(f"- **File generation**: {durations['file_generation']:.1f}s ({durations['file_generation']/total*100:.1f}%)\n")
    
    # Essay generation timing by model
    report.append("## Essay Generation Timing\n")
    report.append("| Model | Duration (s) |")
    report.append("|-------|-------------|")
    
    for model, duration in timing_data["model_timing"]["essay"].items():
        report.append(f"| {model} | {duration:.2f} |")
    
    # Calculate average essay generation time
    if timing_data["model_timing"]["essay"]:
        avg_essay_time = sum(timing_data["model_timing"]["essay"].values()) / len(timing_data["model_timing"]["essay"])
        report.append(f"| **Average** | **{avg_essay_time:.2f}** |\n")
    
    # Grading timing by model
    report.append("## Grading Timing\n")
    report.append("| Grader | Essays Graded | Total Duration (s) | Avg. Seconds per Essay |")
    report.append("|--------|---------------|-------------------|------------------------|")
    
    for grader, gradings in timing_data["model_timing"]["grading"].items():
        essays_graded = len(gradings)
        total_time = sum(gradings.values())
        avg_time = total_time / essays_graded if essays_graded > 0 else 0
        
        report.append(f"| {grader} | {essays_graded} | {total_time:.2f} | {avg_time:.2f} |")
    
    return "\n".join(report)