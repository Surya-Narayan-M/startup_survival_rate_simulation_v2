# Startup Funding Dynamics - Agent-Based Simulation

Agent-based stochastic simulation using Mesa framework to model startup funding dynamics and success/failure rates.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Using the Launcher (Recommended)
```bash
python launcher.py
```
Interactive menu with options to configure policies, run simulation, or view results.

### Option 2: Configure Policies with GUI
```bash
python policy_gui.py
```
Opens a graphical interface to customize all simulation parameters. Configuration is saved to `policy_config.json`

### Option 3: Run Simulation Directly
```bash
python run_simulation.py
```
Runs with saved configuration or defaults.

## Project Structure

- `launcher.py` - Interactive menu interface (start here!)
- `policy_gui.py` - GUI for policy configuration
- `startup_agent.py` - StartupAgent implementation
- `startup_model.py` - Mesa Model with global dynamics
- `run_simulation.py` - Main simulation execution
- `analysis.py` - Data analysis and visualization
- `config.py` - Default model parameters
- `policy_config.json` - User-saved configurations (auto-generated)
