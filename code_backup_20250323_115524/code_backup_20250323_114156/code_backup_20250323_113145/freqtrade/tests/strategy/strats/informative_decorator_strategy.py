# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

from pandas import DataFrame

from freqtrade.strategy import IStrategy, informative, merge_informative_pair


class InformativeDecoratorTest(IStrategy):
    """
    Strategy used by tests freqtrade bot.
    Please do not modify this strategy, it's  intended for internal use only.
    Please look at the SampleStrategy in the user_data/strategy directory
    or strategy repository https://github.com/freqtrade/freqtrade-strategies
    for samples and inspiration.
    """

# REMOVED_UNUSED_CODE:     INTERFACE_VERSION = 2
# REMOVED_UNUSED_CODE:     stoploss = -0.10
    timeframe = "5m"
# REMOVED_UNUSED_CODE:     startup_candle_count: int = 20

# REMOVED_UNUSED_CODE:     def informative_pairs(self):
# REMOVED_UNUSED_CODE:         # Intentionally return 2 tuples, must be converted to 3 in compatibility code
# REMOVED_UNUSED_CODE:         return [
# REMOVED_UNUSED_CODE:             ("NEO/USDT", "5m"),
# REMOVED_UNUSED_CODE:             ("NEO/USDT", "15m", ""),
# REMOVED_UNUSED_CODE:             ("NEO/USDT", "2h", "futures"),
# REMOVED_UNUSED_CODE:         ]

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["buy"] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["sell"] = 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe

    # Decorator stacking test.
# REMOVED_UNUSED_CODE:     @informative("30m")
    @informative("1h")
# REMOVED_UNUSED_CODE:     def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         dataframe["rsi"] = 14
# REMOVED_UNUSED_CODE:         return dataframe

    # Simple informative test.
# REMOVED_UNUSED_CODE:     @informative("1h", "NEO/{stake}")
# REMOVED_UNUSED_CODE:     def populate_indicators_neo_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         dataframe["rsi"] = 14
# REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE:     @informative("1h", "{base}/BTC")
# REMOVED_UNUSED_CODE:     def populate_indicators_base_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         dataframe["rsi"] = 14
# REMOVED_UNUSED_CODE:         return dataframe

    # Quote currency different from stake currency test.
# REMOVED_UNUSED_CODE:     @informative("1h", "ETH/BTC", candle_type="spot")
# REMOVED_UNUSED_CODE:     def populate_indicators_eth_btc_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         dataframe["rsi"] = 14
# REMOVED_UNUSED_CODE:         return dataframe

    # Formatting test.
# REMOVED_UNUSED_CODE:     @informative("30m", "NEO/{stake}", "{column}_{BASE}_{QUOTE}_{base}_{quote}_{asset}_{timeframe}")
# REMOVED_UNUSED_CODE:     def populate_indicators_btc_1h_2(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         dataframe["rsi"] = 14
# REMOVED_UNUSED_CODE:         return dataframe

    # Custom formatter test
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @informative("30m", "ETH/{stake}", fmt=lambda column, **kwargs: column + "_from_callable")
# REMOVED_UNUSED_CODE:     def populate_indicators_eth_30m(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE:         dataframe["rsi"] = 14
# REMOVED_UNUSED_CODE:         return dataframe

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Strategy timeframe indicators for current pair.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["rsi"] = 14
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Informative pairs are available in this method.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe["rsi_less"] = dataframe["rsi"] < dataframe["rsi_1h"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Mixing manual informative pairs with decorators.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         informative = self.dp.get_pair_dataframe("NEO/USDT", "5m", "")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         informative["rsi"] = 14
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dataframe = merge_informative_pair(dataframe, informative, self.timeframe, "5m", ffill=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return dataframe
