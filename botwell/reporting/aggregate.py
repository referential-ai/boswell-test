"""
Aggregate reporting functionality across domains.
"""

import os
import json
import time
from typing import Dict, Any, List

from botwell.core.files import find_result_directories
from botwell.domains import AVAILABLE_DOMAINS


def aggregate_boswell_quotient(domain_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate Boswell Quotient scores across multiple domains.
    
    Args:
        domain_results: Dictionary of domain names to result dictionaries
        
    Returns:
        Dictionary containing aggregated Boswell Quotient data
    """
    # Initialize data structure for aggregated results
    aggregated = {
        "model_scores": {},
        "domains_analyzed": list(domain_results.keys()),
        "component_weights": {  
            "performance": 0.25,
            "evaluation": 0.25,
            "efficiency": 0.25,
            "empathy": 0.25
        }
    }
    
    # Track which models appear in which domains
    model_domains = {}
    
    # Collect all Boswell Quotient data by model across domains
    for domain_name, results in domain_results.items():
        if "boswell_quotient" in results and "model_scores" in results["boswell_quotient"]:
            model_scores = results["boswell_quotient"]["model_scores"]
            
            for model, score_data in model_scores.items():
                # Initialize model entry if not exists
                if model not in aggregated["model_scores"]:
                    aggregated["model_scores"][model] = {
                        "domain_scores": {},
                        "domain_components": {},
                        "average_boswell_quotient": 0.0,
                        "rank": 0
                    }
                
                # Add domain-specific data
                aggregated["model_scores"][model]["domain_scores"][domain_name] = score_data["boswell_quotient"]
                aggregated["model_scores"][model]["domain_components"][domain_name] = score_data.get("components", {})
                
                # Track which domains this model appears in
                if model not in model_domains:
                    model_domains[model] = []
                model_domains[model].append(domain_name)
    
    # Calculate aggregate scores
    for model, data in aggregated["model_scores"].items():
        # Calculate average Boswell Quotient across all domains where the model appears
        if data["domain_scores"]:
            data["average_boswell_quotient"] = sum(data["domain_scores"].values()) / len(data["domain_scores"])
            
            # Calculate aggregated component scores
            all_components = {
                "performance": [],
                "evaluation": [],
                "efficiency": [],
                "empathy": []
            }
            
            # Collect component scores from all domains
            for domain, components in data["domain_components"].items():
                for component in all_components:
                    if component in components:
                        all_components[component].append(components[component])
            
            # Calculate average for each component
            data["aggregated_components"] = {}
            for component, scores in all_components.items():
                if scores:
                    data["aggregated_components"][component] = sum(scores) / len(scores)
    
    # Rank models by average Boswell Quotient
    sorted_models = sorted(
        aggregated["model_scores"].keys(),
        key=lambda m: aggregated["model_scores"][m]["average_boswell_quotient"],
        reverse=True
    )
    
    # Assign ranks
    for i, model in enumerate(sorted_models):
        aggregated["model_scores"][model]["rank"] = i + 1
    
    # Add consistency metrics - how consistent are models across domains?
    for model, data in aggregated["model_scores"].items():
        if len(data["domain_scores"]) > 1:
            scores = list(data["domain_scores"].values())
            max_score = max(scores)
            min_score = min(scores)
            
            # Calculate consistency as 100 - (max-min)
            # Higher values mean more consistent performance across domains
            data["consistency"] = 100 - (max_score - min_score)
            
            # Add domain count
            data["domain_count"] = len(data["domain_scores"])
            
            # Identify best and worst domains
            best_domain = max(data["domain_scores"].items(), key=lambda x: x[1])[0]
            worst_domain = min(data["domain_scores"].items(), key=lambda x: x[1])[0]
            
            data["best_domain"] = best_domain
            data["worst_domain"] = worst_domain
    
    return aggregated


def generate_aggregate_boswell_report(aggregated_data: Dict[str, Any], domain_descriptions: Dict[str, str]) -> str:
    """Generate a comprehensive report of aggregate Boswell Quotient results.
    
    Args:
        aggregated_data: Aggregated Boswell Quotient data
        domain_descriptions: Dictionary mapping domain IDs to descriptions
        
    Returns:
        Markdown report as a string
    """
    lines = []
    
    # Title and introduction
    lines.append("# Aggregate Boswell Quotient Analysis Across Domains")
    lines.append(f"\nThis report aggregates model performance across {len(aggregated_data['domains_analyzed'])} domains:")
    
    # List the domains included
    for domain_id in aggregated_data['domains_analyzed']:
        domain_desc = domain_descriptions.get(domain_id, domain_id)
        lines.append(f"- **{domain_desc}**")
    
    # Overall model rankings table
    lines.append("\n## Overall Model Rankings")
    lines.append("\nThe table below shows models ranked by their average Boswell Quotient across all domains:")
    lines.append("\n| Rank | Model | Boswell Quotient | Grade | Domain Count | Consistency | Best Domain | Worst Domain |")
    lines.append("|------|-------|-----------------|-------|--------------|-------------|------------|-------------|")
    
    # Import needed functions
    from botwell.core.grading import percentage_to_letter_grade
    
    # Sort models by rank
    sorted_models = sorted(
        aggregated_data["model_scores"].keys(),
        key=lambda m: aggregated_data["model_scores"][m]["rank"]
    )
    
    # Add each model's data
    for model in sorted_models:
        data = aggregated_data["model_scores"][model]
        
        rank = data["rank"]
        avg_score = data["average_boswell_quotient"]
        
        # Convert to letter grade
        letter_grade = percentage_to_letter_grade(int(avg_score))
        
        domain_count = data.get("domain_count", len(data["domain_scores"]))
        
        # Format consistency if available
        consistency = data.get("consistency", "N/A")
        if consistency != "N/A":
            consistency = f"{consistency:.1f}"
            
        # Get best and worst domains with descriptions
        best_domain = data.get("best_domain", list(data["domain_scores"].keys())[0] if data["domain_scores"] else "N/A")
        worst_domain = data.get("worst_domain", best_domain)
        
        best_domain_desc = domain_descriptions.get(best_domain, best_domain)
        worst_domain_desc = domain_descriptions.get(worst_domain, worst_domain)
        
        # Format row
        lines.append(f"| {rank} | {model} | {avg_score:.1f} | {letter_grade} | {domain_count} | {consistency} | {best_domain_desc} | {worst_domain_desc} |")
    
    # Top performers section
    if sorted_models:
        lines.append("\n## Top Performing Models")
        top_model = sorted_models[0]
        top_data = aggregated_data["model_scores"][top_model]
        
        lines.append(f"\n**{top_model}** achieved the highest average Boswell Quotient of **{top_data['average_boswell_quotient']:.1f}** " +
                    f"across {len(top_data['domain_scores'])} domains.")
        
        # Add information about consistency for top model
        if "consistency" in top_data:
            if top_data["consistency"] > 90:
                lines.append(f"With a consistency score of {top_data['consistency']:.1f}, it demonstrated remarkably stable performance across all domains.")
            elif top_data["consistency"] > 75:
                lines.append(f"With a consistency score of {top_data['consistency']:.1f}, it performed well across most domains with some variation.")
            else:
                lines.append(f"With a consistency score of {top_data['consistency']:.1f}, it showed significant performance variation across domains.")
                
                # Mention best and worst domains
                best = domain_descriptions.get(top_data["best_domain"], top_data["best_domain"])
                worst = domain_descriptions.get(top_data["worst_domain"], top_data["worst_domain"])
                lines.append(f"It performed best in **{best}** and had more difficulty with **{worst}**.")
        
        # Mention other top performers
        if len(sorted_models) > 1:
            runner_ups = []
            for model in sorted_models[1:4]:  # Get up to next 3 models
                if model in aggregated_data["model_scores"]:
                    score = aggregated_data["model_scores"][model]["average_boswell_quotient"]
                    runner_ups.append(f"**{model}** ({score:.1f})")
            
            if runner_ups:
                lines.append(f"\nOther strong performers include {', '.join(runner_ups)}.")
    
    # Domain-specific leaders
    lines.append("\n## Domain-Specific Leaders")
    lines.append("\nThe table below shows which models performed best in each domain:")
    lines.append("\n| Domain | Top Model | Boswell Quotient | Grade |")
    lines.append("|--------|-----------|------------------|-------|")
    
    # Find top model for each domain
    for domain_id in aggregated_data["domains_analyzed"]:
        domain_desc = domain_descriptions.get(domain_id, domain_id)
        
        # Find the best model for this domain
        best_model = ""
        best_score = 0
        
        for model, data in aggregated_data["model_scores"].items():
            if domain_id in data["domain_scores"] and data["domain_scores"][domain_id] > best_score:
                best_model = model
                best_score = data["domain_scores"][domain_id]
        
        if best_model:
            # Convert to letter grade
            letter_grade = percentage_to_letter_grade(int(best_score))
            lines.append(f"| {domain_desc} | {best_model} | {best_score:.1f} | {letter_grade} |")
    
    # Overall insights
    lines.append("\n## Key Insights")
    
    # Find models that perform consistently across domains
    consistent_models = []
    for model, data in aggregated_data["model_scores"].items():
        if "consistency" in data and data["consistency"] > 85 and len(data["domain_scores"]) > 1:
            consistent_models.append((model, data["consistency"], data["average_boswell_quotient"]))
    
    if consistent_models:
        # Sort by consistency
        consistent_models.sort(key=lambda x: x[1], reverse=True)
        
        # Take up to top 3
        top_consistent = consistent_models[:min(3, len(consistent_models))]
        model_list = [f"**{m}** (consistency: {c:.1f})" for m, c, _ in top_consistent]
        
        lines.append("\n### Most Consistent Performers")
        lines.append(f"These models maintained the most consistent performance across different domains: {', '.join(model_list)}.")
        lines.append("High consistency suggests these models have broad capabilities that transfer well between different subject areas.")
    
    # Find specialists (high performance in specific domains)
    specialists = []
    for model, data in aggregated_data["model_scores"].items():
        if len(data["domain_scores"]) > 1:
            scores = list(data["domain_scores"].values())
            max_score = max(scores)
            avg_other = sum(s for s in scores if s != max_score) / (len(scores) - 1)
            
            # If top domain is significantly better than average of others
            if max_score > avg_other + 10:
                best_domain = max(data["domain_scores"].items(), key=lambda x: x[1])[0]
                specialists.append((model, best_domain, max_score, max_score - avg_other))
    
    if specialists:
        # Sort by specialization gap
        specialists.sort(key=lambda x: x[3], reverse=True)
        
        lines.append("\n### Domain Specialists")
        lines.append("These models showed significantly stronger performance in specific domains:")
        
        for model, domain, score, gap in specialists[:min(3, len(specialists))]:
            domain_desc = domain_descriptions.get(domain, domain)
            lines.append(f"- **{model}** excels in **{domain_desc}** (score: {score:.1f}, {gap:.1f} points above its average in other domains)")
    
    # Conclusion
    lines.append("\n## Conclusion")
    lines.append(
        "The aggregated Boswell Quotient provides a comprehensive view of model capabilities across multiple domains, "
        "helping identify both generalist models that perform consistently well across diverse tasks and specialist models "
        "that excel in particular areas."
    )
    
    if sorted_models:
        lines.append(
            f"\nBased on this cross-domain analysis, **{sorted_models[0]}** emerges as the most capable overall AI assistant, "
            f"with strong performance across the tested domains."
        )
    
    return "\n".join(lines)


def load_domain_results(results_dir: str) -> Dict[str, Any]:
    """Load results from a domain directory.
    
    Args:
        results_dir: Path to the results directory
        
    Returns:
        The loaded results dictionary or None if loading fails
    """
    import re
    
    try:
        full_results_path = os.path.join(results_dir, "full_results.json")
        if not os.path.exists(full_results_path):
            print(f"Error: No full_results.json found in {results_dir}")
            return None
            
        with open(full_results_path, 'r') as f:
            results = json.load(f)
            
        # Extract domain name from path
        domain_match = re.search(r"-([a-z_]+\d*)(-free)?$", results_dir)
        if domain_match:
            domain_id = domain_match.group(1)
            if domain_id not in AVAILABLE_DOMAINS:
                print(f"Warning: Domain '{domain_id}' from {results_dir} is not in AVAILABLE_DOMAINS")
                
        return results
    except Exception as e:
        print(f"Error loading results from {results_dir}: {e}")
        return None


def aggregate_existing_results(results_dirs: List[str] = None) -> None:
    """Generate an aggregate report from existing result directories.
    
    Args:
        results_dirs: Optional list of specific result directories to include
    """
    # Find result directories if not specified
    if not results_dirs:
        results_dirs = find_result_directories()
        
    if not results_dirs:
        print("Error: No result directories found. Run tests first before aggregating.")
        return
        
    print(f"Aggregating results from {len(results_dirs)} directories:")
    for dir_path in results_dirs:
        print(f"  - {dir_path}")
        
    # Load results from each directory
    results_by_domain = {}
    
    for dir_path in results_dirs:
        results = load_domain_results(dir_path)
        if results:
            domain_info = results.get("domain", {})
            domain_name = domain_info.get("name", "Unknown Domain")
            
            # Extract domain key from path
            import re
            domain_match = re.search(r"-([a-z_]+\d*)(-free)?$", dir_path)
            if domain_match:
                domain_key = domain_match.group(1)
                results_by_domain[domain_key] = {
                    "directory": dir_path,
                    "domain": domain_name,
                    "boswell_quotient": results.get("boswell_quotient", {}),
                    "run_timestamp": results.get("run_timestamp", "")
                }
                print(f"  - Successfully loaded results for: {domain_name}")
    
    if not results_by_domain:
        print("Error: Failed to load any valid result sets.")
        return
        
    # Create timestamp for aggregate results
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Create aggregate results directory
    aggregate_dir = f"results/{timestamp}-aggregate"
    os.makedirs(aggregate_dir, exist_ok=True)
    
    # Generate aggregate data
    aggregated_data = aggregate_boswell_quotient(results_by_domain)
    
    # Create mapping of domain IDs to descriptions
    domain_descriptions = {name: desc for name, desc in AVAILABLE_DOMAINS.items()}
    
    # Generate aggregate report
    aggregate_report = generate_aggregate_boswell_report(aggregated_data, domain_descriptions)
    
    # Save aggregate report
    with open(f"{aggregate_dir}/aggregate_boswell_report.md", 'w') as f:
        f.write(aggregate_report)
    
    # Generate aggregate visualizations
    from botwell.reporting.visualizations import generate_aggregate_visualizations
    generate_aggregate_visualizations(aggregated_data, aggregate_dir)
    
    # Save aggregate data as JSON
    with open(f"{aggregate_dir}/aggregate_boswell_quotient.json", 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "aggregated_data": aggregated_data,
            "source_domains": [d for d in aggregated_data["domains_analyzed"]],
            "domain_descriptions": domain_descriptions,
            "source_directories": results_dirs
        }, f, indent=2)
    
    print(f"\nAggregate results generated successfully!")
    print(f"  - Aggregate report: {aggregate_dir}/aggregate_boswell_report.md")
    print(f"  - Visualizations: {aggregate_dir}/charts/aggregate_boswell_quotient.png")
    print(f"                    {aggregate_dir}/charts/domain_comparison.png")