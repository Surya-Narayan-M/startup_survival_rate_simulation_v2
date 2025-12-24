"""
Configuration parameters for the Startup Funding Dynamics simulation.
All values are fixed as per specification.
"""

# Simulation Parameters
NUM_STARTUPS = 1000
TIME_HORIZON = 60  # months
RANDOM_SEED = 42

# Initial Capital (K0) - Uniform distribution
K0_MIN = 20_00_000  # 20 Lakhs in rupees
K0_MAX = 2_00_00_000  # 2 Crores in rupees

# Initial Burn Rate (B0) - as percentage of K0
B0_MIN_RATIO = 0.05
B0_MAX_RATIO = 0.15

# Initial Revenue (R0)
R0_INITIAL = 0

# Initial PMF - Beta distribution
PMF_ALPHA = 2
PMF_BETA = 5

# Consumer Adoption Parameters
GAMMA = 2  # logistic curve steepness
EPSILON_PRICE = 0.01  # price sensitivity
BASE_PRICE = 100  # base product price

# Revenue Noise
SIGMA_R = 10000  # standard deviation for revenue noise

# Burn Rate Dynamics
DELTA_GROWTH = 0.2  # 20% increase after funding
DELTA_CUT = 0.15  # 15% decrease when runway is low
RUNWAY_LOW_THRESHOLD = 3  # months

# PMF Evolution
ETA = 0.01  # learning rate from revenue
SIGMA_PMF = 0.02  # PMF noise std dev

# Valuation Coefficients
LAMBDA_1 = 10  # revenue multiplier
LAMBDA_2 = 1_00_00_000  # PMF multiplier
LAMBDA_3 = 2  # capital multiplier

# Investor Logic - Funding every 6 months
FUNDING_INTERVAL = 6  # months
ALPHA_REVENUE_BURN = 0.3  # minimum revenue/burn ratio
PMF_MIN = 0.3  # minimum PMF for funding eligibility

# Funding Probability (logistic regression)
BETA_1 = 5.0  # PMF coefficient
BETA_2 = 0.5  # log(Revenue) coefficient
BETA_3 = 2.0  # competition (theta) coefficient

# Funding Amount
KAPPA = 0.25  # 25% of valuation

# Market Dynamics
M0_INITIAL = 10_00_00_000  # initial market size (consumers) - increased 10x
GROWTH_RATE_M = 0.05  # 5% monthly market growth

# Policy Parameters - Applied every 12 months
POLICY_INTERVAL = 12  # months
C_REG = 50000  # regulatory compliance cost
S_G = 30000  # government subsidy
TAU = 0.18  # tax rate on revenue (GST)

# Shocks - Monthly probability
P_SHOCK = 0.05  # 5% probability each month
DELTA_PMF_SHOCK_MIN = -0.1
DELTA_PMF_SHOCK_MAX = 0.15
DELTA_M_SHOCK_MIN = -0.05
DELTA_M_SHOCK_MAX = 0.1

# Success Definition
V_EXIT = 10_00_00_000  # 10 Crore minimum valuation for success
SUCCESS_PERCENTILE = 0.90  # Top 10% valuation percentile

# Quantity sold per customer (normalized)
Q_T = 10  # average quantity per adopting customer - increased from 1
