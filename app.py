"""
ABM: How Monetary Policy Affects Startup Funding (Mesa)

Single-file runnable example.

Install:
    pip install mesa pandas numpy

Run:
    python abm_startup_funding.py
"""

import random
import math
import statistics
import numpy as np
import pandas as pd
from mesa import Model, Agent
from mesa.time import StagedActivation
from mesa.datacollection import DataCollector

# -------------------------
# Model-level configuration
# -------------------------
MODEL_PARAMS = {
    # RBI policy inputs (these could be hooked to sliders/UI)
    "repo": 6.50,            # percent
    "rev_repo": 6.00,        # reverse repo (lower bound)
    "msf": 7.00,             # MSF (upper bound)
    "crr": 4.5,              # percent
    "slr": 18.0,             # percent
    "omo": 0.0,              # net OMO injection (₹ units, abstract scale)

    # pass-through coefficients and FC weights
    "a_CRR": 0.01,           # how strongly CRR increases funding cost (per %)
    "a_SLR": 0.002,          # SLR effect (per %)
    "a_MSF": 0.5,            # MSF spread weight
    "a_RR": 0.3,             # reverse repo effect weight

    # loan pricing
    "m0": 0.5,               # base markup (percentage points)
    "m1": 5.0,               # multiplier on startup risk (higher -> bigger premium)

    # pass-through reduced form
    "mu": 1.0,               # base markup in lending-rate pass-through
    "beta_pass": 0.8,        # fraction of marginal cost passed to lending rate

    # investor logit parameters
    "lambda_dom": 1.0,       # domestic investor sensitivity (higher -> more responsive)
    "kappa_for": 1.0,        # foreign investor sensitivity

    # funding score coefficients
    "a1": 1.0,               # weight on loan rate (negative sign applied in formula)
    "a2": 1.0,               # domestic supply weight
    "a3": 1.0,               # foreign supply weight
    "a4": 1.0,               # government support weight

    # pools & counts
    "num_banks": 5,
    "num_dom_investors": 20,
    "num_startups": 200,
    "initial_dom_investor_pool": 1000.0,   # abstract money units
    "initial_foreign_pool": 2000.0,        # abstract money
    "gov_support_level": 50.0,             # F_gov
    "r_safe_IN": 4.0,                      # local safe return (%)
    "r_global": 3.5,                       # global risk-free (%)
    "risk_premium_IN": 1.0,                # home equity risk premium
    "liquidity_initial": 500.0,            # system liquidity (abstract units)
}


# -------------------------
# Helper math functions
# -------------------------
def logistic(x):
    return 1.0 / (1.0 + math.exp(-x))


# -------------------------
# Agent classes
# -------------------------
class RBI(Agent):
    """
    RBI agent: holds policy inputs and updates model-level attributes.
    In this simple implementation, RBI reads static inputs provided in
    model.config and writes model-level variables that other agents use.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def rbi_update(self): pass
    def government_update(self): pass
    def bank_update(self): pass
    def investor_update(self): pass
    def foreign_update(self): pass
    def startup_update(self): pass


    def rbi_update(self):
        m = self.model
        cfg = m.config

        # set policy variables (could be dynamic or scenario-driven)
        m.repo = cfg["repo"]
        m.rev_repo = cfg["rev_repo"]
        m.msf = cfg["msf"]
        m.crr = cfg["crr"]
        m.slr = cfg["slr"]
        # OMO affects liquidity
        m.omo = cfg["omo"]

        # update liquidity with OMO (simple additive)
        m.liquidity += m.omo

    def step(self):
        pass


class GovernmentAgent(Agent):
    """
    Government sets fiscal inputs that affect startups (F_gov).
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def rbi_update(self): pass
    def government_update(self): pass
    def bank_update(self): pass
    def investor_update(self): pass
    def foreign_update(self): pass
    def startup_update(self): pass


    def government_update(self):
        m = self.model
        cfg = m.config
        m.tax_rate = cfg.get("tax_rate", 0.0)
        m.gov_support = cfg.get("gov_support_level", MODEL_PARAMS["gov_support_level"])

    def step(self):
        pass


