"""
Analysis and visualization of simulation results.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import config


def analyze_single_run(model):
    """Analyze results from a single model run"""
    
    results = {
        'total_startups': len(model.schedule.agents),
        'alive_startups': sum(1 for a in model.schedule.agents if a.S == 1),
        'dead_startups': sum(1 for a in model.schedule.agents if a.S == 0),
        'failure_rate': sum(1 for a in model.schedule.agents if a.S == 0) / len(model.schedule.agents),
        'success_count': model.get_success_count(),
        'top_10_percent_count': model.get_top_10_percent_count(),
        'survival_times': model.get_survival_times(),
    }
    
    # Get alive startups data
    alive_agents = [a for a in model.schedule.agents if a.S == 1]
    if alive_agents:
        results['avg_valuation'] = np.mean([a.V for a in alive_agents])
        results['median_valuation'] = np.median([a.V for a in alive_agents])
        results['avg_pmf'] = np.mean([a.PMF for a in alive_agents])
        results['avg_revenue'] = np.mean([a.R for a in alive_agents])
        results['total_funding'] = sum(getattr(a, 'funding_received', 0) for a in alive_agents)
    else:
        results['avg_valuation'] = 0
        results['median_valuation'] = 0
        results['avg_pmf'] = 0
        results['avg_revenue'] = 0
        results['total_funding'] = 0
    
    return results


def analyze_multiple_runs(models):
    """Analyze results from multiple Monte Carlo runs"""
    
    all_results = [analyze_single_run(model) for model in models]
    
    summary = {
        'mean_failure_rate': np.mean([r['failure_rate'] for r in all_results]),
        'std_failure_rate': np.std([r['failure_rate'] for r in all_results]),
        'mean_success_count': np.mean([r['success_count'] for r in all_results]),
        'std_success_count': np.std([r['success_count'] for r in all_results]),
        'mean_avg_valuation': np.mean([r['avg_valuation'] for r in all_results]),
        'std_avg_valuation': np.std([r['avg_valuation'] for r in all_results]),
        'all_survival_times': [t for r in all_results for t in r['survival_times']],
    }
    
    return summary, all_results


def plot_model_dynamics(model, save_path='results'):
    """Plot time series of model-level variables"""
    
    Path(save_path).mkdir(exist_ok=True)
    
    model_data = model.get_model_data()
    
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    fig.suptitle('Startup Ecosystem Dynamics Over Time', fontsize=16, fontweight='bold')
    
    # Plot 1: Alive vs Dead Startups
    axes[0, 0].plot(model_data.index, model_data['Alive_Startups'], label='Alive', color='green', linewidth=2)
    axes[0, 0].plot(model_data.index, model_data['Dead_Startups'], label='Dead', color='red', linewidth=2)
    axes[0, 0].set_xlabel('Month')
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].set_title('Startup Survival Over Time')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Failure Rate
    axes[0, 1].plot(model_data.index, model_data['Failure_Rate'], color='darkred', linewidth=2)
    axes[0, 1].set_xlabel('Month')
    axes[0, 1].set_ylabel('Failure Rate')
    axes[0, 1].set_title('Cumulative Failure Rate')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Average Valuation
    axes[1, 0].plot(model_data.index, model_data['Avg_Valuation'] / 1e7, color='blue', linewidth=2)
    axes[1, 0].set_xlabel('Month')
    axes[1, 0].set_ylabel('Avg Valuation (Crores)')
    axes[1, 0].set_title('Average Valuation of Alive Startups')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Average PMF
    axes[1, 1].plot(model_data.index, model_data['Avg_PMF'], color='purple', linewidth=2)
    axes[1, 1].set_xlabel('Month')
    axes[1, 1].set_ylabel('Avg PMF')
    axes[1, 1].set_title('Average Product-Market Fit')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Plot 5: Market Size
    axes[2, 0].plot(model_data.index, model_data['Market_Size'] / 1e7, color='orange', linewidth=2)
    axes[2, 0].set_xlabel('Month')
    axes[2, 0].set_ylabel('Market Size (10M units)')
    axes[2, 0].set_title('Market Size Growth')
    axes[2, 0].grid(True, alpha=0.3)
    
    # Plot 6: Competition Index
    axes[2, 1].plot(model_data.index, model_data['Competition_Index'], color='brown', linewidth=2)
    axes[2, 1].set_xlabel('Month')
    axes[2, 1].set_ylabel('Competition Index (θ)')
    axes[2, 1].set_title('Competition Index Over Time')
    axes[2, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}/model_dynamics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Model dynamics plot saved to {save_path}/model_dynamics.png")


def plot_survival_analysis(models, save_path='results'):
    """Plot survival time distribution"""
    
    Path(save_path).mkdir(exist_ok=True)
    
    # Collect all survival times
    all_survival_times = []
    for model in models:
        all_survival_times.extend(model.get_survival_times())
    
    if not all_survival_times:
        print("No deaths recorded - cannot plot survival distribution")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Startup Survival Analysis', fontsize=16, fontweight='bold')
    
    # Histogram of survival times
    axes[0].hist(all_survival_times, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Survival Time (months)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Distribution of Survival Times (Failed Startups)')
    axes[0].grid(True, alpha=0.3)
    
    # Cumulative distribution
    sorted_times = np.sort(all_survival_times)
    cumulative = np.arange(1, len(sorted_times) + 1) / len(sorted_times)
    axes[1].plot(sorted_times, cumulative, color='darkred', linewidth=2)
    axes[1].set_xlabel('Survival Time (months)')
    axes[1].set_ylabel('Cumulative Probability')
    axes[1].set_title('Cumulative Distribution of Failure Times')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}/survival_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Survival analysis plot saved to {save_path}/survival_analysis.png")


def plot_valuation_distribution(models, save_path='results'):
    """Plot final valuation distribution"""
    
    Path(save_path).mkdir(exist_ok=True)
    
    # Collect final valuations of alive startups
    all_valuations = []
    for model in models:
        alive_agents = [a for a in model.schedule.agents if a.S == 1]
        all_valuations.extend([a.V / 1e7 for a in alive_agents])  # Convert to Crores
    
    if not all_valuations:
        print("No surviving startups - cannot plot valuation distribution")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Final Valuation Distribution (Alive Startups)', fontsize=16, fontweight='bold')
    
    # Histogram
    axes[0].hist(all_valuations, bins=50, color='green', edgecolor='black', alpha=0.7)
    axes[0].axvline(config.V_EXIT / 1e7, color='red', linestyle='--', linewidth=2, label=f'Success Threshold ({config.V_EXIT/1e7:.0f} Cr)')
    axes[0].set_xlabel('Valuation (Crores)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Valuation Distribution')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Box plot
    axes[1].boxplot(all_valuations, vert=True)
    axes[1].axhline(config.V_EXIT / 1e7, color='red', linestyle='--', linewidth=2, label='Success Threshold')
    axes[1].set_ylabel('Valuation (Crores)')
    axes[1].set_title('Valuation Box Plot')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_path}/valuation_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Valuation distribution plot saved to {save_path}/valuation_distribution.png")


def generate_summary_report(models, save_path='results'):
    """Generate a comprehensive summary report"""
    
    Path(save_path).mkdir(exist_ok=True)
    
    summary, all_results = analyze_multiple_runs(models)
    
    report = f"""
