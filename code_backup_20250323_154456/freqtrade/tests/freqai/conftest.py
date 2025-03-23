import sys
from copy import deepcopy
from pathlib import Path
# REMOVED_UNUSED_CODE: from typing import Any
# REMOVED_UNUSED_CODE: from unittest.mock import MagicMock

import pytest

# REMOVED_UNUSED_CODE: from freqtrade.configuration import TimeRange
# REMOVED_UNUSED_CODE: from freqtrade.data.dataprovider import DataProvider
# REMOVED_UNUSED_CODE: from freqtrade.freqai.data_drawer import FreqaiDataDrawer
# REMOVED_UNUSED_CODE: from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
# REMOVED_UNUSED_CODE: from freqtrade.resolvers import StrategyResolver
# REMOVED_UNUSED_CODE: from freqtrade.resolvers.freqaimodel_resolver import FreqaiModelResolver
# REMOVED_UNUSED_CODE: from tests.conftest import get_patched_exchange


# REMOVED_UNUSED_CODE: def is_py12() -> bool:
# REMOVED_UNUSED_CODE:     return sys.version_info >= (3, 12)


# REMOVED_UNUSED_CODE: @pytest.fixture(scope="function")
# REMOVED_UNUSED_CODE: def freqai_conf(default_conf, tmp_path):
# REMOVED_UNUSED_CODE:     freqaiconf = deepcopy(default_conf)
# REMOVED_UNUSED_CODE:     freqaiconf.update(
# REMOVED_UNUSED_CODE:         {
# REMOVED_UNUSED_CODE:             "datadir": Path(default_conf["datadir"]),
# REMOVED_UNUSED_CODE:             "runmode": "backtest",
# REMOVED_UNUSED_CODE:             "strategy": "freqai_test_strat",
# REMOVED_UNUSED_CODE:             "user_data_dir": tmp_path,
# REMOVED_UNUSED_CODE:             "strategy-path": "freqtrade/tests/strategy/strats",
# REMOVED_UNUSED_CODE:             "freqaimodel": "LightGBMRegressor",
# REMOVED_UNUSED_CODE:             "freqaimodel_path": "freqai/prediction_models",
# REMOVED_UNUSED_CODE:             "timerange": "20180110-20180115",
# REMOVED_UNUSED_CODE:             "freqai": {
# REMOVED_UNUSED_CODE:                 "enabled": True,
# REMOVED_UNUSED_CODE:                 "purge_old_models": 2,
# REMOVED_UNUSED_CODE:                 "train_period_days": 2,
# REMOVED_UNUSED_CODE:                 "backtest_period_days": 10,
# REMOVED_UNUSED_CODE:                 "live_retrain_hours": 0,
# REMOVED_UNUSED_CODE:                 "expiration_hours": 1,
# REMOVED_UNUSED_CODE:                 "identifier": "unique-id100",
# REMOVED_UNUSED_CODE:                 "live_trained_timestamp": 0,
# REMOVED_UNUSED_CODE:                 "data_kitchen_thread_count": 2,
# REMOVED_UNUSED_CODE:                 "activate_tensorboard": False,
# REMOVED_UNUSED_CODE:                 "feature_parameters": {
# REMOVED_UNUSED_CODE:                     "include_timeframes": ["5m"],
# REMOVED_UNUSED_CODE:                     "include_corr_pairlist": ["ADA/BTC"],
# REMOVED_UNUSED_CODE:                     "label_period_candles": 20,
# REMOVED_UNUSED_CODE:                     "include_shifted_candles": 1,
# REMOVED_UNUSED_CODE:                     "DI_threshold": 0.9,
# REMOVED_UNUSED_CODE:                     "weight_factor": 0.9,
# REMOVED_UNUSED_CODE:                     "principal_component_analysis": False,
# REMOVED_UNUSED_CODE:                     "use_SVM_to_remove_outliers": True,
# REMOVED_UNUSED_CODE:                     "stratify_training_data": 0,
# REMOVED_UNUSED_CODE:                     "indicator_periods_candles": [10],
# REMOVED_UNUSED_CODE:                     "shuffle_after_split": False,
# REMOVED_UNUSED_CODE:                     "buffer_train_data_candles": 0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "data_split_parameters": {"test_size": 0.33, "shuffle": False},
# REMOVED_UNUSED_CODE:                 "model_training_parameters": {"n_estimators": 100},
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "config_files": [Path("config_examples", "config_freqai.example.json")],
# REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     freqaiconf["exchange"].update({"pair_whitelist": ["ADA/BTC", "DASH/BTC", "ETH/BTC", "LTC/BTC"]})
# REMOVED_UNUSED_CODE:     return freqaiconf


