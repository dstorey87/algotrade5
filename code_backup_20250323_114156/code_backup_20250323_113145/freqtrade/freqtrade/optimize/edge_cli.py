# pragma pylint: disable=missing-docstring, W0212, too-many-arguments

"""
This module contains the edge backtesting interface
"""

import logging

# REMOVED_UNUSED_CODE: from freqtrade import constants
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.configuration import TimeRange, validate_config_consistency
# REMOVED_UNUSED_CODE: from freqtrade.constants import Config
# REMOVED_UNUSED_CODE: from freqtrade.data.dataprovider import DataProvider
# REMOVED_UNUSED_CODE: from freqtrade.edge import Edge
# REMOVED_UNUSED_CODE: from freqtrade.optimize.optimize_reports import generate_edge_table
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.resolvers import ExchangeResolver, StrategyResolver


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class EdgeCli:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     EdgeCli class, this class contains all the logic to run edge backtesting
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     To run a edge backtest:
# REMOVED_UNUSED_CODE:     edge = EdgeCli(config)
# REMOVED_UNUSED_CODE:     edge.start()
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         self.config = config
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Ensure using dry-run
# REMOVED_UNUSED_CODE:         self.config["dry_run"] = True
# REMOVED_UNUSED_CODE:         self.config["stake_amount"] = constants.UNLIMITED_STAKE_AMOUNT
# REMOVED_UNUSED_CODE:         self.exchange = ExchangeResolver.load_exchange(self.config)
# REMOVED_UNUSED_CODE:         self.strategy = StrategyResolver.load_strategy(self.config)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.strategy.dp = DataProvider(config, self.exchange)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         validate_config_consistency(self.config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.edge = Edge(config, self.exchange, self.strategy)
# REMOVED_UNUSED_CODE:         # Set refresh_pairs to false for edge-cli (it must be true for edge)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.edge._refresh_pairs = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.edge._timerange = TimeRange.parse_timerange(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             None if self.config.get("timerange") is None else str(self.config.get("timerange"))
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         self.strategy.ft_bot_start()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def start(self) -> None:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         result = self.edge.calculate(self.config["exchange"]["pair_whitelist"])
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if result:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             print("")  # blank line for readability
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             generate_edge_table(self.edge._cached_pairs)
