"""
USER GUIDE - Startup Funding Dynamics Simulation
"""

GUI_TUTORIAL = """
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                    STARTUP SIMULATION - USER GUIDE                       ║
║                                                                          ║
║              How to Configure Policies and Run Simulations               ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝


█ TABLE OF CONTENTS
═══════════════════════════════════════════════════════════════════════════

1. Quick Start
2. Using the Launcher
3. Configuring Policies with the GUI
4. Parameter Guide
5. Running Simulations
6. Interpreting Results
7. Advanced Scenarios


█ 1. QUICK START
═══════════════════════════════════════════════════════════════════════════

First-time users should run the Launcher:

    python launcher.py

This gives you a menu interface with 4 options:
    1. Configure Policies (GUI)
    2. Run Simulation
    3. View Last Results
    4. Exit


█ 2. USING THE LAUNCHER
═══════════════════════════════════════════════════════════════════════════

The Launcher Menu:

Option 1: CONFIGURE POLICIES & PARAMETERS
─────────────────────────────────────────
Opens a graphical interface to customize all simulation parameters.

Why use this?
  • User-friendly interface with organized tabs
  • No need to edit config files manually
  • Save/load multiple configurations
  • See all parameters with units and descriptions
  
Steps:
  1. Run "python launcher.py"
  2. Select "1" (Configure Policies)
  3. GUI window opens with 7 tabs
  4. Modify parameters as needed
  5. Click "Save Configuration" to save
  6. Close GUI and run simulation


Option 2: RUN SIMULATION
────────────────────────
Executes the Monte Carlo simulation.

Configuration Priority:
  1. First checks for policy_config.json (saved configuration)
  2. If found, uses those values
  3. If not found, uses defaults from config.py

Steps:
  1. Run "python launcher.py"
  2. Select "2" (Run Simulation)
  3. Enter number of Monte Carlo runs (default: 10)
  4. Simulation runs and generates results
  5. Results saved to 'results/' directory


Option 3: VIEW LAST RESULTS
───────────────────────────
Opens the results directory in file explorer.

Contents of results folder:
  • summary_report.txt - Statistical summary
  • model_dynamics.png - Time series graphs
  • survival_analysis.png - Failure distributions
  • valuation_distribution.png - Final valuations
  • model_timeseries.csv - Monthly data
  • agent_data.csv - Per-agent detailed data
  • monte_carlo_summary.csv - Cross-run statistics


Option 4: EXIT
──────────────
Closes the launcher.


█ 3. CONFIGURING POLICIES WITH THE GUI
═══════════════════════════════════════════════════════════════════════════

GUI Tabs and Parameters:

┌─────────────────────────────────────────────────────────────────────┐
│ TAB 1: INITIAL CONDITIONS                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Parameter              │ Default         │ Meaning                  │
├───────────────────────┼─────────────────┼──────────────────────────┤
│ K0_MIN                │ ₹20 Lakhs       │ Min starting capital     │
│ K0_MAX                │ ₹2 Crores       │ Max starting capital     │
│ B0_MIN_RATIO          │ 5%              │ Min burn rate (% of K0)  │
│ B0_MAX_RATIO          │ 15%             │ Max burn rate (% of K0)  │
│ PMF_ALPHA             │ 2               │ Beta distribution α      │
│ PMF_BETA              │ 5               │ Beta distribution β      │
└───────────────────────┴─────────────────┴──────────────────────────┘

Why adjust these?
  • Change K0_MIN/MAX to test different startup funding levels
  • Adjust B0 ratios to model different spending habits
  • Change PMF distribution to modify initial product-market fit


┌─────────────────────────────────────────────────────────────────────┐
│ TAB 2: CONSUMER ADOPTION                                            │
├─────────────────────────────────────────────────────────────────────┤
│ Parameter              │ Default         │ Meaning                  │
├───────────────────────┼─────────────────┼──────────────────────────┤
│ GAMMA                 │ 2               │ Adoption curve steepness │
│ EPSILON_PRICE         │ 0.01            │ Price sensitivity        │
│ BASE_PRICE            │ ₹100            │ Product price            │
│ SIGMA_R               │ ₹10,000         │ Revenue volatility       │
│ Q_T                   │ 10 units        │ Quantity per customer    │
└───────────────────────┴─────────────────┴──────────────────────────┘

Why adjust these?
  • Lower GAMMA = more gradual adoption (slow growth)
  • Higher GAMMA = faster adoption (hockey stick curve)
  • Increase Q_T to model higher sales volumes
  • Adjust SIGMA_R to increase/decrease revenue variability


┌─────────────────────────────────────────────────────────────────────┐
│ TAB 3: INVESTOR LOGIC                                               │
├─────────────────────────────────────────────────────────────────────┤
│ Parameter              │ Default         │ Meaning                  │
├───────────────────────┼─────────────────┼──────────────────────────┤
│ ALPHA_REVENUE_BURN    │ 0.3             │ Min revenue/burn ratio   │
│ PMF_MIN               │ 0.3             │ Min PMF for funding      │
│ BETA_1                │ 5.0             │ PMF coefficient          │
│ BETA_2                │ 0.5             │ Revenue coefficient      │
│ BETA_3                │ 2.0             │ Competition coefficient  │
│ KAPPA                 │ 0.25            │ Funding amount (% of V)  │
└───────────────────────┴─────────────────┴──────────────────────────┘

Why adjust these?
  • Stricter funding = higher ALPHA_REVENUE_BURN, PMF_MIN
  • More generous funding = increase KAPPA
  • Make revenue more important = increase BETA_2


┌─────────────────────────────────────────────────────────────────────┐
│ TAB 4: MARKET DYNAMICS                                              │
├─────────────────────────────────────────────────────────────────────┤
│ Parameter              │ Default         │ Meaning                  │
├───────────────────────┼─────────────────┼──────────────────────────┤
│ M0_INITIAL            │ 10 Crores       │ Initial market size      │
│ GROWTH_RATE_M         │ 5%              │ Monthly market growth    │
│ DELTA_GROWTH          │ 20%             │ Burn ↑ after funding     │
│ DELTA_CUT             │ 15%             │ Burn ↓ if low runway     │
│ RUNWAY_LOW_THRESHOLD  │ 3 months        │ Runway limit             │
└───────────────────────┴─────────────────┴──────────────────────────┘

Why adjust these?
  • Increase M0_INITIAL for larger total addressable market
  • Lower GROWTH_RATE_M for mature markets
  • Higher DELTA_GROWTH to penalize spending after funding


┌─────────────────────────────────────────────────────────────────────┐
│ TAB 5: POLICY & TAX                                                 │
├─────────────────────────────────────────────────────────────────────┤
│ Parameter              │ Default         │ Meaning                  │
├───────────────────────┼─────────────────┼──────────────────────────┤
│ C_REG                 │ ₹50,000         │ Regulatory compliance    │
│ S_G                   │ ₹30,000         │ Government subsidy       │
│ TAU                   │ 18%             │ Tax rate on revenue      │
│ SIGMA_PMF             │ 0.02            │ PMF noise std dev        │
│ ETA                   │ 0.01            │ PMF learning rate        │
└───────────────────────┴─────────────────┴──────────────────────────┘

Why adjust these?
  • Simulate tax policy changes by adjusting TAU
  • Increase C_REG to model regulatory burden
  • Higher S_G to model government support


┌─────────────────────────────────────────────────────────────────────┐
│ TAB 6: EXTERNAL SHOCKS                                              │
├─────────────────────────────────────────────────────────────────────┤
│ Parameter              │ Default         │ Meaning                  │
├───────────────────────┼─────────────────┼──────────────────────────┤
│ P_SHOCK               │ 5%              │ Monthly shock prob       │
│ DELTA_PMF_SHOCK_MIN   │ -10%            │ Min PMF shock            │
│ DELTA_PMF_SHOCK_MAX   │ 15%             │ Max PMF shock            │
│ DELTA_M_SHOCK_MIN     │ -5%             │ Min market shock         │
│ DELTA_M_SHOCK_MAX     │ 10%             │ Max market shock         │
└───────────────────────┴─────────────────┴──────────────────────────┘

Why adjust these?
  • Increase P_SHOCK to model volatile markets
  • Set to 0 for deterministic scenario
  • Larger shock ranges = higher volatility


┌─────────────────────────────────────────────────────────────────────┐
│ TAB 7: SIMULATION                                                   │
├─────────────────────────────────────────────────────────────────────┤
│ Parameter              │ Default         │ Meaning                  │
├───────────────────────┼─────────────────┼──────────────────────────┤
│ NUM_STARTUPS          │ 1000            │ Number of agents         │
│ TIME_HORIZON          │ 60              │ Duration (months)        │
│ V_EXIT                │ ₹10 Crores      │ Success valuation        │
│ LAMBDA_1              │ 10              │ Revenue in valuation     │
│ LAMBDA_2              │ 1 Crore         │ PMF in valuation         │
│ LAMBDA_3              │ 2               │ Capital in valuation     │
└───────────────────────┴─────────────────┴──────────────────────────┘

Why adjust these?
  • Lower NUM_STARTUPS for faster runs
  • Increase TIME_HORIZON to see long-term effects
  • Adjust V_EXIT to change success threshold


█ 4. PARAMETER GUIDE
═══════════════════════════════════════════════════════════════════════════

COMMON ADJUSTMENT SCENARIOS:

Scenario 1: LOW-TAX STARTUP ECOSYSTEM
──────────────────────────────────────
Goal: Model startup-friendly tax policy

Changes:
  • TAU = 0.05 (reduce from 18%)
  • C_REG = 10000 (reduce from 50000)
  • S_G = 100000 (increase from 30000)

Expected Result: Higher survival rates, larger final valuations


Scenario 2: CONSERVATIVE INVESTORS
──────────────────────────────────
Goal: Model risk-averse venture capitalists

Changes:
  • ALPHA_REVENUE_BURN = 0.5 (increase from 0.3)
  • PMF_MIN = 0.5 (increase from 0.3)
  • KAPPA = 0.15 (decrease from 0.25)

Expected Result: Fewer startups get funded, stricter survival


Scenario 3: HIGH-GROWTH MARKET
──────────────────────────────
Goal: Model emerging tech market boom

Changes:
  • M0_INITIAL = 50000000 (increase 5x)
  • GROWTH_RATE_M = 0.10 (increase from 5%)
  • GAMMA = 5 (increase from 2, faster adoption)

Expected Result: Higher revenues, more successful exits


Scenario 4: CRISIS CONDITIONS
──────────────────────────────
Goal: Model recession or market shock

Changes:
  • P_SHOCK = 0.15 (increase from 5%)
  • DELTA_M_SHOCK_MIN = -0.20 (decrease from -5%)
  • DELTA_M_SHOCK_MAX = 0.05 (decrease from 10%)
  • TAU = 0.25 (increase from 18%)

Expected Result: Higher failure rates, shorter lifespans


█ 5. RUNNING SIMULATIONS
═══════════════════════════════════════════════════════════════════════════

After configuring policies:

Step 1: Save Configuration
──────────────────────────
In the GUI, click "Save Configuration"
  ✓ Saves to policy_config.json
  ✓ Automatically loaded when running simulation

Step 2: Run Simulation
──────────────────────
Option A - From Launcher:
  python launcher.py
  → Select "2" (Run Simulation)

Option B - Direct:
  python run_simulation.py

Step 3: Enter Number of Runs
──────────────────────────────
When prompted, enter number of Monte Carlo runs (e.g., 10, 50, 100)
  • More runs = more reliable statistics, longer time
  • 10 runs ≈ 13 seconds
  • 50 runs ≈ 65 seconds
  • 100 runs ≈ 2 minutes


█ 6. INTERPRETING RESULTS
═══════════════════════════════════════════════════════════════════════════

Key Metrics:

FAILURE RATE
────────────
Percentage of startups that run out of capital before month 60
  • 0-10%: Very healthy ecosystem
  • 10-20%: Normal ecosystem
  • 20-50%: Difficult environment
  • 50%+: Harsh conditions


SURVIVAL TIME
─────────────
Average time (in months) before failed startups run out of capital
  • 5-10 months: Quick failures (low initial capital or high burn)
  • 10-20 months: Moderate survival
  • 20+ months: Extended survival (strong revenue or funding)


SUCCESS RATE
────────────
Percentage reaching V_EXIT valuation threshold
  • This depends heavily on your V_EXIT setting
  • Higher V_EXIT = lower success rate


AVERAGE VALUATION
──────────────────
Final valuation of surviving startups
  • Indicates market value creation
  • Directly influenced by revenue success


█ 7. ADVANCED SCENARIOS
═══════════════════════════════════════════════════════════════════════════

POLICY IMPACT ANALYSIS
─────────────────────
Compare two scenarios to measure policy impact:

Example: Impact of reducing TAU from 18% to 5%

Run 1: Default with TAU=18%
  → Save results/scenario1/

Run 2: Change TAU=5%
  → Save results/scenario2/

Compare: 
  monte_carlo_summary.csv from both runs
  Look at: survival_rate, avg_valuation, total_funding


MARKET SENSITIVITY ANALYSIS
──────────────────────────
Test different market sizes:

  M0 = 5M: Small niche market
  M0 = 50M: Standard market
  M0 = 500M: Large market

Run each and compare success rates


INVESTOR BEHAVIOR ANALYSIS
──────────────────────────
Test different funding criteria:

  Scenario A: ALPHA=0.1, PMF=0.1 (generous investors)
  Scenario B: ALPHA=0.5, PMF=0.5 (strict investors)
  Scenario C: ALPHA=1.0, PMF=0.7 (extremely picky)

Observe startup survival and funding patterns


TIMING ANALYSIS
───────────────
Compare different time horizons:

  TIME_HORIZON = 12 (1 year): Quick success/failure
  TIME_HORIZON = 60 (5 years): Long-term viability
  TIME_HORIZON = 120 (10 years): Extended operations

Observe how outcomes change over time


═══════════════════════════════════════════════════════════════════════════
For questions or issues, refer to README.md or examine the source code.
"""


if __name__ == "__main__":
    import sys
    import io
    # Force UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(GUI_TUTORIAL)
