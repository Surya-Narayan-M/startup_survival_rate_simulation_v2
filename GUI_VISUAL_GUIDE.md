# GUI Visual Guide - Startup Policy Configuration

## 🖥️ GUI Interface Overview

When you run `python launcher.py` and select "1" to configure policies, the following window opens:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Startup Funding Dynamics - Policy Configuration                       │
│                                                                         │
│  [Initial Conditions] [Consumer...] [Investor...] [Market...] [...]    │
│  ═════════════════════════════════════════════════════════════════     │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ K0_MIN (Min Initial Capital)         [2000000    ]    ₹        │   │
│  │                                                                 │   │
│  │ K0_MAX (Max Initial Capital)         [200000000  ]    ₹        │   │
│  │                                                                 │   │
│  │ B0 Min Ratio                         [0.05       ]    %        │   │
│  │                                                                 │   │
│  │ B0 Max Ratio                         [0.15       ]    %        │   │
│  │                                                                 │   │
│  │ PMF Distribution Alpha               [2          ]             │   │
│  │                                                                 │   │
│  │ PMF Distribution Beta                [5          ]             │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  [Save Configuration] [Load Saved Config] [Reset to Defaults]          │
│                                         [Run Simulation →]             │
└─────────────────────────────────────────────────────────────────────────┘
```

## 📑 Tab Structure

### Tab 1: Initial Conditions
```
Parameters:
  • K0_MIN: Minimum startup capital
  • K0_MAX: Maximum startup capital
  • B0_MIN_RATIO: Minimum burn rate
  • B0_MAX_RATIO: Maximum burn rate
  • PMF_ALPHA: Product-market fit (Alpha)
  • PMF_BETA: Product-market fit (Beta)
```

### Tab 2: Consumer Adoption
```
Parameters:
  • GAMMA: Adoption curve steepness
  • EPSILON_PRICE: Price sensitivity
  • BASE_PRICE: Base product price
  • SIGMA_R: Revenue noise
  • Q_T: Quantity per customer
```

### Tab 3: Investor Logic
```
Parameters:
  • ALPHA_REVENUE_BURN: Min revenue/burn ratio
  • PMF_MIN: Min PMF for funding
  • BETA_1: PMF coefficient
  • BETA_2: Revenue coefficient
  • BETA_3: Competition coefficient
  • KAPPA: Funding amount multiplier
```

### Tab 4: Market Dynamics
```
Parameters:
  • M0_INITIAL: Initial market size
  • GROWTH_RATE_M: Market growth rate
  • DELTA_GROWTH: Burn rate increase after funding
  • DELTA_CUT: Burn rate decrease when low runway
  • RUNWAY_LOW_THRESHOLD: Low runway limit
```

### Tab 5: Policy & Tax
```
Parameters:
  • C_REG: Regulatory compliance cost
  • S_G: Government subsidy
  • TAU: Tax rate
  • SIGMA_PMF: PMF noise
  • ETA: PMF learning rate
```

### Tab 6: External Shocks
```
Parameters:
  • P_SHOCK: Monthly shock probability
  • DELTA_PMF_SHOCK_MIN: Min PMF shock
  • DELTA_PMF_SHOCK_MAX: Max PMF shock
  • DELTA_M_SHOCK_MIN: Min market shock
  • DELTA_M_SHOCK_MAX: Max market shock
```

### Tab 7: Simulation
```
Parameters:
  • NUM_STARTUPS: Number of startup agents
  • TIME_HORIZON: Simulation duration (months)
  • V_EXIT: Success valuation threshold
  • LAMBDA_1: Revenue weight in valuation
  • LAMBDA_2: PMF weight in valuation
  • LAMBDA_3: Capital weight in valuation
