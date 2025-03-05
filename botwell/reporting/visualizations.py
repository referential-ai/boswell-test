"""
Visualization generation functionality.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, List


def generate_visualizations(results: Dict[str, Any], run_dir: str) -> None:
    """Generate data visualizations of the test results."""
    models = list(results["essays"].keys())
    
    # Create a charts directory
    charts_dir = f"{run_dir}/charts"
    os.makedirs(charts_dir, exist_ok=True)
    
    # 1. Chart: Grading bias visualization
    plt.figure(figsize=(12, 8))
    
    bias_data = results.get("bias_analysis", {}).get("grader_bias", {})
    if bias_data:
        graders = list(bias_data.keys())
        median_bias = [bias_data[grader]["median_bias"] for grader in graders]
        
        # Sort by bias value for better visualization
        sorted_indices = np.argsort(median_bias)
        sorted_graders = [graders[i] for i in sorted_indices]
        sorted_bias = [median_bias[i] for i in sorted_indices]
        
        # Color bars based on bias (red for negative/strict, green for positive/lenient)
        colors = ['#FF6B6B' if bias < 0 else '#4ECDC4' for bias in sorted_bias]
        
        plt.bar(sorted_graders, sorted_bias, color=colors)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.title('Grading Bias by Model')
        plt.xlabel('Model')
        plt.ylabel('Bias (Negative = Stricter, Positive = More Lenient)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/grading_bias.png", dpi=300)
        plt.close()
    
    # 2. Chart: Grade distribution
    plt.figure(figsize=(12, 8))
    
    # Collect all numeric grades
    numeric_grades = {}
    for model in models:
        grades = []
        for grader, grades_given in results.get("grades", {}).items():
            if model in grades_given:
                grades.append(grades_given[model]["numeric_grade"])
        if grades:
            numeric_grades[model] = grades
    
    if numeric_grades:
        # Create boxplot of grades received by each model
        plt.boxplot([numeric_grades[model] for model in models], 
                   tick_labels=models, 
                   patch_artist=True,
                   boxprops=dict(facecolor='#A8DADC'))
        
        plt.title('Distribution of Grades Received by Each Model')
        plt.ylabel('Numeric Grade')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/grade_distribution.png", dpi=300)
        plt.close()
    
    # 3. Chart: Timing comparison
    plt.figure(figsize=(12, 8))
    
    timing_data = results.get("timing", {}).get("model_timing", {}).get("essay", {})
    if timing_data:
        model_names = list(timing_data.keys())
        times = list(timing_data.values())
        
        # Sort by time for better visualization
        sorted_indices = np.argsort(times)
        sorted_models = [model_names[i] for i in sorted_indices]
        sorted_times = [times[i] for i in sorted_indices]
        
        plt.barh(sorted_models, sorted_times, color='#457B9D')
        plt.title('Time to Generate Essay by Model')
        plt.xlabel('Time (seconds)')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/essay_generation_time.png", dpi=300)
        plt.close()
    
    # 4. Chart: Grading time comparison
    plt.figure(figsize=(12, 8))
    
    grading_data = results.get("timing", {}).get("model_timing", {}).get("grading", {})
    if grading_data:
        # Calculate average grading time for each model
        avg_grading_times = {}
        for grader, times in grading_data.items():
            if times:
                avg_grading_times[grader] = sum(times.values()) / len(times)
        
        if avg_grading_times:
            graders = list(avg_grading_times.keys())
            avg_times = list(avg_grading_times.values())
            
            # Sort by time for better visualization
            sorted_indices = np.argsort(avg_times)
            sorted_graders = [graders[i] for i in sorted_indices]
            sorted_avg_times = [avg_times[i] for i in sorted_indices]
            
            plt.barh(sorted_graders, sorted_avg_times, color='#1D3557')
            plt.title('Average Grading Time by Model')
            plt.xlabel('Time (seconds)')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(f"{charts_dir}/average_grading_time.png", dpi=300)
            plt.close()
    
    # 5. Chart: Cost breakdown
    plt.figure(figsize=(12, 8))
    
    # Essay costs
    essay_costs = {}
    for model, cost_info in results.get("cost", {}).get("essay_costs", {}).items():
        essay_costs[model] = cost_info.get("total_cost", 0)
    
    # Grading costs
    grading_costs = {}
    for grader, gradings in results.get("cost", {}).get("grading_costs", {}).items():
        grading_costs[grader] = sum(info.get("total_cost", 0) for info in gradings.values())
    
    if essay_costs and grading_costs:
        # Prepare data for stacked bar chart
        models_with_both = [m for m in models if m in essay_costs and m in grading_costs]
        essay_cost_values = [essay_costs.get(m, 0) for m in models_with_both]
        grading_cost_values = [grading_costs.get(m, 0) for m in models_with_both]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bar_width = 0.5
        
        # Create stacked bars
        ax.bar(models_with_both, essay_cost_values, bar_width, 
               label='Essay Generation', color='#E9C46A')
        ax.bar(models_with_both, grading_cost_values, bar_width,
               bottom=essay_cost_values, label='Grading', color='#F4A261')
        
        ax.set_title('Cost Breakdown by Model')
        ax.set_xlabel('Model')
        ax.set_ylabel('Cost ($)')
        ax.legend()
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/cost_breakdown.png", dpi=300)
        plt.close()
    
    # 6. Chart: Process timing breakdown
    plt.figure(figsize=(10, 6))
    
    durations = results.get("timing", {}).get("step_durations", {})
    if durations:
        steps = ['essay_generation', 'grading', 'analysis', 'file_generation']
        step_names = ['Essay Generation', 'Grading', 'Analysis', 'File Generation']
        times = [durations.get(step, 0) for step in steps]
        
        # Check if we have any non-zero times to create a meaningful pie chart
        if sum(times) > 0:
            # Create pie chart
            plt.pie(times, labels=step_names, autopct='%1.1f%%', 
                    startangle=90, shadow=False, 
                    colors=['#264653', '#2A9D8F', '#E9C46A', '#F4A261'])
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            plt.title('Time Breakdown by Process Phase')
        else:
            # If all times are zero, create a placeholder message
            plt.text(0.5, 0.5, 'No timing data available', 
                     horizontalalignment='center', verticalalignment='center',
                     fontsize=14)
            plt.title('Time Breakdown by Process Phase')
            plt.axis('off')  # Hide axes
        
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/time_breakdown.png", dpi=300)
        plt.close()
    
    # 7. Chart: Boswell Quotient visualization
    if "boswell_quotient" in results and "model_scores" in results["boswell_quotient"]:
        plt.figure(figsize=(14, 8))
        
        quotient_data = results["boswell_quotient"]["model_scores"]
        
        # Sort models by Boswell Quotient score (descending)
        sorted_models = sorted(
            quotient_data.keys(),
            key=lambda m: quotient_data[m]["boswell_quotient"],
            reverse=True
        )
        
        # Prepare data for visualization
        scores = [quotient_data[model]["boswell_quotient"] for model in sorted_models]
        
        # Create bar chart for overall Boswell Quotient
        plt.barh(sorted_models, scores, color='#6A5ACD')
        plt.title('Boswell Quotient by Model', fontsize=16)
        plt.xlabel('Boswell Quotient (0-100)', fontsize=12)
        plt.yticks(fontsize=10)
        plt.xlim(0, 100)  # Scale from 0 to 100
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/boswell_quotient.png", dpi=300)
        plt.close()
        
        # 8. Chart: Boswell Quotient component breakdown
        plt.figure(figsize=(14, 10))
        
        # Prepare component data
        components = ["performance", "evaluation", "efficiency", "empathy"]
        component_data = {component: [] for component in components}
        
        for model in sorted_models:
            model_components = quotient_data[model].get("components", {})
            for component in components:
                component_data[component].append(model_components.get(component, 0))
        
        # Set up the bar chart
        bar_width = 0.2
        index = np.arange(len(sorted_models))
        
        # Plot each component
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Set colors for components
        colors = ['#4CAF50', '#2196F3', '#FF9800', '#E91E63']  # Green, Blue, Orange, Pink
        
        # Plot bars for each component
        for i, component in enumerate(components):
            ax.barh(index + i*bar_width, component_data[component], 
                   bar_width, label=component.capitalize(), color=colors[i])
        
        # Configure axes and labels
        ax.set_yticks(index + 1.5*bar_width)
        ax.set_yticklabels(sorted_models)
        ax.set_xlabel('Component Score (0-100)')
        ax.set_title('Boswell Quotient Component Breakdown by Model')
        ax.set_xlim(0, 100)
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/boswell_quotient_components.png", dpi=300)
        plt.close()
    
    print(f"  Visualizations saved to {charts_dir}")


def generate_aggregate_visualizations(aggregated_data: Dict[str, Any], aggregate_dir: str) -> None:
    """Generate visualization charts for aggregate data across domains."""
    # Create charts directory
    charts_dir = f"{aggregate_dir}/charts"
    os.makedirs(charts_dir, exist_ok=True)
    
    # Create aggregate Boswell Quotient chart
    plt.figure(figsize=(14, 8))
    
    # Prepare data
    sorted_models = sorted(
        aggregated_data["model_scores"].keys(),
        key=lambda m: aggregated_data["model_scores"][m]["average_boswell_quotient"],
        reverse=True
    )
    
    scores = [aggregated_data["model_scores"][m]["average_boswell_quotient"] for m in sorted_models]
    
    # Get component scores for stacked bars
    components = ["performance", "evaluation", "efficiency", "empathy"]
    component_data = {component: [] for component in components}
    component_weights = aggregated_data.get("component_weights", {
        "performance": 0.25,
        "evaluation": 0.25,
        "efficiency": 0.25,
        "empathy": 0.25
    })
    
    for model in sorted_models:
        model_components = aggregated_data["model_scores"][model].get("average_components", {})
        for component in components:
            # Scale the component by its weight for the stacked bar
            value = model_components.get(component, 0) * component_weights.get(component, 0.25)
            component_data[component].append(value)
    
    # Create bar chart with a colorful gradient
    cmap = plt.cm.viridis  # Choose a colorful colormap
    colors = cmap(np.linspace(0.2, 0.8, len(scores)))
    
    # Create horizontal bar chart with custom colors and styling
    bars = plt.barh(sorted_models, scores, color=colors)
    
    # Add score values at the end of each bar
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                f'{scores[i]:.1f}', 
                va='center', fontsize=9)
    
    # Style the chart
    plt.title('Aggregate Boswell Quotient by Model (All Domains)', fontsize=16, fontweight='bold')
    plt.xlabel('Boswell Quotient (0-100)', fontsize=12, fontweight='bold')
    plt.yticks(fontsize=10)
    plt.xlim(0, 105)  # Extend limit to allow space for score labels
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Add a gradient colorbar for reference
    sm = plt.cm.ScalarMappable(cmap=cmap)
    sm.set_array([])
    
    # Background styling
    ax = plt.gca()
    cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.1, aspect=40)
    cbar.set_label('Higher Score → Better Performance', fontsize=10)
    
    ax.set_facecolor('#f8f9fa')  # Light background
    plt.gcf().set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    
    # Save chart
    plt.savefig(f"{charts_dir}/aggregate_boswell_quotient.png", dpi=300)
    plt.close()
    
    # Create component breakdown chart for aggregate data
    plt.figure(figsize=(14, 10))
    
    # Create stacked horizontal bar chart for components
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Set colors for components
    component_colors = {
        "performance": '#4CAF50',  # Green
        "evaluation": '#2196F3',   # Blue
        "efficiency": '#FF9800',   # Orange
        "empathy": '#E91E63'       # Pink
    }
    
    # Initialize left position for each bar
    left = np.zeros(len(sorted_models))
    
    for component in components:
        # Convert raw scores to weighted scores (0-25 points each)
        weight = component_weights.get(component, 0.25)
        weighted_scores = [aggregated_data["model_scores"][model].get("aggregated_components", {}).get(component, 0) * weight for model in sorted_models]
        
        ax.barh(sorted_models, weighted_scores, left=left, height=0.7,
                label=f"{component.capitalize()} ({int(weight*100)}%)", color=component_colors[component])
        
        # Update left position for next component
        left += weighted_scores
    
    # Style the chart
    ax.set_title('Boswell Quotient Component Breakdown (Aggregate)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Weighted Component Score (0-100 total)', fontsize=12)
    ax.set_xlim(0, 100)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.legend(loc='upper right')
    
    # Background styling
    ax.set_facecolor('#f8f9fa')
    fig.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    
    # Save component breakdown chart
    plt.savefig(f"{charts_dir}/aggregate_component_breakdown.png", dpi=300)
    plt.close()
    
    # Domain comparison chart
    domains = aggregated_data.get("domains_analyzed", [])
    if len(domains) > 1 and len(sorted_models) > 0:
        
        # Take top 5 models or fewer if less available
        top_models = sorted_models[:min(5, len(sorted_models))]
        
        plt.figure(figsize=(14, 8))
        
        # Define a vibrant color palette
        color_palette = [
            '#FF6B6B',  # Coral Red
            '#4ECDC4',  # Turquoise
            '#FFD166',  # Yellow
            '#6A0572',  # Purple
            '#1A535C',  # Dark Teal
        ]
        
        # Set up bar positions
        bar_width = 0.15
        positions = np.arange(len(domains))
        
        # Plot bars for each model with vibrant colors
        for i, model in enumerate(top_models):
            domain_scores = [aggregated_data["model_scores"][model]["domain_scores"].get(d, 0) for d in domains]
            plt.bar(
                positions + i*bar_width, 
                domain_scores, 
                bar_width, 
                label=model,
                color=color_palette[i % len(color_palette)],
                edgecolor='white',
                linewidth=0.7
            )
            
            # Add score values on top of each bar
            for j, score in enumerate(domain_scores):
                plt.text(
                    positions[j] + i*bar_width, 
                    score + 2, 
                    f'{score:.1f}', 
                    ha='center', 
                    va='bottom', 
                    fontsize=8, 
                    rotation=90,
                    fontweight='bold'
                )
        
        # Configure chart with enhanced styling
        plt.title('Boswell Quotient Comparison Across Domains (Top Models)', fontsize=16, fontweight='bold')
        plt.xlabel('Domain', fontsize=12, fontweight='bold')
        plt.ylabel('Boswell Quotient', fontsize=12, fontweight='bold')
        plt.xticks(positions + bar_width * (len(top_models)-1)/2, domains, rotation=45, ha='right')
        plt.ylim(0, 110)  # Increased to accommodate score labels
        
        # Add a styled legend
        legend = plt.legend(
            title='Models', 
            title_fontsize=12,
            loc='upper right', 
            frameon=True, 
            framealpha=0.95,
            edgecolor='gray'
        )
        
        # Add background styling
        ax = plt.gca()
        ax.set_facecolor('#f8f9fa')  # Light background
        plt.gcf().set_facecolor('#f8f9fa')
        
        # Add a grid for better readability
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        # Save chart
        plt.savefig(f"{charts_dir}/domain_comparison.png", dpi=300)
        plt.close()