class BankAgent(Agent):
    """
    Bank agent implements cost-of-funds and lending decisions.
    Each bank has a small balance sheet; lending capacity depends on model liquidity.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.loans_given = 0.0
        self.deposits = 100.0 + random.random() * 50.0  # simple initial deposits
        self.reserves = 0.0

    def rbi_update(self): pass
    def government_update(self): pass
    def bank_update(self): pass
    def investor_update(self): pass
    def foreign_update(self): pass
    def startup_update(self): pass


    def compute_FC(self):
        m = self.model
        cfg = m.config
        # FC(t) formula from user
        fc = (
            m.repo
            + cfg["a_CRR"] * m.crr
            + cfg["a_SLR"] * m.slr
            + cfg["a_MSF"] * (m.msf - m.repo)
            - cfg["a_RR"] * (m.repo - m.rev_repo)
        )
        return fc

    def compute_loan_rate_startup(self, startup_risk):
        m = self.model
        cfg = m.config
        fc = self.compute_FC()
        # r_loan_startup = FC + m0 + m1 * StartupRisk
        return fc + cfg["m0"] + cfg["m1"] * startup_risk

    def compute_market_lending_rate(self):
        # reduced-form pass-through: l_t = mu + beta*mc_t
        m = self.model
        mc = self.compute_FC()
        return m.config["mu"] + m.config["beta_pass"] * mc

    def bank_update(self):
        # Each bank decides how much credit to supply this period.
        m = self.model
        # Simple rule: available_to_lend depends on deposits + share of system liquidity
        # scaling factor to avoid unrealistic lending
        supply_from_liquidity = max(0.0, m.liquidity * 0.02)  # each bank takes small share
        available = max(0.0, self.deposits * 0.6 + supply_from_liquidity)
        self.available_to_lend = available
        # record lending rate for outputs (we use market lending rate)
        self.current_lending_rate = self.compute_market_lending_rate()

    def allocate_loans_to_startups(self, startup_list):
        """
        Distribute available_to_lend across startups based on their funding score ranking.
        This is called by the model after all banks updated.
        """
        if self.available_to_lend <= 0:
            return 0.0
        # Sort startups by funding score descending
        sorted_startups = sorted(startup_list, key=lambda s: s.funding_score, reverse=True)
        allocated = 0.0
        remaining = self.available_to_lend
        for s in sorted_startups:
            if remaining <= 0:
                break
            # each startup has a demand; fulfill partially if possible
            demand = s.request_amount
            give = min(demand, remaining)
            if give > 0:
                s.receive_debt(give, lender=self)
                remaining -= give
                allocated += give
        # reduce liquidity by amount allocated (banks used cash to lend)
        self.loans_given += allocated
        return allocated

    def step(self):
        pass


class DomesticInvestorAgent(Agent):
    """
    Domestic equity investors (VC/Angel).
    Each investor has a pool of capital and decides fraction to allocate to startups.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pool = model.config["initial_dom_investor_pool"] / model.config["num_dom_investors"]
        # portfolio shares (for output metric)
        self.safe_share = 1.0
        self.startup_share = 0.0

    def rbi_update(self): pass
    def government_update(self): pass
    def bank_update(self): pass
    def investor_update(self): pass
    def foreign_update(self): pass
    def startup_update(self): pass


    def compute_R_startup(self):
        """
        Expected return from startup investments.
        Here we make a parsimonious, defensible specification:
        R_startup = base_equity_return - penalty * average_loan_rate + sentiment_term
        The user provided logit uses R_startup - r_safe; this is consistent.
        """
        m = self.model
        base_equity = 15.0  # baseline expected return percent for startups (abstract)
        avg_loan = m.get_average_loan_rate()
        sentiment = m.sentiment_index  # can be positive/negative small number
        # penalty coefficient (how much loan rate reduces equity returns)
        penalty = 0.5
        R = base_equity - penalty * avg_loan + 0.1 * sentiment
        return R

    def investor_update(self):
        m = self.model
        cfg = m.config
        R_startup = self.compute_R_startup()
        r_safe = cfg["r_safe_IN"]
        lam = cfg["lambda_dom"]
        # logit allocation
        share_to_startups = logistic(lam * (R_startup - r_safe))
        # allocate capital
        invest = self.pool * share_to_startups
        # update portfolio shares (for outputs)
        self.startup_share = share_to_startups
        self.safe_share = 1.0 - share_to_startups
        # distribute funds to startups via model allocator
        m.domestic_supply += invest

    def step(self):
        pass