```

## 🎯 How to Modify Parameters

Each parameter row has:
```
┌─────────────────────────────────────────────────────────────┐
│ Parameter Name         │ [Input Field] │ Unit Label        │
└─────────────────────────────────────────────────────────────┘
```

### Steps to Change a Parameter:
1. Click on the input field (e.g., `[2000000]`)
2. Clear the current value
3. Type your new value
4. Press Tab or click another field (validates immediately)
5. Click "Save Configuration" to save all changes

## 💾 Button Actions

### Save Configuration
- Saves all current values to `policy_config.json`
- Shows confirmation: "Configuration saved to policy_config.json"
- File can be shared with others

### Load Saved Config
- Loads previously saved `policy_config.json`
- Populates all fields with saved values
- Shows confirmation or warning if no file exists

### Reset to Defaults
- Restores all fields to original default values
- Confirmation: "Configuration reset to defaults"
- Useful if you make mistakes

### Run Simulation →
- Saves current configuration
- Closes GUI
- Automatically starts simulation
- Shows message: "Configuration applied! Run: python run_simulation.py"

## 🔍 Example: Changing Tax Rate

Let's say you want to reduce the tax rate from 18% to 5%:

1. **Open Policy Tab**
   ```
   python launcher.py → Select "1" → Click "Policy & Tax" tab
   ```

2. **Find TAU Parameter**
   ```
   Scroll to find: "Tax Rate (τ)" with value [0.18]
   ```

3. **Modify Value**
   ```
   Click on [0.18]
   Delete the text
   Type: 0.05
   ```

4. **Save Configuration**
   ```
   Click "Save Configuration" button
   Confirm: "Configuration saved to policy_config.json"
   ```

5. **Run Simulation**
   ```
   Click "Run Simulation →"
   Enter number of Monte Carlo runs (e.g., 20)
   Results saved to results/ folder
   ```

## 📊 Example Workflow

```
START: python launcher.py
│
├─→ OPTION 1: CONFIGURE POLICIES
│   │
│   ├─→ GUI Opens with 7 tabs
│   │
│   ├─→ Go to "Policy & Tax" tab
│   │
│   ├─→ Change TAU from 0.18 to 0.05
│   │
│   ├─→ Go to "Market Dynamics" tab
│   │
│   ├─→ Change M0_INITIAL from 10M to 50M
│   │
│   ├─→ Click "Save Configuration"
│   │   └─→ File: policy_config.json (created)
│   │
│   └─→ Close GUI
│
├─→ OPTION 2: RUN SIMULATION
│   │
│   ├─→ Loads policy_config.json ✓
│   │
│   ├─→ Initializes 1000 startups
│   │
│   ├─→ Runs 60 months × 20 Monte Carlo runs
│   │
│   ├─→ Generates analysis
│   │
│   └─→ Results:
│       ├─→ summary_report.txt
│       ├─→ model_dynamics.png
│       ├─→ model_timeseries.csv
│       └─→ monte_carlo_summary.csv
│
├─→ OPTION 3: VIEW RESULTS
│   │
│   └─→ Opens results/ folder in file explorer
│
└─→ OPTION 4: EXIT
    └─→ Program closes
```

## 🎨 Color & Layout Notes

- **Tabbed Interface**: Easy navigation between categories
- **Scrollable Frames**: Can scroll if parameters don't fit
- **Input Validation**: Numbers only, automatic validation
- **Label-Entry-Unit Layout**: Clear parameter identification
- **UTF-8 Support**: Currency symbols (₹) display correctly
- **Light/Dark Mode**: Follows OS settings

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Next Field | Tab |
| Previous Field | Shift+Tab |
| Save (Manual) | Ctrl+S (on Windows) |
| Quit GUI | Alt+F4 or Escape |

## 🔄 Configuration File Format

When you save, `policy_config.json` looks like:
```json
{
    "K0_MIN": 2000000,
    "K0_MAX": 200000000,
    "B0_MIN_RATIO": 0.05,
    "B0_MAX_RATIO": 0.15,
    "PMF_ALPHA": 2,
    "PMF_BETA": 5,
    "GAMMA": 2,
    "EPSILON_PRICE": 0.01,
    "BASE_PRICE": 100,
    "SIGMA_R": 10000,
    "Q_T": 10,
    ...
}
```

You can:
- ✓ Edit this file manually in any text editor
- ✓ Share with colleagues
- ✓ Keep different versions for scenarios
- ✓ Use version control (git)

## 📱 Mobile-Friendly Layout

Although the GUI is desktop-based, it's optimized for:
- ✓ Various window sizes
- ✓ Different screen resolutions
- ✓ Horizontal scrolling if needed
- ✓ Accessible keyboard navigation

## 🎓 Tips for New Users

1. **Start with Default Values**
   - Don't change everything at once
   - Change one parameter at a time
   - Run simulations to see impact

2. **Use the Guides**
   - `python USER_GUIDE.py` explains each parameter
   - `python QUICK_REFERENCE.py` for commands
   - README.md for full documentation

3. **Save Your Work**
   - Always click "Save Configuration" before closing
   - Rename saved configs for different scenarios
   - Keep backups of important configurations

4. **Compare Results**
   - Run 2 simulations with different configs
   - Look at monte_carlo_summary.csv
   - Compare key metrics (failure_rate, avg_valuation)

---

**That's it!** You now understand the GUI interface completely. 🎉

Start with: `python launcher.py`
