from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider
from mesa.visualization.modules import ChartModule

from app import StartupFundingModel, MODEL_PARAMS

# -----------------------
# Charts (React frontend)
# -----------------------
charts = [
    ChartModule(
        [
            {"Label": "total_startup_funding", "Color": "Blue"},
            {"Label": "foreign_capital_inflow", "Color": "Green"},
        ],
        data_collector_name="datacollector"
    ),
    ChartModule(
        [
            {"Label": "avg_valuation", "Color": "Purple"},
            {"Label": "startup_failure_rate", "Color": "Red"},
        ],
        data_collector_name="datacollector"
    ),
    ChartModule(
        [
            {"Label": "avg_loan_rate", "Color": "Orange"},
            {"Label": "investor_portfolio_shift", "Color": "Black"},
        ],
        data_collector_name="datacollector"
    ),
]

# -----------------------
# Sliders (Policy Inputs)
# -----------------------
model_params = {
    "repo": Slider(
        "Repo Rate (%)",
        MODEL_PARAMS["repo"],
        3.0, 10.0, 0.25
    ),
    "rev_repo": Slider(
        "Reverse Repo (%)",
        MODEL_PARAMS["rev_repo"],
        2.0, 9.0, 0.25
    ),
    "msf": Slider(
        "MSF Rate (%)",
        MODEL_PARAMS["msf"],
        4.0, 12.0, 0.25
    ),
    "crr": Slider(
        "CRR (%)",
        MODEL_PARAMS["crr"],
        2.0, 8.0, 0.25
    ),
    "slr": Slider(
        "SLR (%)",
        MODEL_PARAMS["slr"],
        15.0, 25.0, 0.5
    ),
    "r_global": Slider(
        "Global Interest Rate (%)",
        MODEL_PARAMS["r_global"],
        0.0, 6.0, 0.25
    ),
    "gov_support_level": Slider(
        "Government Startup Support",
        MODEL_PARAMS["gov_support_level"],
        0.0, 200.0, 10.0
    ),
}

# -----------------------
# Server
# -----------------------
server = ModularServer(
    StartupFundingModel,
    charts,
    "Monetary Policy → Startup Funding (ABM)",
    model_params
)

server.port = 8521

if __name__ == "__main__":
    server.launch()