class ForeignCapitalAgent(Agent):
    """
    Foreign capital flows react to global interest rates and India risk-adjusted returns.
    The global rate is treated as an exogenous input in model.config.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pool = model.config["initial_foreign_pool"]

    def rbi_update(self): pass
    def government_update(self): pass
    def bank_update(self): pass
    def investor_update(self): pass
    def foreign_update(self): pass
    def startup_update(self): pass


    def foreign_update(self):
        m = self.model
        cfg = m.config
        # risk-adjusted home return
        r_safe_IN = cfg["r_safe_IN"]
        risk_prem = cfg["risk_premium_IN"]
        r_global = cfg["r_global"]
        # expression inside logistic: (r_safe_IN - riskprem - r_global)
        inner = (r_safe_IN - risk_prem) - r_global
        kappa = cfg["kappa_for"]
        share_to_india = logistic(kappa * inner)
        # foreign supply for startups
        supply = self.pool * share_to_india
        m.foreign_supply += supply
        # record for outputs
        self.latest_inflow = supply

    def step(self):
        pass


class StartupAgent(Agent):
    """
    Startup agent demands funding and updates its state.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # state variables
        self.age = 0
        self.alive = True
        self.valuation = 1.0 + random.random() * 2.0  # initial valuation (abstract units)
        self.request_amount = 5.0 + random.random() * 10.0  # demand per period
        # risk score [0,1], higher -> riskier (affects m1 * StartupRisk)
        self.risk = 0.2 + random.random() * 0.6
        # funds received in current period
        self.received_debt = 0.0
        self.received_equity = 0.0
        self.funded = False
        # funding score (calculated by model)
        self.funding_score = 0.0

    def rbi_update(self): pass
    def government_update(self): pass
    def bank_update(self): pass
    def investor_update(self): pass
    def foreign_update(self): pass
    def startup_update(self): pass


    def compute_funding_score(self):
        """
        FundingScore(t) = -a1 * r_loan(t) + a2*S_dom + a3*S_for + a4*F_gov
        r_loan here we use model average loan rate (or bank's lending rate)
        S_dom and S_for are current supplies
        """
        m = self.model
        cfg = m.config
        r_loan = m.get_average_loan_rate()
        score = (
            -cfg["a1"] * r_loan
            + cfg["a2"] * m.domestic_supply
            + cfg["a3"] * m.foreign_supply
            + cfg["a4"] * m.gov_support
        )
        self.funding_score = score
        return score

    def request_funding(self):
        # called each period; reset funding flags and required amounts
        self.funded = False
        self.received_debt = 0.0
        self.received_equity = 0.0
        # demand may vary with age
        self.request_amount = max(2.0, 5.0 + (1.0 - self.risk) * 10.0 * random.random())

    def receive_debt(self, amount, lender=None):
        self.received_debt += amount
        if self.received_debt >= self.request_amount * 0.6:
            # consider startup 'debt-funded' if it gets at least 60% of demand
            self.funded = True

    def receive_equity(self, amount):
        self.received_equity += amount
        if (self.received_debt + self.received_equity) >= self.request_amount * 0.6:
            self.funded = True

    def startup_update(self):
        m = self.model
        # update age and expectations
        self.age += 1
        # After funding allocation, determine survival
        if not self.funded:
            # probability of failure increases if no funding
            fail_prob = min(0.5, 0.05 + 0.2 * (self.request_amount / (1.0 + 0.01 * m.get_average_loan_rate())))
            if random.random() < fail_prob:
                self.alive = False
        else:
            # funded -> valuation grows; growth depends on investment amount and sentiment
            inflow = self.received_debt + self.received_equity
            growth = 0.01 * inflow + 0.02 * (m.sentiment_index / 10.0)
            self.valuation *= (1.0 + growth)

    def step(self):
        pass


