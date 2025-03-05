"""
Boswell report generation functionality.
"""

from typing import Dict, Any
from botwell.reporting.tables import generate_boswell_quotient_table
from botwell.reporting.boswell_quotient import interpret_boswell_quotient


def generate_boswell_report(results: Dict[str, Any], quotient_results: Dict[str, Any]) -> str:
    """Generate a detailed report on the Boswell Quotient results.
    
    The report includes:
    1. Introduction to the Boswell Quotient
    2. Overall ranking of models
    3. Component breakdown and analysis
    4. Insights and observations
    """
    domain_info = results["domain"]
    timestamp = results["run_timestamp"]
    
    # Calculate some statistics for the report
    model_scores = quotient_results["model_scores"]
    sorted_models = sorted(
        model_scores.keys(),
        key=lambda m: model_scores[m]["rank"]
    )
    
    # Get top and bottom 3 models (or fewer if less than 6 models total)
    top_models = sorted_models[:min(3, len(sorted_models))]
    bottom_models = sorted_models[max(0, len(sorted_models)-3):]
    
    # Find performance leaders in each component
    component_leaders = {
        "performance": {"model": "", "score": 0},
        "evaluation": {"model": "", "score": 0},
        "efficiency": {"model": "", "score": 0},
        "empathy": {"model": "", "score": 0}
    }
    
    for model in sorted_models:
        components = model_scores[model]["components"]
        for component in component_leaders:
            if component in components:
                score = components[component]
                if score > component_leaders[component]["score"]:
                    component_leaders[component]["model"] = model
                    component_leaders[component]["score"] = score
    
    # Generate the report
    lines = []
    
    # Title and introduction
    lines.append("# Boswell Quotient Analysis Report")
    lines.append(f"\nRun timestamp: {timestamp}")
    lines.append(f"Domain: {domain_info['name']}")
    
    # Introduction section
    lines.append("\n## Introduction to the Boswell Quotient")
    lines.append(
        "The Boswell Quotient is a comprehensive metric designed to evaluate LLM capabilities across multiple dimensions. "
        "Named after James Boswell, who was known for his deep understanding and insightful observations of Samuel Johnson, "
        "this quotient aims to measure how well an AI model can serve as an indispensable companion in academic and analytical tasks."
    )
    lines.append("\nThe Boswell Quotient (0-100) is calculated from four key components:")
    lines.append("1. **Performance (25%)**: How well the model performs in generating content, based on grades received from peers")
    lines.append("2. **Evaluation (25%)**: How accurately and consistently the model evaluates others' work")
    lines.append("3. **Efficiency (25%)**: How quickly the model completes tasks")
    lines.append("4. **Empathy (25%)**: How well the model demonstrates emotional intelligence in responses")
    
    # Overall ranking section
    lines.append("\n## Overall Model Rankings")
    lines.append("The table below shows all models ranked by their Boswell Quotient:")
    
    # Add the full table
    lines.append("\n" + generate_boswell_quotient_table(quotient_results))
    
    # Top performers section
    lines.append("\n## Top Performing Models")
    if top_models:
        top_model = top_models[0]
        top_score = model_scores[top_model]["boswell_quotient"]
        lines.append(f"\n**{top_model}** achieved the highest Boswell Quotient of **{top_score:.1f}**, ")
        
        # Add description of why the top model performed well
        components = model_scores[top_model]["components"]
        strengths = []
        
        if "performance" in components and components["performance"] > 85:
            strengths.append("exceptional content quality")
        elif "performance" in components and components["performance"] > 75:
            strengths.append("strong content quality")
            
        if "evaluation" in components and components["evaluation"] > 85:
            strengths.append("excellent evaluation capabilities")
        elif "evaluation" in components and components["evaluation"] > 75:
            strengths.append("good evaluation consistency")
            
        if "efficiency" in components and components["efficiency"] > 85:
            strengths.append("outstanding efficiency")
        elif "efficiency" in components and components["efficiency"] > 75:
            strengths.append("good response time")
            
        if strengths:
            lines.append(f"demonstrating {', '.join(strengths)}.")
        else:
            lines.append("with balanced performance across all components.")
        
        # Mention other top performers
        if len(top_models) > 1:
            other_tops = [f"**{m}** ({model_scores[m]['boswell_quotient']:.1f})" for m in top_models[1:]]
            lines.append(f"\nOther top performers include {', '.join(other_tops)}.")
    
    # Component analysis section
    lines.append("\n## Component Analysis")
    
    # Performance component
    lines.append("\n### Performance Component")
    performance_leader = component_leaders["performance"]["model"]
    performance_score = component_leaders["performance"]["score"]
    
    if performance_leader:
        lines.append(
            f"**{performance_leader}** leads in the Performance component with a score of **{performance_score:.1f}**. "
            f"This reflects the model's ability to generate high-quality content that receives favorable evaluations from peers."
        )
    
    # Evaluation component
    lines.append("\n### Evaluation Component")
    evaluation_leader = component_leaders["evaluation"]["model"]
    evaluation_score = component_leaders["evaluation"]["score"]
    
    if evaluation_leader:
        lines.append(
            f"**{evaluation_leader}** excels in the Evaluation component with a score of **{evaluation_score:.1f}**. "
            f"This indicates the model's ability to provide consistent and fair assessments that align with the consensus."
        )
    
    # Efficiency component
    lines.append("\n### Efficiency Component")
    efficiency_leader = component_leaders["efficiency"]["model"]
    efficiency_score = component_leaders["efficiency"]["score"]
    
    if efficiency_leader:
        lines.append(
            f"**{efficiency_leader}** demonstrates superior Efficiency with a score of **{efficiency_score:.1f}**. "
            f"This reflects the model's ability to generate responses and evaluations quickly while using resources effectively."
        )
        
    # Empathy component
    lines.append("\n### Empathy Component")
    empathy_leader = component_leaders["empathy"]["model"]
    empathy_score = component_leaders["empathy"]["score"]
    
    if empathy_leader:
        lines.append(
            f"**{empathy_leader}** excels in the Empathy component with a score of **{empathy_score:.1f}**. "
            f"This indicates the model's ability to recognize emotions, validate feelings, and provide supportive responses."
        )
    
    # Observations and insights
    lines.append("\n## Observations and Insights")
    
    # Look for models with balanced performance
    balanced_models = []
    for model in sorted_models:
        components = model_scores[model]["components"]
        if len(components) >= 3:  # Has all three components
            scores = [components.get(c, 0) for c in ["performance", "evaluation", "efficiency"]]
            if scores[0] > 0 and scores[1] > 0 and scores[2] > 0:
                # Check if all scores are within 15 points of each other
                if max(scores) - min(scores) <= 15:
                    balanced_models.append((model, model_scores[model]["boswell_quotient"]))
    
    if balanced_models:
        balanced_models.sort(key=lambda x: x[1], reverse=True)
        balanced_list = [f"**{m}** ({s:.1f})" for m, s in balanced_models[:3]]
        lines.append(
            f"The most balanced models across all components were {', '.join(balanced_list)}. "
            f"These models demonstrate well-rounded capabilities essential for being a reliable AI assistant."
        )
    
    # Look for interesting patterns or outliers
    performance_vs_evaluation = []
    for model in sorted_models:
        components = model_scores[model]["components"]
        if "performance" in components and "evaluation" in components:
            perf = components["performance"]
            eval_score = components["evaluation"]
            if abs(perf - eval_score) > 20:  # Significant difference
                performance_vs_evaluation.append((model, perf, eval_score))
    
    if performance_vs_evaluation:
        # Models that are better at performance than evaluation
        better_performers = [(m, p, e) for m, p, e in performance_vs_evaluation if p > e]
        if better_performers:
            example = better_performers[0]
            lines.append(
                f"\n**{example[0]}** and similar models demonstrate significantly higher content quality "
                f"({example[1]:.1f}) than evaluation consistency ({example[2]:.1f}). "
                f"This suggests these models excel at generating content but may need improvement in "
                f"their critical assessment capabilities."
            )
        
        # Models that are better at evaluation than performance
        better_evaluators = [(m, p, e) for m, p, e in performance_vs_evaluation if e > p]
        if better_evaluators:
            example = better_evaluators[0]
            lines.append(
                f"\n**{example[0]}** and similar models show stronger evaluation capabilities "
                f"({example[2]:.1f}) compared to content generation ({example[1]:.1f}). "
                f"These models may excel as critics or reviewers rather than primary content generators."
            )
    
    # Conclusion
    lines.append("\n## Conclusion")
    lines.append(
        "The Boswell Quotient provides a multi-dimensional assessment of AI models' capabilities, "
        "helping identify which models are best suited for different use cases. A high Boswell Quotient "
        "indicates a model that can effectively serve as a comprehensive AI assistant - generating high-quality "
        "content, providing accurate evaluations, and doing so efficiently."
    )
    
    if top_models:
        top_three = [f"**{m}**" for m in top_models[:min(3, len(top_models))]]
        lines.append(f"\nBased on this analysis, {', '.join(top_three)} stand out as the most capable AI assistants in this domain.")
    
    # Add repository information
    lines.append("\n## Repository Information")
    lines.append("This report was generated by the [Boswell Test](https://github.com/referential-ai/boswell-test) framework, " +
                "an open-source project for evaluating and comparing LLM performance through essay generation and peer grading.")
    
    # Return the full report
    return "\n".join(lines)