import logging
from typing import Any

from pandas import DataFrame
from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
from sb3_contrib.common.maskable.utils import is_masking_supported
from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor

from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner
from freqtrade.freqai.RL.BaseReinforcementLearningModel import make_env
from freqtrade.freqai.tensorboard.TensorboardCallback import TensorboardCallback


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: class ReinforcementLearner_multiproc(ReinforcementLearner):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Demonstration of how to build vectorized environments
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def set_train_and_eval_environments(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         data_dictionary: dict[str, Any],
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         prices_train: DataFrame,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         prices_test: DataFrame,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         dk: FreqaiDataKitchen,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         User can override this if they are using a custom MyRLEnv
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param data_dictionary: dict = common data dictionary containing train and test
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             features/labels/weights.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param prices_train/test: DataFrame = dataframe comprised of the prices to be used in
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             the environment during training
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         or testing
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param dk: FreqaiDataKitchen = the datakitchen for the current pair
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         train_df = data_dictionary["train_features"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         test_df = data_dictionary["test_features"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.train_env:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.train_env.close()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self.eval_env:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.eval_env.close()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         env_info = self.pack_env_dict(dk.pair)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         eval_freq = len(train_df) // self.max_threads
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         env_id = "train_env"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.train_env = VecMonitor(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             SubprocVecEnv(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     make_env(self.MyRLEnv, env_id, i, 1, train_df, prices_train, env_info=env_info)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     for i in range(self.max_threads)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         eval_env_id = "eval_env"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.eval_env = VecMonitor(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             SubprocVecEnv(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 [
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     make_env(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                         self.MyRLEnv, eval_env_id, i, 1, test_df, prices_test, env_info=env_info
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     for i in range(self.max_threads)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.eval_callback = MaskableEvalCallback(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.eval_env,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             deterministic=True,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             render=False,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             eval_freq=eval_freq,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             best_model_save_path=str(dk.data_path),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             use_masking=(self.model_type == "MaskablePPO" and is_masking_supported(self.eval_env)),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # TENSORBOARD CALLBACK DOES NOT RECOMMENDED TO USE WITH MULTIPLE ENVS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # IT WILL RETURN FALSE INFORMATION, NEVERTHELESS NOT THREAD SAFE WITH SB3!!!
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         actions = self.train_env.env_method("get_actions")[0]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.tensorboard_callback = TensorboardCallback(verbose=1, actions=actions)