# -------------------------
# The Model
# -------------------------
class StartupFundingModel(Model):
    def __init__(self, **kwargs):
        super().__init__()

        # start with default parameters
        self.config = dict(MODEL_PARAMS)

        # overwrite defaults with values coming from sliders
        for key, value in kwargs.items():
            self.config[key] = value
        # macro state variables
        self.repo = self.config["repo"]
        self.rev_repo = self.config["rev_repo"]
        self.msf = self.config["msf"]
        self.crr = self.config["crr"]
        self.slr = self.config["slr"]
        self.omo = self.config["omo"]
        self.liquidity = self.config["liquidity_initial"]

        # aggregated supplies produced each step by investors/foreign/banks
        self.domestic_supply = 0.0
        self.foreign_supply = 0.0
        self.bank_total_available = 0.0

        # sentiment index (simple tracker of recent successes)
        self.sentiment_index = 0.0

        # data outputs
        self.running = True

        # scheduler with stages in correct causal order
        stage_list = [
            "rbi_update",
            "government_update",
            "bank_update",
            "investor_update",
            "foreign_update",
            "prep_startups",  # compute funding scores and reset requests
            "allocate_credit",  # banks allocate debt and model allocates equity
            "startup_update",
        ]
        self.schedule = StagedActivation(self, stage_list=stage_list, shuffle=False)

        # create agents
        self.rbi = RBI("RBI", self)
        self.schedule.add(self.rbi)
        self.gov = GovernmentAgent("GOV", self)
        self.schedule.add(self.gov)

        # banks
        self.banks = []
        for i in range(self.config["num_banks"]):
            b = BankAgent(f"B{i}", self)
            self.banks.append(b)
            self.schedule.add(b)

        # domestic investors
        self.domestic_investors = []
        for i in range(self.config["num_dom_investors"]):
            inv = DomesticInvestorAgent(f"DINV{i}", self)
            self.domestic_investors.append(inv)
            self.schedule.add(inv)

        # foreign capital (single aggregated agent)
        self.foreign_agent = ForeignCapitalAgent("FOR", self)
        self.schedule.add(self.foreign_agent)

        # startups
        self.startups = []
        for i in range(self.config["num_startups"]):
            s = StartupAgent(f"S{i}", self)
            self.startups.append(s)
            self.schedule.add(s)

        # Data collector for output metrics
        self.datacollector = DataCollector(
            model_reporters={
                "total_startup_funding": lambda m: m.get_total_funding_volume(),
                "avg_valuation": lambda m: m.get_average_valuation(),
                "startup_failure_rate": lambda m: m.get_failure_rate(),
                "avg_loan_rate": lambda m: m.get_average_loan_rate(),
                "investor_portfolio_shift": lambda m: m.get_investor_portfolio_shift(),
                "sentiment_index": lambda m: m.sentiment_index,
                "foreign_capital_inflow": lambda m: m.foreign_supply,
                "liquidity_index": lambda m: m.liquidity,
            },
            agent_reporters={}
        )

        # initialize trackers
        self.step_count = 0

    # -------------------------
    # Utility methods used by agents and outputs
    # -------------------------
    def get_average_loan_rate(self):
        # average current_lending_rate across banks
        rates = [getattr(b, "current_lending_rate", None) for b in self.banks]
        rates = [r for r in rates if r is not None]
        if len(rates) == 0:
            return self.config["repo"]
        return sum(rates) / len(rates)

    def get_total_funding_volume(self):
        # total funding provided to startups this step (debt + equity)
        total = sum((s.received_debt + s.received_equity) for s in self.startups)
        return total

    def get_average_valuation(self):
        vals = [s.valuation for s in self.startups if s.alive]
        if not vals:
            return 0.0
        return sum(vals) / len(vals)

    def get_failure_rate(self):
        alive = [s for s in self.startups if s.alive]
        failed = [s for s in self.startups if not s.alive]
        total = len(self.startups)
        if total == 0:
            return 0.0
        return len(failed) / total

    def get_investor_portfolio_shift(self):
        # average fraction allocated to startups by domestic investors
        shares = [inv.startup_share for inv in self.domestic_investors]
        if not shares:
            return 0.0
        return sum(shares) / len(shares)

    # -------------------------
    # Scheduler stage methods (called by StagedActivation)
    # The stage methods are named "<stage>_<agent class name>" or we can
    # dispatch within each agent's step; Mesa StagedActivation calls agent.<stage>()
    # We implement per-agent methods with matching names.
    # -------------------------
    def step(self):
        # reset aggregated supplies each step
        self.domestic_supply = 0.0
        self.foreign_supply = 0.0
        self.bank_total_available = 0.0
        self.sentiment_index = max(0.0, self.sentiment_index * 0.95)  # decay
        self.schedule.step()
        # after full step, collect data
        self.datacollector.collect(self)
        self.step_count += 1

    # Stage callbacks: the scheduler calls agents' methods with stage name.
    # We'll implement the action by having each agent's class implement methods named
    # like rbi_update(), government_update(), etc., which we did above.

    # After 'bank_update' stage, we need a global action to allocate loans
    # We'll implement that in the 'allocate_credit' stage by using a model-level method.
    def allocate_credit(self):
        # Banks allocate to startups (debt)
        # First, let each bank compute its available_to_lend and accumulate total
        total_allocated = 0.0
        # call bank allocation function sequentially
        for b in self.banks:
            total_allocated += b.allocate_loans_to_startups(self.startups)
        # After banks have allocated debt, allocate equity from domestic and foreign supplies.
        # Simple pro-rata equity allocation to top startups by funding_score.
        total_equity = self.domestic_supply + self.foreign_supply
        if total_equity > 0:
            # order startups by funding_score
            sorted_startups = sorted(self.startups, key=lambda s: s.funding_score, reverse=True)
            remaining = total_equity
            for s in sorted_startups:
                if remaining <= 0:
                    break
                # give small equity slice up to request remaining
                needed = max(0.0, s.request_amount - (s.received_debt + s.received_equity))
                give = min(needed, remaining)
                if give > 0:
                    s.receive_equity(give)
                    remaining -= give
        # track liquidity change: lending reduces liquidity, equity inflows increase it
        # approximate: debt allocated reduces liquidity by total_allocated, equity adds domestic+foreign
        self.liquidity = max(0.0, self.liquidity - total_allocated + (self.domestic_supply + self.foreign_supply))
        # update sentiment index: successful funded startups increase sentiment
        successes = sum(1 for s in self.startups if s.funded and s.alive)
        self.sentiment_index += successes * 0.1

    # Methods to be invoked by StageActivation through agents
    # We map these by giving the agents methods named exactly as stage names if needed.
    # But for the 'prep_startups' and 'allocate_credit' stages we handle at the model-level.

