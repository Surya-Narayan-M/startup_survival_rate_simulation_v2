# 📚 Documentation Index

Complete guide to all documentation and how to use this startup simulation.

## 🎯 Quick Navigation

### **For First-Time Users**
1. **START HERE** → `START_HERE.md`
   - Overview of what's new
   - 3-step quick start guide
   - Common use cases

2. **Visual Guide** → `GUI_VISUAL_GUIDE.md`
   - How the GUI looks
   - Screenshots and layouts
   - Step-by-step examples

### **For Policy Configuration**
1. **GUI Usage** → `USER_GUIDE.py`
   - Detailed parameter explanations
   - Scenario templates
   - Analysis workflows
   - Run: `python USER_GUIDE.py`

2. **Setup Instructions** → `GUI_SETUP_GUIDE.md`
   - Installation steps
   - Feature overview
   - Workflow comparison

### **For Running Simulations**
1. **Command Reference** → `QUICK_REFERENCE.py`
   - All commands at a glance
   - Keyboard shortcuts
   - Troubleshooting
   - Run: `python QUICK_REFERENCE.py`

2. **Full Documentation** → `README.md`
   - Complete technical details
   - Parameter reference
   - Output descriptions

---

## 📁 File Organization

```
DOCUMENTATION:
├── START_HERE.md               ← Read this first!
├── GUI_VISUAL_GUIDE.md         ← See what the GUI looks like
├── GUI_SETUP_GUIDE.md          ← Setup and features overview
├── USER_GUIDE.py               ← Detailed parameter guide
│   └── Run: python USER_GUIDE.py
├── QUICK_REFERENCE.py          ← Command cheat sheet
│   └── Run: python QUICK_REFERENCE.py
├── README.md                   ← Full documentation
└── DOCUMENTATION_INDEX.md      ← This file

EXECUTABLE ENTRY POINTS:
├── launcher.py                 ← Main entry point ⭐
│   └── Run: python launcher.py
├── policy_gui.py              ← GUI configuration tool
│   └── Run: python policy_gui.py
└── run_simulation.py           ← Run simulation directly
    └── Run: python run_simulation.py

CONFIGURATION:
├── config.py                   ← Default parameters
└── policy_config.json         ← Your saved configurations (auto-generated)

SOURCE CODE:
├── startup_agent.py           ← Agent implementation
├── startup_model.py           ← Model and scheduler
└── analysis.py                ← Analysis and visualization

RESULTS:
└── results/                   ← Simulation outputs (auto-generated)
    ├── summary_report.txt
    ├── model_dynamics.png
    ├── model_timeseries.csv
    └── ...
```

---

## 🚀 Getting Started Paths

### Path 1: Complete Beginner
```
1. Open START_HERE.md
2. Run: python launcher.py
3. Select option 1 (Configure)
4. Browse GUI_VISUAL_GUIDE.md for help
5. Save configuration
6. Run simulation
7. Check results/
```

### Path 2: Quick Test
```
1. Run: python launcher.py
2. Select option 2 (Run with defaults)
3. Enter: 5 (for 5 Monte Carlo runs)
4. View results in results/ folder
```

### Path 3: Policy Analysis
```
1. Run: python USER_GUIDE.py (read about parameters)
2. Run: python launcher.py
3. Select option 1 (Configure)
4. Change policy parameters
5. Save configuration
6. Run simulation with multiple runs
7. Compare monte_carlo_summary.csv
```

### Path 4: Advanced Scenarios
```
1. Read: GUI_SETUP_GUIDE.md (scenario section)
2. Run: python policy_gui.py
3. Create custom scenarios
4. Run simulations for each
5. Analyze differences
6. Generate presentation
```

---

## 📖 Documentation by Topic

### **How to Configure Policies**
- `START_HERE.md` - Overview
- `GUI_VISUAL_GUIDE.md` - Visual walkthrough
- `USER_GUIDE.py` - Detailed parameter guide
- `policy_gui.py` - The actual GUI

### **How to Run Simulations**
- `QUICK_REFERENCE.py` - Commands
- `README.md` - Full options
- `launcher.py` - Interactive menu
- `run_simulation.py` - Direct execution

### **Understanding Parameters**
- `USER_GUIDE.py` - All parameter explanations
- `config.py` - Default values
- `GUI_SETUP_GUIDE.md` - Impact summaries

### **Analyzing Results**
- `README.md` - Output file descriptions
- `GUI_SETUP_GUIDE.md` - Result interpretation
- `analysis.py` - Visualization code

### **Troubleshooting**
- `QUICK_REFERENCE.py` - Troubleshooting section
- `README.md` - FAQ
- `START_HERE.md` - Common issues

---

## 🎓 Document Purpose

