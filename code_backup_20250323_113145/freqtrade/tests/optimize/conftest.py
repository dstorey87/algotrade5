from copy import deepcopy
# REMOVED_UNUSED_CODE: from datetime import datetime
from pathlib import Path

# REMOVED_UNUSED_CODE: import pandas as pd
import pytest

# REMOVED_UNUSED_CODE: from freqtrade.enums import ExitType, RunMode
# REMOVED_UNUSED_CODE: from freqtrade.optimize.backtesting import Backtesting
# REMOVED_UNUSED_CODE: from freqtrade.optimize.hyperopt import Hyperopt
# REMOVED_UNUSED_CODE: from tests.conftest import patch_exchange


# REMOVED_UNUSED_CODE: @pytest.fixture(scope="function")
def hyperopt_conf(default_conf):
    hyperconf = deepcopy(default_conf)
    hyperconf.update(
        {
            "datadir": Path(default_conf["datadir"]),
            "runmode": RunMode.HYPEROPT,
            "strategy": "HyperoptableStrategy",
            "hyperopt_loss": "ShortTradeDurHyperOptLoss",
            "hyperopt_path": str(Path(__file__).parent / "hyperopts"),
            "epochs": 1,
            "timerange": None,
            "spaces": ["default"],
            "hyperopt_jobs": 1,
            "hyperopt_min_trades": 1,
        }
    )
    return hyperconf


# REMOVED_UNUSED_CODE: @pytest.fixture(autouse=True)
# REMOVED_UNUSED_CODE: def backtesting_cleanup():
# REMOVED_UNUSED_CODE:     yield None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Backtesting.cleanup()


# REMOVED_UNUSED_CODE: @pytest.fixture(scope="function")
# REMOVED_UNUSED_CODE: def hyperopt(hyperopt_conf, mocker):
# REMOVED_UNUSED_CODE:     patch_exchange(mocker)
# REMOVED_UNUSED_CODE:     return Hyperopt(hyperopt_conf)


# REMOVED_UNUSED_CODE: @pytest.fixture(scope="function")
# REMOVED_UNUSED_CODE: def hyperopt_results():
# REMOVED_UNUSED_CODE:     return pd.DataFrame(
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "pair": ["ETH/USDT", "ETH/USDT", "ETH/USDT", "ETH/USDT"],
# REMOVED_UNUSED_CODE:             "profit_ratio": [-0.1, 0.2, -0.12, 0.3],
# REMOVED_UNUSED_CODE:             "profit_abs": [-0.2, 0.4, -0.21, 0.6],
# REMOVED_UNUSED_CODE:             "trade_duration": [10, 30, 10, 10],
# REMOVED_UNUSED_CODE:             "amount": [0.1, 0.1, 0.1, 0.1],
# REMOVED_UNUSED_CODE:             "exit_reason": [ExitType.STOP_LOSS, ExitType.ROI, ExitType.STOP_LOSS, ExitType.ROI],
# REMOVED_UNUSED_CODE:             "open_date": [
# REMOVED_UNUSED_CODE:                 datetime(2019, 1, 1, 9, 15, 0),
# REMOVED_UNUSED_CODE:                 datetime(2019, 1, 2, 8, 55, 0),
# REMOVED_UNUSED_CODE:                 datetime(2019, 1, 3, 9, 15, 0),
# REMOVED_UNUSED_CODE:                 datetime(2019, 1, 4, 9, 15, 0),
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:             "close_date": [
# REMOVED_UNUSED_CODE:                 datetime(2019, 1, 1, 9, 25, 0),
# REMOVED_UNUSED_CODE:                 datetime(2019, 1, 2, 9, 25, 0),
# REMOVED_UNUSED_CODE:                 datetime(2019, 1, 3, 9, 25, 0),
# REMOVED_UNUSED_CODE:                 datetime(2019, 1, 4, 9, 25, 0),
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     )