# REMOVED_UNUSED_CODE: def make_rl_config(conf):
# REMOVED_UNUSED_CODE:     conf.update({"strategy": "freqai_rl_test_strat"})
# REMOVED_UNUSED_CODE:     conf["freqai"].update(
# REMOVED_UNUSED_CODE:         {"model_training_parameters": {"learning_rate": 0.00025, "gamma": 0.9, "verbose": 1}}
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     conf["freqai"]["rl_config"] = {
# REMOVED_UNUSED_CODE:         "train_cycles": 1,
# REMOVED_UNUSED_CODE:         "thread_count": 2,
# REMOVED_UNUSED_CODE:         "max_trade_duration_candles": 300,
# REMOVED_UNUSED_CODE:         "model_type": "PPO",
# REMOVED_UNUSED_CODE:         "policy_type": "MlpPolicy",
# REMOVED_UNUSED_CODE:         "max_training_drawdown_pct": 0.5,
# REMOVED_UNUSED_CODE:         "net_arch": [32, 32],
# REMOVED_UNUSED_CODE:         "model_reward_parameters": {"rr": 1, "profit_aim": 0.02, "win_reward_factor": 2},
# REMOVED_UNUSED_CODE:         "drop_ohlc_from_features": False,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return conf


# REMOVED_UNUSED_CODE: def mock_pytorch_mlp_model_training_parameters() -> dict[str, Any]:
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "learning_rate": 3e-4,
# REMOVED_UNUSED_CODE:         "trainer_kwargs": {
# REMOVED_UNUSED_CODE:             "n_steps": None,
# REMOVED_UNUSED_CODE:             "batch_size": 64,
# REMOVED_UNUSED_CODE:             "n_epochs": 1,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "model_kwargs": {
# REMOVED_UNUSED_CODE:             "hidden_dim": 32,
# REMOVED_UNUSED_CODE:             "dropout_percent": 0.2,
# REMOVED_UNUSED_CODE:             "n_layer": 1,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def get_patched_data_kitchen(mocker, freqaiconf):
# REMOVED_UNUSED_CODE:     dk = FreqaiDataKitchen(freqaiconf)
# REMOVED_UNUSED_CODE:     return dk


# REMOVED_UNUSED_CODE: def get_patched_data_drawer(mocker, freqaiconf):
# REMOVED_UNUSED_CODE:     # dd = mocker.patch('freqtrade.freqai.data_drawer', MagicMock())
# REMOVED_UNUSED_CODE:     dd = FreqaiDataDrawer(freqaiconf)
# REMOVED_UNUSED_CODE:     return dd


# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: def get_patched_freqai_strategy(mocker, freqaiconf):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy = StrategyResolver.load_strategy(freqaiconf)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy.ft_bot_start()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     return strategy


# REMOVED_UNUSED_CODE: def get_patched_freqaimodel(mocker, freqaiconf):
# REMOVED_UNUSED_CODE:     freqaimodel = FreqaiModelResolver.load_freqaimodel(freqaiconf)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return freqaimodel


# REMOVED_UNUSED_CODE: def make_unfiltered_dataframe(mocker, freqai_conf):
# REMOVED_UNUSED_CODE:     freqai_conf.update({"timerange": "20180110-20180130"})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     strategy = get_patched_freqai_strategy(mocker, freqai_conf)
# REMOVED_UNUSED_CODE:     exchange = get_patched_exchange(mocker, freqai_conf)
# REMOVED_UNUSED_CODE:     strategy.dp = DataProvider(freqai_conf, exchange)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy.freqai_info = freqai_conf.get("freqai", {})
# REMOVED_UNUSED_CODE:     freqai = strategy.freqai
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai.live = True
# REMOVED_UNUSED_CODE:     freqai.dk = FreqaiDataKitchen(freqai_conf)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai.dk.live = True
# REMOVED_UNUSED_CODE:     freqai.dk.pair = "ADA/BTC"
# REMOVED_UNUSED_CODE:     data_load_timerange = TimeRange.parse_timerange("20180110-20180130")
# REMOVED_UNUSED_CODE:     freqai.dd.load_all_pair_histories(data_load_timerange, freqai.dk)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai.dd.pair_dict = MagicMock()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     new_timerange = TimeRange.parse_timerange("20180120-20180130")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     corr_dataframes, base_dataframes = freqai.dd.get_base_and_corr_dataframes(
# REMOVED_UNUSED_CODE:         data_load_timerange, freqai.dk.pair, freqai.dk
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     unfiltered_dataframe = freqai.dk.use_strategy_to_populate_indicators(
# REMOVED_UNUSED_CODE:         strategy, corr_dataframes, base_dataframes, freqai.dk.pair
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     for i in range(5):
# REMOVED_UNUSED_CODE:         unfiltered_dataframe[f"constant_{i}"] = i
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     unfiltered_dataframe = freqai.dk.slice_dataframe(new_timerange, unfiltered_dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return freqai, unfiltered_dataframe


# REMOVED_UNUSED_CODE: def make_data_dictionary(mocker, freqai_conf):
# REMOVED_UNUSED_CODE:     freqai_conf.update({"timerange": "20180110-20180130"})
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     strategy = get_patched_freqai_strategy(mocker, freqai_conf)
# REMOVED_UNUSED_CODE:     exchange = get_patched_exchange(mocker, freqai_conf)
# REMOVED_UNUSED_CODE:     strategy.dp = DataProvider(freqai_conf, exchange)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy.freqai_info = freqai_conf.get("freqai", {})
# REMOVED_UNUSED_CODE:     freqai = strategy.freqai
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai.live = True
# REMOVED_UNUSED_CODE:     freqai.dk = FreqaiDataKitchen(freqai_conf)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai.dk.live = True
# REMOVED_UNUSED_CODE:     freqai.dk.pair = "ADA/BTC"
# REMOVED_UNUSED_CODE:     data_load_timerange = TimeRange.parse_timerange("20180110-20180130")
# REMOVED_UNUSED_CODE:     freqai.dd.load_all_pair_histories(data_load_timerange, freqai.dk)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai.dd.pair_dict = MagicMock()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     new_timerange = TimeRange.parse_timerange("20180120-20180130")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     corr_dataframes, base_dataframes = freqai.dd.get_base_and_corr_dataframes(
# REMOVED_UNUSED_CODE:         data_load_timerange, freqai.dk.pair, freqai.dk
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     unfiltered_dataframe = freqai.dk.use_strategy_to_populate_indicators(
# REMOVED_UNUSED_CODE:         strategy, corr_dataframes, base_dataframes, freqai.dk.pair
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     unfiltered_dataframe = freqai.dk.slice_dataframe(new_timerange, unfiltered_dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     freqai.dk.find_features(unfiltered_dataframe)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     features_filtered, labels_filtered = freqai.dk.filter_features(
# REMOVED_UNUSED_CODE:         unfiltered_dataframe,
# REMOVED_UNUSED_CODE:         freqai.dk.training_features_list,
# REMOVED_UNUSED_CODE:         freqai.dk.label_list,
# REMOVED_UNUSED_CODE:         training_filter=True,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     data_dictionary = freqai.dk.make_train_test_datasets(features_filtered, labels_filtered)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     data_dictionary = freqai.dk.normalize_data(data_dictionary)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return freqai


# REMOVED_UNUSED_CODE: def get_freqai_live_analyzed_dataframe(mocker, freqaiconf):
# REMOVED_UNUSED_CODE:     strategy = get_patched_freqai_strategy(mocker, freqaiconf)
# REMOVED_UNUSED_CODE:     exchange = get_patched_exchange(mocker, freqaiconf)
# REMOVED_UNUSED_CODE:     strategy.dp = DataProvider(freqaiconf, exchange)
# REMOVED_UNUSED_CODE:     freqai = strategy.freqai
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai.live = True
# REMOVED_UNUSED_CODE:     freqai.dk = FreqaiDataKitchen(freqaiconf, freqai.dd)
# REMOVED_UNUSED_CODE:     timerange = TimeRange.parse_timerange("20180110-20180114")
# REMOVED_UNUSED_CODE:     freqai.dk.load_all_pair_histories(timerange)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     strategy.analyze_pair("ADA/BTC", "5m")
# REMOVED_UNUSED_CODE:     return strategy.dp.get_analyzed_dataframe("ADA/BTC", "5m")


# REMOVED_UNUSED_CODE: def get_freqai_analyzed_dataframe(mocker, freqaiconf):
# REMOVED_UNUSED_CODE:     strategy = get_patched_freqai_strategy(mocker, freqaiconf)
# REMOVED_UNUSED_CODE:     exchange = get_patched_exchange(mocker, freqaiconf)
# REMOVED_UNUSED_CODE:     strategy.dp = DataProvider(freqaiconf, exchange)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy.freqai_info = freqaiconf.get("freqai", {})
# REMOVED_UNUSED_CODE:     freqai = strategy.freqai
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai.live = True
# REMOVED_UNUSED_CODE:     freqai.dk = FreqaiDataKitchen(freqaiconf, freqai.dd)
# REMOVED_UNUSED_CODE:     timerange = TimeRange.parse_timerange("20180110-20180114")
# REMOVED_UNUSED_CODE:     freqai.dk.load_all_pair_histories(timerange)
# REMOVED_UNUSED_CODE:     sub_timerange = TimeRange.parse_timerange("20180111-20180114")
# REMOVED_UNUSED_CODE:     corr_df, base_df = freqai.dk.get_base_and_corr_dataframes(sub_timerange, "LTC/BTC")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return freqai.dk.use_strategy_to_populate_indicators(strategy, corr_df, base_df, "LTC/BTC")


# REMOVED_UNUSED_CODE: def get_ready_to_train(mocker, freqaiconf):
# REMOVED_UNUSED_CODE:     strategy = get_patched_freqai_strategy(mocker, freqaiconf)
# REMOVED_UNUSED_CODE:     exchange = get_patched_exchange(mocker, freqaiconf)
# REMOVED_UNUSED_CODE:     strategy.dp = DataProvider(freqaiconf, exchange)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     strategy.freqai_info = freqaiconf.get("freqai", {})
# REMOVED_UNUSED_CODE:     freqai = strategy.freqai
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     freqai.live = True
# REMOVED_UNUSED_CODE:     freqai.dk = FreqaiDataKitchen(freqaiconf, freqai.dd)
# REMOVED_UNUSED_CODE:     timerange = TimeRange.parse_timerange("20180110-20180114")
# REMOVED_UNUSED_CODE:     freqai.dk.load_all_pair_histories(timerange)
# REMOVED_UNUSED_CODE:     sub_timerange = TimeRange.parse_timerange("20180111-20180114")
# REMOVED_UNUSED_CODE:     corr_df, base_df = freqai.dk.get_base_and_corr_dataframes(sub_timerange, "LTC/BTC")
# REMOVED_UNUSED_CODE:     return corr_df, base_df, freqai, strategy
