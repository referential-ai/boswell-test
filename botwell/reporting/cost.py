"""
Cost reporting functionality.
"""

from typing import Dict, Any


def generate_cost_report(results: Dict[str, Any]) -> str:
    """Generate a detailed cost report for the run."""
    cost_data = results["cost"]
    
    # Format total cost and duration
    total_cost = cost_data["total_cost"]
    total_duration = cost_data["total_duration"]
    total_tokens = cost_data["total_tokens"]
    
    report = []
    report.append("# Boswell Test Cost Report\n")
    report.append(f"Run timestamp: {results['run_timestamp']}\n")
    report.append(f"Domain: {results['domain']['name']}\n")
    report.append(f"## Summary\n")
    report.append(f"- **Total cost**: ${total_cost:.4f}")
    report.append(f"- **Total tokens**: {total_tokens:,}")
    report.append(f"- **Total duration**: {total_duration:.2f} seconds\n")
    
    # Essay Generation Costs
    report.append(f"## Essay Generation Costs\n")
    report.append("| Model | Tokens | Cost | Duration (s) |")
    report.append("|-------|--------|------|--------------|")
    
    essay_total_cost = 0
    for model_name, cost_info in cost_data["essay_costs"].items():
        tokens = cost_info["input_tokens"] + cost_info["output_tokens"]
        cost = cost_info["total_cost"]
        duration = cost_info["duration"]
        essay_total_cost += cost
        
        report.append(f"| {model_name} | {tokens:,} | ${cost:.4f} | {duration:.2f} |")
    
    report.append(f"| **TOTAL** | | **${essay_total_cost:.4f}** | |\n")
    
    # Grading Costs
    report.append(f"## Grading Costs\n")
    report.append("| Grader | Essays Graded | Total Tokens | Total Cost | Avg. Cost per Essay |")
    report.append("|--------|---------------|--------------|------------|---------------------|")
    
    grading_total_cost = 0
    for grader_name, gradings in cost_data["grading_costs"].items():
        essays_graded = len(gradings)
        grader_tokens = sum(info["input_tokens"] + info["output_tokens"] for info in gradings.values())
        grader_cost = sum(info["total_cost"] for info in gradings.values())
        avg_cost = grader_cost / essays_graded if essays_graded > 0 else 0
        grading_total_cost += grader_cost
        
        report.append(f"| {grader_name} | {essays_graded} | {grader_tokens:,} | ${grader_cost:.4f} | ${avg_cost:.4f} |")
    
    report.append(f"| **TOTAL** | | | **${grading_total_cost:.4f}** | |\n")
    
    # Cost breakdown by phase
    report.append(f"## Cost Breakdown by Phase\n")
    report.append("| Phase | Cost | Percentage |")
    report.append("|-------|------|------------|")
    
    essay_percent = (essay_total_cost / total_cost) * 100 if total_cost > 0 else 0
    grading_percent = (grading_total_cost / total_cost) * 100 if total_cost > 0 else 0
    
    report.append(f"| Essay Generation | ${essay_total_cost:.4f} | {essay_percent:.1f}% |")
    report.append(f"| Grading | ${grading_total_cost:.4f} | {grading_percent:.1f}% |")
    report.append(f"| **TOTAL** | **${total_cost:.4f}** | **100%** |")
    
    return "\n".join(report)