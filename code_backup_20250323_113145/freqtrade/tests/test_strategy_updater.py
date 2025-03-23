# pragma pylint: disable=missing-docstring, protected-access, invalid-name

import re
import shutil
from pathlib import Path

from freqtrade.commands.strategy_utils_commands import start_strategy_update
# REMOVED_UNUSED_CODE: from freqtrade.strategy.strategyupdater import StrategyUpdater
from tests.conftest import get_args


def test_strategy_updater_start(user_dir, capsys) -> None:
    # Effective test without mocks.
    teststrats = Path(__file__).parent / "strategy/strats"
    tmpdirp = Path(user_dir) / "strategies"
    tmpdirp.mkdir(parents=True, exist_ok=True)
    shutil.copy(teststrats / "strategy_test_v2.py", tmpdirp)
    old_code = (teststrats / "strategy_test_v2.py").read_text()

    args = ["strategy-updater", "--userdir", str(user_dir), "--strategy-list", "StrategyTestV2"]
    pargs = get_args(args)
    pargs["config"] = None

    start_strategy_update(pargs)

    assert Path(user_dir / "strategies_orig_updater").exists()
    # Backup file exists
    assert Path(user_dir / "strategies_orig_updater" / "strategy_test_v2.py").exists()
    # updated file exists
    new_file = tmpdirp / "strategy_test_v2.py"
    assert new_file.exists()
    new_code = new_file.read_text()
    assert "INTERFACE_VERSION = 3" in new_code
    assert "INTERFACE_VERSION = 2" in old_code
    captured = capsys.readouterr()

    assert "Conversion of strategy_test_v2.py started." in captured.out
    assert re.search(r"Conversion of strategy_test_v2\.py took .* seconds", captured.out)


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def test_strategy_updater_methods(default_conf, caplog) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     modified_code1 = instance_strategy_updater.update_code(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: class testClass(IStrategy):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_buy_trend():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_sell_trend():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def check_buy_timeout():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def check_sell_timeout():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def custom_sell():
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "populate_entry_trend" in modified_code1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "populate_exit_trend" in modified_code1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "check_entry_timeout" in modified_code1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "check_exit_timeout" in modified_code1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "custom_exit" in modified_code1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "INTERFACE_VERSION = 3" in modified_code1


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def test_strategy_updater_params(default_conf, caplog) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     modified_code2 = instance_strategy_updater.update_code(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: ticker_interval = '15m'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: buy_some_parameter = IntParameter(space='buy')
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: sell_some_parameter = IntParameter(space='sell')
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "timeframe" in modified_code2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     # check for not editing hyperopt spaces
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "space='buy'" in modified_code2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "space='sell'" in modified_code2


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def test_strategy_updater_constants(default_conf, caplog) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     modified_code3 = instance_strategy_updater.update_code(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: use_sell_signal = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: sell_profit_only = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: sell_profit_offset = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: ignore_roi_if_buy_signal = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: forcebuy_enable = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "use_exit_signal" in modified_code3
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "exit_profit_only" in modified_code3
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "exit_profit_offset" in modified_code3
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "ignore_roi_if_entry_signal" in modified_code3
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "force_entry_enable" in modified_code3


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def test_strategy_updater_df_columns(default_conf, caplog) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     modified_code = instance_strategy_updater.update_code(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: dataframe.loc[reduce(lambda x, y: x & y, conditions), ["buy", "buy_tag"]] = (1, "buy_signal_1")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: dataframe.loc[reduce(lambda x, y: x & y, conditions), 'sell'] = 1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "enter_long" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "exit_long" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "enter_tag" in modified_code


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def test_strategy_updater_method_params(default_conf, caplog) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     modified_code = instance_strategy_updater.update_code(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def confirm_trade_exit(sell_reason: str):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     nr_orders = trade.nr_of_successful_buys
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "exit_reason" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "nr_orders = trade.nr_of_successful_entries" in modified_code


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def test_strategy_updater_dicts(default_conf, caplog) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     modified_code = instance_strategy_updater.update_code(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: order_time_in_force = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     'buy': 'gtc',
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     'sell': 'ioc'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: order_types = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     'buy': 'limit',
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     'sell': 'market',
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     'stoploss': 'market',
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     'stoploss_on_exchange': False
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: unfilledtimeout = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     'buy': 1,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     'sell': 2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "'entry': 'gtc'" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "'exit': 'ioc'" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "'entry': 'limit'" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "'exit': 'market'" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "'entry': 1" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "'exit': 2" in modified_code


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def test_strategy_updater_comparisons(default_conf, caplog) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     modified_code = instance_strategy_updater.update_code(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def confirm_trade_exit(sell_reason):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     if (sell_reason == 'stop_loss'):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pass
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "exit_reason" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "exit_reason == 'stop_loss'" in modified_code


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def test_strategy_updater_strings(default_conf, caplog) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     modified_code = instance_strategy_updater.update_code(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: sell_reason == 'sell_signal'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: sell_reason == 'force_sell'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: sell_reason == 'emergency_sell'
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     # those tests currently don't work, next in line.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "exit_signal" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "exit_reason" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "force_exit" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "emergency_exit" in modified_code


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def test_strategy_updater_comments(default_conf, caplog) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     instance_strategy_updater = StrategyUpdater()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     modified_code = instance_strategy_updater.update_code(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # This is the 1st comment
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: import talib.abstract as ta
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # This is the 2nd comment
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: import freqtrade.vendor.qtpylib.indicators as qtpylib
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: class someStrategy(IStrategy):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     INTERFACE_VERSION = 2
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     # This is the 3rd comment
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     # This attribute will be overridden if the config file contains "minimal_roi"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     minimal_roi = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "0": 0.50
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     # This is the 4th comment
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     stoploss = -0.1
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "This is the 1st comment" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "This is the 2nd comment" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "This is the 3rd comment" in modified_code
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     assert "INTERFACE_VERSION = 3" in modified_code
    # currently still missing:
    # Webhook terminology, Telegram notification settings, Strategy/Config settings
