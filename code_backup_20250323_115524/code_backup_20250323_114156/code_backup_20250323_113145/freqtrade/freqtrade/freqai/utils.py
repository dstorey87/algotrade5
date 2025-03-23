import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import rapidjson

from freqtrade.configuration import TimeRange
from freqtrade.constants import Config
from freqtrade.data.dataprovider import DataProvider
from freqtrade.data.history.history_utils import refresh_backtest_ohlcv_data
from freqtrade.exceptions import OperationalException
from freqtrade.exchange import timeframe_to_seconds
from freqtrade.freqai.data_drawer import FreqaiDataDrawer
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.plugins.pairlist.pairlist_helpers import dynamic_expand_pairlist


logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def download_all_data_for_training(dp: DataProvider, config: Config) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Called only once upon start of bot to download the necessary data for
# REMOVED_UNUSED_CODE:     populating indicators and training the model.
# REMOVED_UNUSED_CODE:     :param timerange: TimeRange = The full data timerange for populating the indicators
# REMOVED_UNUSED_CODE:                                     and training the model.
# REMOVED_UNUSED_CODE:     :param dp: DataProvider instance attached to the strategy
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if dp._exchange is None:
# REMOVED_UNUSED_CODE:         raise OperationalException("No exchange object found.")
# REMOVED_UNUSED_CODE:     markets = [
# REMOVED_UNUSED_CODE:         p
# REMOVED_UNUSED_CODE:         for p in dp._exchange.get_markets(
# REMOVED_UNUSED_CODE:             tradable_only=True, active_only=not config.get("include_inactive")
# REMOVED_UNUSED_CODE:         ).keys()
# REMOVED_UNUSED_CODE:     ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     all_pairs = dynamic_expand_pairlist(config, markets)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     timerange = get_required_data_timerange(config)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     new_pairs_days = int((timerange.stopts - timerange.startts) / 86400)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     refresh_backtest_ohlcv_data(
# REMOVED_UNUSED_CODE:         dp._exchange,
# REMOVED_UNUSED_CODE:         pairs=all_pairs,
# REMOVED_UNUSED_CODE:         timeframes=config["freqai"]["feature_parameters"].get("include_timeframes"),
# REMOVED_UNUSED_CODE:         datadir=config["datadir"],
# REMOVED_UNUSED_CODE:         timerange=timerange,
# REMOVED_UNUSED_CODE:         new_pairs_days=new_pairs_days,
# REMOVED_UNUSED_CODE:         erase=False,
# REMOVED_UNUSED_CODE:         data_format=config.get("dataformat_ohlcv", "feather"),
# REMOVED_UNUSED_CODE:         trading_mode=config.get("trading_mode", "spot"),
# REMOVED_UNUSED_CODE:         prepend=config.get("prepend_data", False),
# REMOVED_UNUSED_CODE:     )


def get_required_data_timerange(config: Config) -> TimeRange:
    """
    Used to compute the required data download time range
    for auto data-download in FreqAI
    """
    time = datetime.now(tz=timezone.utc).timestamp()

    timeframes = config["freqai"]["feature_parameters"].get("include_timeframes")

    max_tf_seconds = 0
    for tf in timeframes:
        secs = timeframe_to_seconds(tf)
        if secs > max_tf_seconds:
            max_tf_seconds = secs

    startup_candles = config.get("startup_candle_count", 0)
    indicator_periods = config["freqai"]["feature_parameters"]["indicator_periods_candles"]

    # factor the max_period as a factor of safety.
    max_period = int(max(startup_candles, max(indicator_periods)) * 1.5)
    config["startup_candle_count"] = max_period
    logger.info(f"FreqAI auto-downloader using {max_period} startup candles.")

    additional_seconds = max_period * max_tf_seconds

    startts = int(time - config["freqai"].get("train_period_days", 0) * 86400 - additional_seconds)
    stopts = int(time)
    data_load_timerange = TimeRange("date", "date", startts, stopts)

    return data_load_timerange