| Document | Purpose | Audience | Read Time |
|----------|---------|----------|-----------|
| **START_HERE.md** | Overview & quick start | Everyone | 5 min |
| **GUI_VISUAL_GUIDE.md** | How GUI looks & works | GUI users | 10 min |
| **USER_GUIDE.py** | Detailed parameters | Policy makers | 30 min |
| **GUI_SETUP_GUIDE.md** | Features overview | Managers | 15 min |
| **QUICK_REFERENCE.py** | Command cheat sheet | Operators | 5 min |
| **README.md** | Complete documentation | Developers | 20 min |

---

## 💡 Common Workflows

### **Workflow 1: Test Tax Policy Impact**
```
Documents to read:
  1. START_HERE.md (quick overview)
  2. USER_GUIDE.py (tax parameter section)

Steps:
  1. Run: python launcher.py
  2. Select "1" (Configure)
  3. Change TAU parameter
  4. Save configuration
  5. Run simulation (select "2")
  6. Compare results
```

### **Workflow 2: Create Custom Scenario**
```
Documents to read:
  1. USER_GUIDE.py (scenario section)
  2. GUI_VISUAL_GUIDE.md (step-by-step)

Steps:
  1. Read scenario examples
  2. Run: python launcher.py → 1
  3. Configure all 7 tabs
  4. Save as unique name
  5. Run simulation
  6. Document findings
```

### **Workflow 3: Compare Multiple Scenarios**
```
Documents to read:
  1. GUI_SETUP_GUIDE.md (scenario section)
  2. README.md (output descriptions)

Steps:
  1. Create scenario A config
  2. Run simulation, save results_A/
  3. Create scenario B config
  4. Run simulation, save results_B/
  5. Compare monte_carlo_summary.csv files
  6. Generate comparison report
```

---

## 🔧 For Different Users

### **Policy Makers / Economists**
- Start with: `USER_GUIDE.py`
- Then: `launcher.py` for configuration
- Look at: `monte_carlo_summary.csv` for analysis

### **Students / Learners**
- Start with: `START_HERE.md`
- Then: `GUI_VISUAL_GUIDE.md`
- Explore: All parameters via GUI
- Read: `USER_GUIDE.py` for details

### **Researchers / Developers**
- Start with: `README.md`
- Study: `startup_agent.py` and `startup_model.py`
- Understand: Formula implementation in source code
- Modify: `config.py` for custom parameters

### **Business Users**
- Start with: `START_HERE.md`
- Use: `launcher.py` for configuration
- Create: Scenarios and compare results
- Generate: Reports from `results/` folder

---

## 📊 Output Understanding

After running simulation, check:

1. **Quick Summary**: `results/summary_report.txt`
   - Failure rates, success counts
   - Valuations and PMF metrics
   - Configuration used

2. **Time Series Data**: `results/model_timeseries.csv`
   - Month-by-month evolution
   - Plot with your preferred tool
   - Identify patterns

3. **Agent Details**: `results/agent_data.csv`
   - Per-startup detailed data
   - Final state of all agents
   - Individual trajectories

4. **Cross-Run Stats**: `results/monte_carlo_summary.csv`
   - Statistics across all runs
   - Identify variability
   - Compare scenarios

5. **Visualizations**: `results/*.png`
   - Model dynamics
   - Survival analysis
   - Valuation distribution

---

## 🎯 Quick Links by Task

| Task | Document | Command |
|------|----------|---------|
| "How do I start?" | START_HERE.md | `python launcher.py` |
| "What do the parameters mean?" | USER_GUIDE.py | `python USER_GUIDE.py` |
| "How do I use the GUI?" | GUI_VISUAL_GUIDE.md | View in editor |
| "What commands exist?" | QUICK_REFERENCE.py | `python QUICK_REFERENCE.py` |
| "Can you explain everything?" | README.md | View in editor |
| "What are new features?" | GUI_SETUP_GUIDE.md | View in editor |
| "I'm confused, help!" | START_HERE.md then GUI_VISUAL_GUIDE.md | Read both |

---

## 🔍 Finding Answers

**"How do I change [parameter]?"**
→ USER_GUIDE.py, search for parameter name

**"What does this output mean?"**
→ README.md, "Data Collection" section

**"What command do I run?"**
→ QUICK_REFERENCE.py

**"Show me a screenshot"**
→ GUI_VISUAL_GUIDE.md

**"How long does it take?"**
→ QUICK_REFERENCE.py, "Performance" section

**"Can I do [specific scenario]?"**
→ USER_GUIDE.py, "Advanced Scenarios" section

---

## 📝 Document Maintenance

- **Last Updated**: December 2025
- **Version**: 2.0 (GUI Release)
- **Status**: ✅ Complete and tested

---

## 🚀 Ready to Start?

**Recommended: Start with `START_HERE.md`**

Then choose your path:
- **Quick Test**: Use defaults (2 min)
- **Policy Experiment**: Configure & compare (15 min)
- **Deep Dive**: Read USER_GUIDE.py (30 min)

```bash
python launcher.py
```

**Enjoy!** 🎉
