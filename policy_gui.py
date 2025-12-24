"""
GUI Interface for Startup Policy Configuration
Allows users to input and modify simulation parameters dynamically
"""

import tkinter as tk
from tkinter import ttk, messagebox
import config
import json
from pathlib import Path


class PolicyConfigGUI:
    """GUI for configuring startup simulation policies and parameters"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Startup Funding Dynamics - Policy Configuration")
        self.root.geometry("900x900")
        self.root.resizable(True, True)
        
        # Store original config values
        self.original_config = self._get_config_dict()
        self.current_config = self._get_config_dict()
        
        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_initial_conditions_tab()
        self.create_consumer_adoption_tab()
        self.create_investor_logic_tab()
        self.create_market_dynamics_tab()
        self.create_policy_tab()
        self.create_shocks_tab()
        self.create_simulation_tab()
        
        # Bottom buttons frame
        self.create_button_frame()
    
    def _get_config_dict(self):
        """Extract all config parameters into a dictionary"""
        return {
            # Initial Conditions
            'K0_MIN': config.K0_MIN,
            'K0_MAX': config.K0_MAX,
            'B0_MIN_RATIO': config.B0_MIN_RATIO,
            'B0_MAX_RATIO': config.B0_MAX_RATIO,
            'PMF_ALPHA': config.PMF_ALPHA,
            'PMF_BETA': config.PMF_BETA,
            
            # Consumer Adoption
            'GAMMA': config.GAMMA,
            'EPSILON_PRICE': config.EPSILON_PRICE,
            'BASE_PRICE': config.BASE_PRICE,
            'SIGMA_R': config.SIGMA_R,
            'Q_T': config.Q_T,
            
            # Burn Rate Dynamics
            'DELTA_GROWTH': config.DELTA_GROWTH,
            'DELTA_CUT': config.DELTA_CUT,
            'RUNWAY_LOW_THRESHOLD': config.RUNWAY_LOW_THRESHOLD,
            
            # PMF Evolution
            'ETA': config.ETA,
            'SIGMA_PMF': config.SIGMA_PMF,
            
            # Valuation
            'LAMBDA_1': config.LAMBDA_1,
            'LAMBDA_2': config.LAMBDA_2,
            'LAMBDA_3': config.LAMBDA_3,
            
            # Investor Logic
            'ALPHA_REVENUE_BURN': config.ALPHA_REVENUE_BURN,
            'PMF_MIN': config.PMF_MIN,
            'BETA_1': config.BETA_1,
            'BETA_2': config.BETA_2,
            'BETA_3': config.BETA_3,
            'KAPPA': config.KAPPA,
            
            # Market
            'M0_INITIAL': config.M0_INITIAL,
            'GROWTH_RATE_M': config.GROWTH_RATE_M,
            
            # Policy
            'C_REG': config.C_REG,
            'S_G': config.S_G,
            'TAU': config.TAU,
            
            # Shocks
            'P_SHOCK': config.P_SHOCK,
            'DELTA_PMF_SHOCK_MIN': config.DELTA_PMF_SHOCK_MIN,
            'DELTA_PMF_SHOCK_MAX': config.DELTA_PMF_SHOCK_MAX,
            'DELTA_M_SHOCK_MIN': config.DELTA_M_SHOCK_MIN,
            'DELTA_M_SHOCK_MAX': config.DELTA_M_SHOCK_MAX,
            
            # Simulation
            'NUM_STARTUPS': config.NUM_STARTUPS,
            'TIME_HORIZON': config.TIME_HORIZON,
            'V_EXIT': config.V_EXIT,
        }
    
    def create_initial_conditions_tab(self):
        """Tab for initial conditions"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Initial Conditions")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self._add_input_row(scrollable_frame, "K0_MIN (Min Initial Capital)", "K0_MIN", "₹", 0)
        self._add_input_row(scrollable_frame, "K0_MAX (Max Initial Capital)", "K0_MAX", "₹", 1)
        self._add_input_row(scrollable_frame, "B0 Min Ratio", "B0_MIN_RATIO", "%", 2)
        self._add_input_row(scrollable_frame, "B0 Max Ratio", "B0_MAX_RATIO", "%", 3)
        self._add_input_row(scrollable_frame, "PMF Distribution Alpha", "PMF_ALPHA", "", 4)
        self._add_input_row(scrollable_frame, "PMF Distribution Beta", "PMF_BETA", "", 5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_consumer_adoption_tab(self):
        """Tab for consumer adoption parameters"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Consumer Adoption")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self._add_input_row(scrollable_frame, "GAMMA (Adoption Curve Steepness)", "GAMMA", "", 0)
        self._add_input_row(scrollable_frame, "Price Sensitivity (ε)", "EPSILON_PRICE", "", 1)
        self._add_input_row(scrollable_frame, "Base Price", "BASE_PRICE", "₹", 2)
        self._add_input_row(scrollable_frame, "Revenue Noise Std Dev", "SIGMA_R", "₹", 3)
        self._add_input_row(scrollable_frame, "Quantity Per Customer", "Q_T", "units", 4)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_investor_logic_tab(self):
        """Tab for investor logic parameters"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Investor Logic")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self._add_input_row(scrollable_frame, "Min Revenue/Burn Ratio (α)", "ALPHA_REVENUE_BURN", "", 0)
        self._add_input_row(scrollable_frame, "Min PMF for Funding", "PMF_MIN", "", 1)
        self._add_input_row(scrollable_frame, "β₁ (PMF Coefficient)", "BETA_1", "", 2)
        self._add_input_row(scrollable_frame, "β₂ (Revenue Coefficient)", "BETA_2", "", 3)
        self._add_input_row(scrollable_frame, "β₃ (Competition Coefficient)", "BETA_3", "", 4)
        self._add_input_row(scrollable_frame, "Funding Amount (κ × V_t)", "KAPPA", "% of valuation", 5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_market_dynamics_tab(self):
        """Tab for market dynamics"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Market Dynamics")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self._add_input_row(scrollable_frame, "Initial Market Size", "M0_INITIAL", "consumers", 0)
        self._add_input_row(scrollable_frame, "Market Growth Rate", "GROWTH_RATE_M", "% per month", 1)
        self._add_input_row(scrollable_frame, "Burn Rate Growth (δ_g)", "DELTA_GROWTH", "%", 2)
        self._add_input_row(scrollable_frame, "Burn Rate Cut (δ_c)", "DELTA_CUT", "%", 3)
        self._add_input_row(scrollable_frame, "Low Runway Threshold", "RUNWAY_LOW_THRESHOLD", "months", 4)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_policy_tab(self):
        """Tab for policy parameters"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Policy & Tax")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self._add_input_row(scrollable_frame, "Regulatory Compliance Cost", "C_REG", "₹", 0)
        self._add_input_row(scrollable_frame, "Government Subsidy", "S_G", "₹", 1)
        self._add_input_row(scrollable_frame, "Tax Rate (τ)", "TAU", "%", 2)
        self._add_input_row(scrollable_frame, "PMF Noise Std Dev", "SIGMA_PMF", "", 3)
        self._add_input_row(scrollable_frame, "PMF Learning Rate (η)", "ETA", "", 4)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_shocks_tab(self):
        """Tab for external shocks"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="External Shocks")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self._add_input_row(scrollable_frame, "Shock Probability (p_s)", "P_SHOCK", "per month", 0)
        self._add_input_row(scrollable_frame, "PMF Shock Min", "DELTA_PMF_SHOCK_MIN", "", 1)
        self._add_input_row(scrollable_frame, "PMF Shock Max", "DELTA_PMF_SHOCK_MAX", "", 2)
        self._add_input_row(scrollable_frame, "Market Shock Min", "DELTA_M_SHOCK_MIN", "%", 3)
        self._add_input_row(scrollable_frame, "Market Shock Max", "DELTA_M_SHOCK_MAX", "%", 4)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_simulation_tab(self):
        """Tab for simulation parameters"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Simulation")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self._add_input_row(scrollable_frame, "Number of Startups", "NUM_STARTUPS", "agents", 0)
        self._add_input_row(scrollable_frame, "Time Horizon", "TIME_HORIZON", "months", 1)
        self._add_input_row(scrollable_frame, "Success Valuation Threshold", "V_EXIT", "₹", 2)
        self._add_input_row(scrollable_frame, "Valuation: Revenue Coefficient (λ₁)", "LAMBDA_1", "", 3)
        self._add_input_row(scrollable_frame, "Valuation: PMF Coefficient (λ₂)", "LAMBDA_2", "", 4)
        self._add_input_row(scrollable_frame, "Valuation: Capital Coefficient (λ₃)", "LAMBDA_3", "", 5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _add_input_row(self, parent, label, key, unit, row):
        """Add an input row to a frame"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        parent.columnconfigure(0, weight=1)
        
        # Label
        label_widget = ttk.Label(frame, text=label, width=40)
        label_widget.pack(side=tk.LEFT, padx=5)
        
        # Entry
        entry = ttk.Entry(frame, width=15)
        entry.pack(side=tk.LEFT, padx=5)
        entry.insert(0, str(self.current_config.get(key, "")))
        
        # Unit label
        unit_label = ttk.Label(frame, text=unit, width=20)
        unit_label.pack(side=tk.LEFT, padx=5)
        
        # Store reference
        if not hasattr(self, 'inputs'):
            self.inputs = {}
        self.inputs[key] = entry
    
    def create_button_frame(self):
        """Create button frame for actions"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Save Config Button
        save_btn = ttk.Button(button_frame, text="Save Configuration", command=self.save_config)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Load Config Button
        load_btn = ttk.Button(button_frame, text="Load Saved Config", command=self.load_config)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset Button
        reset_btn = ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_config)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Run Simulation Button
        run_btn = ttk.Button(button_frame, text="Run Simulation →", command=self.run_simulation)
        run_btn.pack(side=tk.RIGHT, padx=5)
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            # Get values from inputs
            config_dict = {}
            for key, entry in self.inputs.items():
                try:
                    value = float(entry.get())
                    config_dict[key] = value
                except ValueError:
                    messagebox.showerror("Error", f"Invalid value for {key}. Please enter a number.")
                    return
            
            # Save to JSON file
            with open('policy_config.json', 'w') as f:
                json.dump(config_dict, f, indent=4)
            
            self.current_config = config_dict
            messagebox.showinfo("Success", "Configuration saved to policy_config.json")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if Path('policy_config.json').exists():
                with open('policy_config.json', 'r') as f:
                    config_dict = json.load(f)
                
                # Update input fields
                for key, value in config_dict.items():
                    if key in self.inputs:
                        self.inputs[key].delete(0, tk.END)
                        self.inputs[key].insert(0, str(value))
                
                self.current_config = config_dict
                messagebox.showinfo("Success", "Configuration loaded from policy_config.json")
            else:
                messagebox.showwarning("Warning", "No saved configuration found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
    
    def reset_config(self):
        """Reset to original default values"""
        for key, entry in self.inputs.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(self.original_config[key]))
        
        messagebox.showinfo("Success", "Configuration reset to defaults")
    
    def run_simulation(self):
        """Run simulation with current configuration"""
        try:
            # Save current config
            self.save_config()
            
            # Update config module with new values
            for key, value in self.current_config.items():
                setattr(config, key, value)
            
            messagebox.showinfo("Ready", 
                "Configuration applied!\n\n"
                "Run the simulation with:\n"
                "python run_simulation.py"
            )
            
            # Optionally close the GUI
            # self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply configuration: {str(e)}")


def launch_gui():
    """Launch the policy configuration GUI"""
    root = tk.Tk()
    app = PolicyConfigGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
