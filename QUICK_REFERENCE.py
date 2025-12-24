#!/usr/bin/env python3
"""
Quick Reference - Startup Simulation Commands
Print this and keep nearby!
"""

QUICK_REFERENCE = """
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                    QUICK REFERENCE CARD                                 ║
║                  Startup Simulation Commands                             ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝


█ GETTING STARTED
═══════════════════════════════════════════════════════════════════════════

FIRST TIME SETUP:
  1. Install dependencies:
     pip install -r requirements.txt

  2. Run launcher:
     python launcher.py

  3. Select option 1 to configure policies

  4. Save configuration

  5. Select option 2 to run simulation


█ MAIN COMMANDS
═══════════════════════════════════════════════════════════════════════════

INTERACTIVE LAUNCHER (Recommended):
  python launcher.py
  
  Then select:
    1 = Configure policies (opens GUI)
    2 = Run simulation
    3 = View results
    4 = Exit


CONFIGURATION GUI ONLY:
  python policy_gui.py
  
  Modify parameters → Save → Close


RUN SIMULATION ONLY:
  python run_simulation.py
  
  Automatically loads policy_config.json if available


VIEW USER GUIDE:
  python USER_GUIDE.py
  
  Detailed guide for all features


█ QUICK TWEAKS WITHOUT GUI
═══════════════════════════════════════════════════════════════════════════

Edit config.py directly for quick changes:

  # Tax policy
  TAU = 0.05  # 5% instead of 18%

  # Funding policy
  ALPHA_REVENUE_BURN = 0.5  # Stricter investors
  KAPPA = 0.2  # Smaller funding amounts

  # Market size
  M0_INITIAL = 50000000  # Larger market

Then save and run: python run_simulation.py


█ FILE REFERENCE
═══════════════════════════════════════════════════════════════════════════

CONFIGURATION:
  config.py ..................... Default parameters
  policy_config.json ............ Saved user configuration

SOURCE CODE:
  launcher.py ................... Main menu interface
  policy_gui.py ................. GUI for parameter editing
  startup_agent.py .............. Startup agent class
  startup_model.py .............. Mesa model and scheduler
  run_simulation.py ............. Simulation execution
  analysis.py ................... Results analysis and plotting

DOCUMENTATION:
  README.md ..................... Main documentation
  USER_GUIDE.py ................. Detailed user guide


█ OUTPUT FILES
═══════════════════════════════════════════════════════════════════════════

All results saved to: results/ directory

REPORTS:
  summary_report.txt ............ Statistical summary
  model_dynamics.png ............ Time series plots
  survival_analysis.png ......... Failure distributions
  valuation_distribution.png .... Final valuations

DATA:
  model_timeseries.csv .......... Monthly aggregated data
  agent_data.csv ................ Per-agent detailed data
  monte_carlo_summary.csv ....... Cross-run statistics


█ TYPICAL WORKFLOW
═══════════════════════════════════════════════════════════════════════════

WORKFLOW 1: POLICY COMPARISON
──────────────────────────────
  Step 1: python launcher.py → 1 (Configure)
  Step 2: Adjust TAU = 0.05 (low tax)
  Step 3: Save as policy_config.json
  Step 4: python launcher.py → 2 (Run 10 times)
  Step 5: Note failure_rate from summary_report.txt
  Step 6: Repeat with TAU = 0.25 (high tax)
  Step 7: Compare results


WORKFLOW 2: MARKET ANALYSIS
───────────────────────────
  Step 1: python policy_gui.py
  Step 2: Set M0_INITIAL = 10M (small market)
  Step 3: Save → Run simulation (20 runs)
  Step 4: Note avg_valuation
  Step 5: Change M0_INITIAL = 100M (large market)
  Step 6: Save → Run simulation (20 runs)
  Step 7: Compare valuations


WORKFLOW 3: QUICK TEST
──────────────────────
  Step 1: python run_simulation.py
  Step 2: Enter: 2 (for 2 runs)
  Step 3: Wait ~2 seconds
  Step 4: Check results/summary_report.txt


█ PARAMETER QUICK EDIT
═══════════════════════════════════════════════════════════════════════════

Most impactful parameters to adjust:

REDUCE FAILURE RATE:
  ↑ M0_INITIAL = 50000000
  ↑ GROWTH_RATE_M = 0.10
  ↓ TAU = 0.05
  ↓ C_REG = 10000
  ↑ S_G = 100000

INCREASE INVESTOR FUNDING:
  ↓ ALPHA_REVENUE_BURN = 0.1
  ↓ PMF_MIN = 0.2
  ↑ KAPPA = 0.5

INCREASE REVENUE:
  ↑ GAMMA = 5 (faster adoption)
  ↑ Q_T = 20 (more sales per customer)
  ↑ M0_INITIAL = 100000000 (bigger market)

STABILIZE (REDUCE VOLATILITY):
  ↓ P_SHOCK = 0.01
  ↓ SIGMA_R = 5000
  ↓ SIGMA_PMF = 0.01


█ TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════

"GUI won't open":
  pip install tk

"ModuleNotFoundError: No module named 'mesa'":
  pip install -r requirements.txt

"All startups died in month 11":
  Your parameters are too harsh!
  Run policy_gui.py and:
  • Increase M0_INITIAL
  • Decrease B0_MAX_RATIO
  • Decrease TAU

"Simulation takes too long":
  Reduce NUM_STARTUPS in config.py
  Or use fewer Monte Carlo runs

"Cannot find results":
  Check results/ directory in same folder as script


█ PARAMETER UNITS CHEAT SHEET
═══════════════════════════════════════════════════════════════════════════

MONEY:
  ₹20 Lakhs = 2 million rupees
  ₹2 Crores = 20 million rupees
  ₹10 Crores = 100 million rupees

RATIOS & PERCENTAGES:
  0.05 = 5%
  0.18 = 18%
  1.0 = 100%

TIME:
  1 = 1 month
  60 = 5 years


═══════════════════════════════════════════════════════════════════════════
Last Updated: 2025
For more details: python USER_GUIDE.py
"""

if __name__ == "__main__":
    import sys
    import io
    # Force UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(QUICK_REFERENCE)
