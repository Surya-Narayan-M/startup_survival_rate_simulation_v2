"""
Main script to run the startup funding dynamics simulation.

This script:
1. Creates and runs the Mesa model
2. Executes multiple Monte Carlo runs
3. Collects and analyzes results
4. Generates visualizations and reports
"""

import time
from startup_model import StartupModel
import config
import analysis


def run_single_simulation(run_number=0, seed=None):
    """Run a single simulation"""
    
    print(f"\n{'='*70}")
    print(f"Running Simulation #{run_number + 1}")
    print(f"{'='*70}")
    
    # Create model with seed
    if seed is not None:
        model_seed = seed + run_number
    else:
        model_seed = config.RANDOM_SEED + run_number if config.RANDOM_SEED else None
    
    model = StartupModel(num_startups=config.NUM_STARTUPS, seed=model_seed)
    
    print(f"Initialized {config.NUM_STARTUPS} startups")
    print(f"Running for {config.TIME_HORIZON} months...")
    
    # Run the model
    start_time = time.time()
    model.run_model(steps=config.TIME_HORIZON)
    elapsed_time = time.time() - start_time
    
    # Quick summary
    alive = sum(1 for a in model.schedule.agents if a.S == 1)
    dead = sum(1 for a in model.schedule.agents if a.S == 0)
    success = model.get_success_count()
    
    print(f"\nSimulation completed in {elapsed_time:.2f} seconds")
    print(f"Final Status:")
    print(f"  - Alive: {alive} ({alive/config.NUM_STARTUPS:.1%})")
    print(f"  - Dead: {dead} ({dead/config.NUM_STARTUPS:.1%})")
    print(f"  - Successful (V ≥ {config.V_EXIT/1e7:.0f}Cr): {success} ({success/config.NUM_STARTUPS:.1%})")
    
    return model


def run_monte_carlo(num_runs=10, seed=None):
    """Run multiple Monte Carlo simulations"""
    
    print(f"\n{'#'*70}")
    print(f"MONTE CARLO SIMULATION - {num_runs} RUNS")
    print(f"{'#'*70}")
    
    models = []
    overall_start = time.time()
    
    for i in range(num_runs):
        model = run_single_simulation(run_number=i, seed=seed)
        models.append(model)
    
    overall_elapsed = time.time() - overall_start
    
    print(f"\n{'#'*70}")
    print(f"All {num_runs} simulations completed in {overall_elapsed:.2f} seconds")
    print(f"Average time per run: {overall_elapsed/num_runs:.2f} seconds")
    print(f"{'#'*70}")
    
    return models


def main():
    """Main execution function"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║         STARTUP FUNDING DYNAMICS SIMULATION                      ║
    ║         Agent-Based Model using Mesa Framework                   ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Configuration summary
    print(f"\nCONFIGURATION:")
    print(f"  - Number of Startups: {config.NUM_STARTUPS}")
    print(f"  - Time Horizon: {config.TIME_HORIZON} months")
    print(f"  - Random Seed: {config.RANDOM_SEED}")
    print(f"  - Funding Interval: {config.FUNDING_INTERVAL} months")
    print(f"  - Policy Interval: {config.POLICY_INTERVAL} months")
    print(f"  - Success Threshold: ₹{config.V_EXIT/1e7:.0f} Crores")
    
    # Ask user for number of Monte Carlo runs
    try:
        num_runs = int(input("\nEnter number of Monte Carlo runs (default 10): ") or "10")
    except ValueError:
        num_runs = 10
        print(f"Invalid input. Using default: {num_runs} runs")
    
    # Run simulations
    models = run_monte_carlo(num_runs=num_runs, seed=config.RANDOM_SEED)
    
    # Analysis and visualization
    print(f"\n{'='*70}")
    print("GENERATING ANALYSIS AND VISUALIZATIONS")
    print(f"{'='*70}")
    
    # Generate summary report
    print("\n1. Generating summary report...")
    summary, all_results = analysis.generate_summary_report(models)
    
    # Plot model dynamics (using first run)
    print("\n2. Plotting model dynamics...")
    analysis.plot_model_dynamics(models[0])
    
    # Plot survival analysis
    print("\n3. Plotting survival analysis...")
    analysis.plot_survival_analysis(models)
    
    # Plot valuation distribution
    print("\n4. Plotting valuation distribution...")
    analysis.plot_valuation_distribution(models)
    
    # Export data
    print("\n5. Exporting data to CSV...")
    analysis.export_data(models)
    
    print(f"\n{'='*70}")
    print("SIMULATION COMPLETE!")
    print(f"{'='*70}")
    print("\nAll results saved to 'results/' directory:")
    print("  - summary_report.txt")
    print("  - model_dynamics.png")
    print("  - survival_analysis.png")
    print("  - valuation_distribution.png")
    print("  - model_timeseries.csv")
    print("  - agent_data.csv")
    print("  - monte_carlo_summary.csv")
    print()


if __name__ == "__main__":
    main()