STARTUP FUNDING DYNAMICS - SIMULATION SUMMARY REPORT
{'='*70}

SIMULATION PARAMETERS
{'='*70}
Number of Startups: {config.NUM_STARTUPS}
Time Horizon: {config.TIME_HORIZON} months
Number of Monte Carlo Runs: {len(models)}
Random Seed: {config.RANDOM_SEED}

AGGREGATE RESULTS
{'='*70}
Mean Failure Rate: {summary['mean_failure_rate']:.2%} ± {summary['std_failure_rate']:.2%}
Mean Success Count: {summary['mean_success_count']:.1f} ± {summary['std_success_count']:.1f}
Success Rate: {summary['mean_success_count']/config.NUM_STARTUPS:.2%}

Mean Average Valuation: ₹{summary['mean_avg_valuation']/1e7:.2f} Cr ± ₹{summary['std_avg_valuation']/1e7:.2f} Cr

SURVIVAL ANALYSIS
{'='*70}
Total Failed Startups (all runs): {len(summary['all_survival_times'])}
"""
    
    if summary['all_survival_times']:
        report += f"""Mean Survival Time: {np.mean(summary['all_survival_times']):.1f} months
Median Survival Time: {np.median(summary['all_survival_times']):.1f} months
Std Dev Survival Time: {np.std(summary['all_survival_times']):.1f} months
"""
    
    report += f"""
DISTRIBUTION STATISTICS (ACROSS RUNS)
{'='*70}
Failure Rate Range: [{min(r['failure_rate'] for r in all_results):.2%}, {max(r['failure_rate'] for r in all_results):.2%}]
Success Count Range: [{min(r['success_count'] for r in all_results)}, {max(r['success_count'] for r in all_results)}]

MODEL PARAMETERS USED
{'='*70}
Initial Capital Range: ₹{config.K0_MIN/1e5:.0f}L - ₹{config.K0_MAX/1e7:.0f}Cr
Burn Rate: {config.B0_MIN_RATIO:.1%} - {config.B0_MAX_RATIO:.1%} of initial capital
PMF Distribution: Beta({config.PMF_ALPHA}, {config.PMF_BETA})
Funding Interval: {config.FUNDING_INTERVAL} months
Policy Interval: {config.POLICY_INTERVAL} months
Shock Probability: {config.P_SHOCK:.1%} per month
Success Threshold: ₹{config.V_EXIT/1e7:.0f} Cr valuation

{'='*70}
Report generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Save report
    with open(f'{save_path}/summary_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\nFull report saved to {save_path}/summary_report.txt")
    
    return summary, all_results


def export_data(models, save_path='results'):
    """Export detailed data to CSV files"""
    
    Path(save_path).mkdir(exist_ok=True)
    
    # Export model-level data from first run
    model_data = models[0].get_model_data()
    model_data.to_csv(f'{save_path}/model_timeseries.csv')
    print(f"Model time series data exported to {save_path}/model_timeseries.csv")
    
    # Export agent-level data from first run
    agent_data = models[0].get_agent_data()
    agent_data.to_csv(f'{save_path}/agent_data.csv')
    print(f"Agent data exported to {save_path}/agent_data.csv")
    
    # Export summary statistics across all runs
    all_results = [analyze_single_run(model) for model in models]
    
    summary_df = pd.DataFrame({
        'run': range(len(all_results)),
        'failure_rate': [r['failure_rate'] for r in all_results],
        'success_count': [r['success_count'] for r in all_results],
        'alive_startups': [r['alive_startups'] for r in all_results],
        'avg_valuation': [r['avg_valuation'] for r in all_results],
        'avg_pmf': [r['avg_pmf'] for r in all_results],
        'avg_revenue': [r['avg_revenue'] for r in all_results],
    })
    
    summary_df.to_csv(f'{save_path}/monte_carlo_summary.csv', index=False)
    print(f"Monte Carlo summary exported to {save_path}/monte_carlo_summary.csv")
