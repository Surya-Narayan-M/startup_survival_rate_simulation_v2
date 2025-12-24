"""
StartupAgent - The only agent type in the simulation.
Contains all mandatory state variables and update logic.
"""

import numpy as np
from mesa import Agent
import config


class StartupAgent(Agent):
    """
    A startup agent with state variables:
    - K_t: Capital
    - B_t: Burn rate
    - R_t: Revenue
    - PMF_t: Product-Market Fit
    - V_t: Valuation
    - S_t: Survival status (0=dead, 1=alive)
    """
    
    def __init__(self, unique_id, model):
        super().__init__(model)
        
        # Initialize state variables at t=0
        # K0 ~ U(20L, 2Cr)
        self.K = np.random.uniform(config.K0_MIN, config.K0_MAX)
        
        # B0 ∈ [0.05*K0, 0.15*K0]
        self.B = np.random.uniform(
            config.B0_MIN_RATIO * self.K,
            config.B0_MAX_RATIO * self.K
        )
        
        # R0 ≈ 0
        self.R = config.R0_INITIAL
        
        # PMF0 ~ Beta(α, β)
        self.PMF = np.random.beta(config.PMF_ALPHA, config.PMF_BETA)
        
        # V0 ∝ K0 (using lambda_3 coefficient)
        self.V = config.LAMBDA_3 * self.K
        
        # S0 = 1 (alive)
        self.S = 1
        
        # Track if startup received funding this round
        self.just_funded = False
        
        # Initialize funding received
        self.funding_received = 0
        
        # Track runway for burn rate adjustments
        self.runway = self.K / self.B if self.B > 0 else float('inf')
    
    def stage_shock(self):
        """Stage 1: Shocks are handled globally in model"""
        pass
    
    def stage_market_update(self):
        """Stage 2: Market update handled globally in model"""
        pass
    
    def stage_consumer_adoption(self):
        """
        Stage 3: Calculate consumer adoption and revenue.
        
        Formulas:
        p_a,t = 1 / (1 + e^(-γ(PMF_t - ε·price)))
        R̄_t = M_t · p_a,t · q_t · (1 - θ_t)
        R_t = max(0, R̄_t + ε_r), ε_r ~ N(0, σ_r)
        """
        if self.S == 0:
            self.R = 0
            return
        
        # Consumer adoption probability (logistic function)
        exponent = -config.GAMMA * (self.PMF - config.EPSILON_PRICE * config.BASE_PRICE)
        p_a = 1 / (1 + np.exp(exponent))
        
        # Expected revenue
        M_t = self.model.market_size
        theta_t = self.model.competition_index
        q_t = config.Q_T
        
        R_bar = M_t * p_a * q_t * (1 - theta_t)
        
        # Add noise
        epsilon_r = np.random.normal(0, config.SIGMA_R)
        self.R = max(0, R_bar + epsilon_r)
    
    def stage_internal_dynamics(self):
        """
        Stage 4: Update burn rate based on conditions.
        
        B_t = B_{t-1}(1 + δ_g) if just funded
        B_t = B_{t-1}(1 - δ_c) if runway is low
        """
        if self.S == 0:
            return
        
        # Increase burn rate after funding
        if self.just_funded:
            self.B = self.B * (1 + config.DELTA_GROWTH)
            self.just_funded = False
        
        # Decrease burn rate if runway is low
        elif self.runway < config.RUNWAY_LOW_THRESHOLD and self.B > 0:
            self.B = self.B * (1 - config.DELTA_CUT)
    
    def stage_capital_update(self):
        """
        Stage 5: Update capital and check for death.
        
        K_{t+1} = K_t + R_t - B_t + F_t
        If K_{t+1} ≤ 0 => S_{t+1} = 0
        """
        if self.S == 0:
            return
        
        # F_t is set by funding stage, default is 0
        F_t = getattr(self, 'funding_received', 0)
        
        # Update capital
        self.K = self.K + self.R - self.B + F_t
        
        # Reset funding for next cycle
        self.funding_received = 0
        
        # Check for death
        if self.K <= 0:
            self.S = 0
            self.K = 0
            self.death_time = self.model.schedule.steps
        
        # Update runway
        if self.S == 1 and self.B > 0:
            self.runway = self.K / self.B
        else:
            self.runway = 0 if self.S == 0 else float('inf')
    
    def stage_pmf_valuation_update(self):
        """
        Stage 6: Update PMF and valuation.
        
        PMF_{t+1} = PMF_t + η·log(1 + R_t) + ε_p
        V_{t+1} = λ_1·R_t + λ_2·PMF_t + λ_3·K_t
        """
        if self.S == 0:
            return
        
        # PMF evolution
        epsilon_p = np.random.normal(0, config.SIGMA_PMF)
        self.PMF = self.PMF + config.ETA * np.log(1 + self.R) + epsilon_p
        self.PMF = np.clip(self.PMF, 0, 1)  # Keep PMF in [0, 1]
        
        # Valuation update
        self.V = (config.LAMBDA_1 * self.R + 
                  config.LAMBDA_2 * self.PMF + 
                  config.LAMBDA_3 * self.K)
    
    def stage_funding(self):
        """
        Stage 7: Investor logic (executed every 6 months).
        
        Eligibility: R_t/B_t ≥ α AND PMF_t ≥ PMF_min
        P(fund) = σ(β_1·PMF_t + β_2·log(R_t + 1) - β_3·θ_t)
        F_t = κ·V_t if funded, else 0
        """
        if self.S == 0:
            self.funding_received = 0
            return
        
        # Only evaluate funding every 6 months
        if self.model.schedule.steps % config.FUNDING_INTERVAL != 0:
            self.funding_received = 0
            return
        
        # Check eligibility
        revenue_burn_ratio = self.R / self.B if self.B > 0 else 0
        
        is_eligible = (revenue_burn_ratio >= config.ALPHA_REVENUE_BURN and 
                      self.PMF >= config.PMF_MIN)
        
        if not is_eligible:
            self.funding_received = 0
            return
        
        # Calculate funding probability (logistic)
        theta_t = self.model.competition_index
        z = (config.BETA_1 * self.PMF + 
             config.BETA_2 * np.log(self.R + 1) - 
             config.BETA_3 * theta_t)
        
        p_fund = 1 / (1 + np.exp(-z))
        
        # Determine if funded
        if np.random.random() < p_fund:
            self.funding_received = config.KAPPA * self.V
            self.just_funded = True
        else:
            self.funding_received = 0
    
    def stage_policy(self):
        """
        Stage 8: Policy impact (executed every 12 months).
        
        B_t^eff = B_t + C_reg - S_g + τ·R_t
        """
        if self.S == 0:
            return
        
        # Only apply policy every 12 months
        if self.model.schedule.steps % config.POLICY_INTERVAL != 0:
            return
        
        # Effective burn rate includes policy impacts
        policy_impact = config.C_REG - config.S_G + config.TAU * self.R
        self.B = self.B + policy_impact
        
        # Ensure burn rate doesn't go negative
        self.B = max(0, self.B)
