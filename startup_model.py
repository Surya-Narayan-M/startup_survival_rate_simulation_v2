"""
StartupModel - Mesa Model with global dynamics.
Handles market, investor, policy, and shock dynamics.
"""

import numpy as np
from mesa import Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from startup_agent import StartupAgent
import config


class StagedActivation(BaseScheduler):
    """
    Custom scheduler that activates agents in stages.
    
    Stage order (MANDATORY):
    1. Shock stage
    2. Market update stage
    3. Consumer adoption stage
    4. Startup internal dynamics stage
    5. Capital update & death stage
    6. PMF & valuation update stage
    7. Funding stage (if month % 6 == 0)
    8. Policy stage (if month % 12 == 0)
    """
    
    def __init__(self, model):
        super().__init__(model)
        self.stage_list = [
            "stage_shock",
            "stage_market_update",
            "stage_consumer_adoption",
            "stage_internal_dynamics",
            "stage_capital_update",
            "stage_pmf_valuation_update",
            "stage_funding",
            "stage_policy"
        ]
    
    def step(self):
        """Execute all stages in order for all agents"""
        # Stage 1: Shock (global, handled in model)
        self.model.apply_shocks()
        
        # Stage 2: Market update (global, handled in model)
        self.model.update_market()
        
        # Stages 3-8: Agent-specific
        for stage in self.stage_list[2:]:  # Skip shock and market (handled above)
            for agent in self.agents:
                getattr(agent, stage)()
        
        self.steps += 1
        self.time += 1


class StartupModel(Model):
    """
    Mesa model for startup funding dynamics simulation.
    
    Non-agent global processes:
    - Investor logic
    - Market dynamics
    - Consumer behavior
    - Policy/regulation
    - External shocks
    """
    
    def __init__(self, num_startups=config.NUM_STARTUPS, seed=None):
        super().__init__()
        
        # Set random seed for reproducibility
        if seed is not None:
            self.random.seed(seed)
            np.random.seed(seed)
        
        # Initialize scheduler with staged activation
        self.schedule = StagedActivation(self)
        
        # Global state variables
        self.market_size = config.M0_INITIAL
        self.initial_startups = num_startups
        self.competition_index = 0  # θ_t
        
        # Create startup agents
        for i in range(num_startups):
            agent = StartupAgent(i, self)
            self.schedule.add(agent)
        
        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "Alive_Startups": lambda m: sum(1 for a in m.schedule.agents if a.S == 1),
                "Dead_Startups": lambda m: sum(1 for a in m.schedule.agents if a.S == 0),
                "Failure_Rate": lambda m: sum(1 for a in m.schedule.agents if a.S == 0) / len(m.schedule.agents),
                "Total_Funding": lambda m: sum(getattr(a, 'funding_received', 0) for a in m.schedule.agents if a.S == 1),
                "Avg_Valuation": lambda m: np.mean([a.V for a in m.schedule.agents if a.S == 1]) if any(a.S == 1 for a in m.schedule.agents) else 0,
                "Avg_PMF": lambda m: np.mean([a.PMF for a in m.schedule.agents if a.S == 1]) if any(a.S == 1 for a in m.schedule.agents) else 0,
                "Avg_Revenue": lambda m: np.mean([a.R for a in m.schedule.agents if a.S == 1]) if any(a.S == 1 for a in m.schedule.agents) else 0,
                "Market_Size": lambda m: m.market_size,
                "Competition_Index": lambda m: m.competition_index,
            },
            agent_reporters={
                "Capital": "K",
                "Burn_Rate": "B",
                "Revenue": "R",
                "PMF": "PMF",
                "Valuation": "V",
                "Survival": "S",
                "Funding_Received": lambda a: getattr(a, 'funding_received', 0),
                "Death_Time": lambda a: getattr(a, 'death_time', None),
            }
        )
    
    def apply_shocks(self):
        """
        Stage 1: Apply external shocks monthly.
        
        Pr(shock) = p_s
        If shock occurs:
            PMF_t ← PMF_t + ΔPMF
            M_t ← M_t(1 + ΔM)
        """
        # Check if shock occurs
        if np.random.random() < config.P_SHOCK:
            # Generate shock magnitudes
            delta_pmf = np.random.uniform(
                config.DELTA_PMF_SHOCK_MIN,
                config.DELTA_PMF_SHOCK_MAX
            )
            delta_m = np.random.uniform(
                config.DELTA_M_SHOCK_MIN,
                config.DELTA_M_SHOCK_MAX
            )
            
            # Apply PMF shock to all alive startups
            for agent in self.schedule.agents:
                if agent.S == 1:
                    agent.PMF = np.clip(agent.PMF + delta_pmf, 0, 1)
            
            # Apply market shock
            self.market_size = self.market_size * (1 + delta_m)
            self.market_size = max(0, self.market_size)
    
    def update_market(self):
        """
        Stage 2: Update market dynamics.
        
        M_{t+1} = M_t(1 + g_m)
        θ_t = active_startups / initial_startups
        """
        # Market growth
        self.market_size = self.market_size * (1 + config.GROWTH_RATE_M)
        
        # Competition index
        active_startups = sum(1 for agent in self.schedule.agents if agent.S == 1)
        self.competition_index = active_startups / self.initial_startups
    
    def step(self):
        """Execute one time step (1 month)"""
        self.datacollector.collect(self)
        self.schedule.step()
    
    def run_model(self, steps=config.TIME_HORIZON):
        """Run the model for specified number of steps"""
        for _ in range(steps):
            self.step()
        
        # Final data collection
        self.datacollector.collect(self)
    
    def get_success_count(self):
        """
        Calculate success based on definition:
        S_60 = 1 AND V_60 >= V_exit
        """
        successful = sum(
            1 for agent in self.schedule.agents 
            if agent.S == 1 and agent.V >= config.V_EXIT
        )
        return successful
    
    def get_top_10_percent_count(self):
        """Alternative metric: Top 10% valuation percentile"""
        alive_agents = [a for a in self.schedule.agents if a.S == 1]
        if not alive_agents:
            return 0
        
        valuations = [a.V for a in alive_agents]
        percentile_90 = np.percentile(valuations, 90)
        
        top_10_percent = sum(1 for v in valuations if v >= percentile_90)
        return top_10_percent
    
    def get_survival_times(self):
        """Get survival time distribution for dead startups"""
        survival_times = []
        for agent in self.schedule.agents:
            if agent.S == 0 and hasattr(agent, 'death_time'):
                survival_times.append(agent.death_time)
        return survival_times
    
    def get_agent_data(self):
        """Return final agent-level data"""
        agent_data = self.datacollector.get_agent_vars_dataframe()
        return agent_data
    
    def get_model_data(self):
        """Return model-level time series data"""
        model_data = self.datacollector.get_model_vars_dataframe()
        return model_data
