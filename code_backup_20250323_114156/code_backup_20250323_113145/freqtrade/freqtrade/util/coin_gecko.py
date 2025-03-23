# REMOVED_UNUSED_CODE: from pycoingecko import CoinGeckoAPI


# REMOVED_UNUSED_CODE: class FtCoinGeckoApi(CoinGeckoAPI):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Simple wrapper around pycoingecko's api to support Demo API keys.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, api_key: str = "", *, is_demo=True, retries=5):
# REMOVED_UNUSED_CODE:         if api_key and is_demo:
# REMOVED_UNUSED_CODE:             super().__init__(retries=retries, demo_api_key=api_key)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             super().__init__(api_key=api_key, retries=retries)