# REMOVED_UNUSED_CODE: def plot_feature_importance(
# REMOVED_UNUSED_CODE:     model: Any, pair: str, dk: FreqaiDataKitchen, count_max: int = 25
# REMOVED_UNUSED_CODE: ) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Plot Best and worst features by importance for a single sub-train.
# REMOVED_UNUSED_CODE:     :param model: Any = A model which was `fit` using a common library
# REMOVED_UNUSED_CODE:                         such as catboost or lightgbm
# REMOVED_UNUSED_CODE:     :param pair: str = pair e.g. BTC/USD
# REMOVED_UNUSED_CODE:     :param dk: FreqaiDataKitchen = non-persistent data container for current coin/loop
# REMOVED_UNUSED_CODE:     :param count_max: int = the amount of features to be loaded per column
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from freqtrade.plot.plotting import go, make_subplots, store_plot_file
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Extract feature importance from model
# REMOVED_UNUSED_CODE:     models = {}
# REMOVED_UNUSED_CODE:     if "FreqaiMultiOutputRegressor" in str(model.__class__):
# REMOVED_UNUSED_CODE:         for estimator, label in zip(model.estimators_, dk.label_list, strict=False):
# REMOVED_UNUSED_CODE:             models[label] = estimator
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         models[dk.label_list[0]] = model
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for label in models:
# REMOVED_UNUSED_CODE:         mdl = models[label]
# REMOVED_UNUSED_CODE:         if "catboost.core" in str(mdl.__class__):
# REMOVED_UNUSED_CODE:             feature_importance = mdl.get_feature_importance()
# REMOVED_UNUSED_CODE:         elif "lightgbm.sklearn" in str(mdl.__class__):
# REMOVED_UNUSED_CODE:             feature_importance = mdl.feature_importances_
# REMOVED_UNUSED_CODE:         elif "xgb" in str(mdl.__class__):
# REMOVED_UNUSED_CODE:             feature_importance = mdl.feature_importances_
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             logger.info("Model type does not support generating feature importances.")
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Data preparation
# REMOVED_UNUSED_CODE:         fi_df = pd.DataFrame(
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "feature_names": np.array(dk.data_dictionary["train_features"].columns),
# REMOVED_UNUSED_CODE:                 "feature_importance": np.array(feature_importance),
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         fi_df_top = fi_df.nlargest(count_max, "feature_importance")[::-1]
# REMOVED_UNUSED_CODE:         fi_df_worst = fi_df.nsmallest(count_max, "feature_importance")[::-1]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Plotting
# REMOVED_UNUSED_CODE:         def add_feature_trace(fig, fi_df, col):
# REMOVED_UNUSED_CODE:             return fig.add_trace(
# REMOVED_UNUSED_CODE:                 go.Bar(
# REMOVED_UNUSED_CODE:                     x=fi_df["feature_importance"],
# REMOVED_UNUSED_CODE:                     y=fi_df["feature_names"],
# REMOVED_UNUSED_CODE:                     orientation="h",
# REMOVED_UNUSED_CODE:                     showlegend=False,
# REMOVED_UNUSED_CODE:                 ),
# REMOVED_UNUSED_CODE:                 row=1,
# REMOVED_UNUSED_CODE:                 col=col,
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.5)
# REMOVED_UNUSED_CODE:         fig = add_feature_trace(fig, fi_df_top, 1)
# REMOVED_UNUSED_CODE:         fig = add_feature_trace(fig, fi_df_worst, 2)
# REMOVED_UNUSED_CODE:         fig.update_layout(title_text=f"Best and worst features by importance {pair}")
# REMOVED_UNUSED_CODE:         label = label.replace("&", "").replace("%", "")  # escape two FreqAI specific characters
# REMOVED_UNUSED_CODE:         store_plot_file(fig, f"{dk.model_filename}-{label}.html", dk.data_path)


# REMOVED_UNUSED_CODE: def record_params(config: dict[str, Any], full_path: Path) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Records run params in the full path for reproducibility
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     params_record_path = full_path / "run_params.json"
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     run_params = {
# REMOVED_UNUSED_CODE:         "freqai": config.get("freqai", {}),
# REMOVED_UNUSED_CODE:         "timeframe": config.get("timeframe"),
# REMOVED_UNUSED_CODE:         "stake_amount": config.get("stake_amount"),
# REMOVED_UNUSED_CODE:         "stake_currency": config.get("stake_currency"),
# REMOVED_UNUSED_CODE:         "max_open_trades": config.get("max_open_trades"),
# REMOVED_UNUSED_CODE:         "pairs": config.get("exchange", {}).get("pair_whitelist"),
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     with params_record_path.open("w") as handle:
# REMOVED_UNUSED_CODE:         rapidjson.dump(
# REMOVED_UNUSED_CODE:             run_params,
# REMOVED_UNUSED_CODE:             handle,
# REMOVED_UNUSED_CODE:             indent=4,
# REMOVED_UNUSED_CODE:             default=str,
# REMOVED_UNUSED_CODE:             number_mode=rapidjson.NM_NATIVE | rapidjson.NM_NAN,
# REMOVED_UNUSED_CODE:         )


def get_timerange_backtest_live_models(config: Config) -> str:
    """
    Returns a formatted timerange for backtest live/ready models
    :param config: Configuration dictionary

    :return: a string timerange (format example: '20220801-20220822')
    """
    dk = FreqaiDataKitchen(config)
    models_path = dk.get_full_models_path(config)
    dd = FreqaiDataDrawer(models_path, config)
    timerange = dd.get_timerange_from_live_historic_predictions()
    return timerange.timerange_str


# REMOVED_UNUSED_CODE: def get_tb_logger(model_type: str, path: Path, activate: bool) -> Any:
# REMOVED_UNUSED_CODE:     if model_type == "pytorch" and activate:
# REMOVED_UNUSED_CODE:         from freqtrade.freqai.tensorboard import TBLogger
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return TBLogger(path, activate)
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         from freqtrade.freqai.tensorboard.base_tensorboard import BaseTensorboardLogger
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return BaseTensorboardLogger(path, activate)