# -------------------------
# Bind the stage call names to agent methods
# -------------------------
# To make StagedActivation call the right functions on the agents, Mesa looks up methods
# named '<stage>' on each agent. We already defined those (e.g., rbi_update, government_update, bank_update, investor_update, foreign_update, startup_update).
# For the special stages 'prep_startups' and 'allocate_credit' we implement separate functions
# that we call by adding small helper agents or by injecting calls into the model scheduler.
# StagedActivation will call each agent.step() for stages where step() is defined; we'll therefore
# add small wrappers: add methods with names matching stages on each agent. We already added
# e.g., rbi_update() etc. For 'prep_startups' and 'allocate_credit', we'll attach functions to the model object
# by creating a tiny wrapper agent. However Mesa's StagedActivation iterates over self.schedule.agents and calls
# stage method if present; to keep it simple, we will monkey-patch a method named 'prep_startups' and 'allocate_credit'
# onto each agent class that delegates to model-level action when called for the first agent only.

# Attach 'prep_startups' method to agents to call model-level preparation once per step.
def prep_startups_for_agent(self):
    # only let the first agent call the model-level prep
    if isinstance(self, RBI):
        # Prep: each startup reset requests and compute funding score
        for s in self.model.startups:
            s.request_funding()
            s.compute_funding_score()

# Attach allocate_credit_for_agent to call model.allocate_credit from first agent
def allocate_credit_for_agent(self):
    if isinstance(self, RBI):
        self.model.allocate_credit()

# Dynamically add methods to Agent classes so StagedActivation can call them
setattr(RBI, "rbi_update", RBI.rbi_update)
setattr(GovernmentAgent, "government_update", GovernmentAgent.government_update)
setattr(BankAgent, "bank_update", BankAgent.bank_update)
setattr(DomesticInvestorAgent, "investor_update", DomesticInvestorAgent.investor_update)
setattr(ForeignCapitalAgent, "foreign_update", ForeignCapitalAgent.foreign_update)
setattr(StartupAgent, "startup_update", StartupAgent.startup_update)
# prep and allocate hooks
setattr(RBI, "prep_startups", prep_startups_for_agent)
setattr(RBI, "allocate_credit", allocate_credit_for_agent)
# For other agents, provide no-op methods with same names so scheduler won't error
for cls in (GovernmentAgent, BankAgent, DomesticInvestorAgent, ForeignCapitalAgent, StartupAgent):
    if not hasattr(cls, "prep_startups"):
        setattr(cls, "prep_startups", lambda self: None)
    if not hasattr(cls, "allocate_credit"):
        setattr(cls, "allocate_credit", lambda self: None)


# -------------------------
# Run a small demonstration
# -------------------------
def run_demo(steps=30, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    model = StartupFundingModel(config=MODEL_PARAMS)
    for i in range(steps):
        model.step()
    df = model.datacollector.get_model_vars_dataframe()
    print(df.tail(10))
    # Save to CSV for inspection
    df.to_csv("abm_startup_outputs.csv", index=True)
    print("\nSaved outputs to abm_startup_outputs.csv")
    return model, df


if __name__ == "__main__":
    run_demo(steps=60)
