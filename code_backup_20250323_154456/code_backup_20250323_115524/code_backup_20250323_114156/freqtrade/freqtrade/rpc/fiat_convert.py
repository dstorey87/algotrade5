"""
Module that define classes to convert Crypto-currency to FIAT
e.g BTC to USD
"""

import logging
from datetime import datetime
from typing import Any

from cachetools import TTLCache
from requests.exceptions import RequestException

from freqtrade.constants import SUPPORTED_FIAT, Config
from freqtrade.mixins.logging_mixin import LoggingMixin
from freqtrade.util.coin_gecko import FtCoinGeckoApi


logger = logging.getLogger(__name__)


# Manually map symbol to ID for some common coins
# with duplicate coingecko entries
coingecko_mapping = {
    "eth": "ethereum",
    "bnb": "binancecoin",
    "sol": "solana",
    "usdt": "tether",
    "busd": "binance-usd",
    "tusd": "true-usd",
    "usdc": "usd-coin",
    "btc": "bitcoin",
}


# REMOVED_UNUSED_CODE: class CryptoToFiatConverter(LoggingMixin):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Main class to initiate Crypto to FIAT.
# REMOVED_UNUSED_CODE:     This object contains a list of pair Crypto, FIAT
# REMOVED_UNUSED_CODE:     This object is also a Singleton
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     __instance = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     _coinlistings: list[dict] = []
# REMOVED_UNUSED_CODE:     _backoff: float = 0.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def __new__(cls, *args: Any, **kwargs: Any) -> Any:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Singleton pattern to ensure only one instance is created.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not cls.__instance:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             cls.__instance = super().__new__(cls)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return cls.__instance
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config) -> None:
# REMOVED_UNUSED_CODE:         # Timeout: 6h
# REMOVED_UNUSED_CODE:         self._pair_price: TTLCache = TTLCache(maxsize=500, ttl=6 * 60 * 60)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         _coingecko_config = config.get("coingecko", {})
# REMOVED_UNUSED_CODE:         self._coingecko = FtCoinGeckoApi(
# REMOVED_UNUSED_CODE:             api_key=_coingecko_config.get("api_key", ""),
# REMOVED_UNUSED_CODE:             is_demo=_coingecko_config.get("is_demo", True),
# REMOVED_UNUSED_CODE:             retries=1,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         LoggingMixin.__init__(self, logger, 3600)
# REMOVED_UNUSED_CODE:         self._load_cryptomap()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _load_cryptomap(self) -> None:
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             # Use list-comprehension to ensure we get a list.
# REMOVED_UNUSED_CODE:             self._coinlistings = [x for x in self._coingecko.get_coins_list()]
# REMOVED_UNUSED_CODE:         except RequestException as request_exception:
# REMOVED_UNUSED_CODE:             if "429" in str(request_exception):
# REMOVED_UNUSED_CODE:                 logger.warning(
# REMOVED_UNUSED_CODE:                     "Too many requests for CoinGecko API, backing off and trying again later."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 # Set backoff timestamp to 60 seconds in the future
# REMOVED_UNUSED_CODE:                 self._backoff = datetime.now().timestamp() + 60
# REMOVED_UNUSED_CODE:                 return
# REMOVED_UNUSED_CODE:             # If the request is not a 429 error we want to raise the normal error
# REMOVED_UNUSED_CODE:             logger.error(
# REMOVED_UNUSED_CODE:                 "Could not load FIAT Cryptocurrency map for the following problem: "
# REMOVED_UNUSED_CODE:                 f"{request_exception}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         except Exception as exception:
# REMOVED_UNUSED_CODE:             logger.error(
# REMOVED_UNUSED_CODE:                 f"Could not load FIAT Cryptocurrency map for the following problem: {exception}"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _get_gecko_id(self, crypto_symbol):
# REMOVED_UNUSED_CODE:         if not self._coinlistings:
# REMOVED_UNUSED_CODE:             if self._backoff <= datetime.now().timestamp():
# REMOVED_UNUSED_CODE:                 self._load_cryptomap()
# REMOVED_UNUSED_CODE:                 # Still not loaded.
# REMOVED_UNUSED_CODE:                 if not self._coinlistings:
# REMOVED_UNUSED_CODE:                     return None
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 return None
# REMOVED_UNUSED_CODE:         found = [x for x in self._coinlistings if x["symbol"].lower() == crypto_symbol]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if crypto_symbol in coingecko_mapping.keys():
# REMOVED_UNUSED_CODE:             found = [x for x in self._coinlistings if x["id"] == coingecko_mapping[crypto_symbol]]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(found) == 1:
# REMOVED_UNUSED_CODE:             return found[0]["id"]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if len(found) > 0:
# REMOVED_UNUSED_CODE:             # Wrong!
# REMOVED_UNUSED_CODE:             logger.warning(f"Found multiple mappings in CoinGecko for {crypto_symbol}.")
# REMOVED_UNUSED_CODE:             return None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def convert_amount(self, crypto_amount: float, crypto_symbol: str, fiat_symbol: str) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Convert an amount of crypto-currency to fiat
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param crypto_amount: amount of crypto-currency to convert
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param crypto_symbol: crypto-currency used
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param fiat_symbol: fiat to convert to
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: float, value in fiat of the crypto-currency amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if crypto_symbol == fiat_symbol:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return float(crypto_amount)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         price = self.get_price(crypto_symbol=crypto_symbol, fiat_symbol=fiat_symbol)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return float(crypto_amount) * float(price)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_price(self, crypto_symbol: str, fiat_symbol: str) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Return the price of the Crypto-currency in Fiat
# REMOVED_UNUSED_CODE:         :param crypto_symbol: Crypto-currency you want to convert (e.g BTC)
# REMOVED_UNUSED_CODE:         :param fiat_symbol: FIAT currency you want to convert to (e.g USD)
# REMOVED_UNUSED_CODE:         :return: Price in FIAT
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         crypto_symbol = crypto_symbol.lower()
# REMOVED_UNUSED_CODE:         fiat_symbol = fiat_symbol.lower()
# REMOVED_UNUSED_CODE:         inverse = False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if crypto_symbol == "usd":
# REMOVED_UNUSED_CODE:             # usd corresponds to "uniswap-state-dollar" for coingecko.
# REMOVED_UNUSED_CODE:             # We'll therefore need to "swap" the currencies
# REMOVED_UNUSED_CODE:             logger.info(f"reversing Rates {crypto_symbol}, {fiat_symbol}")
# REMOVED_UNUSED_CODE:             crypto_symbol = fiat_symbol
# REMOVED_UNUSED_CODE:             fiat_symbol = "usd"
# REMOVED_UNUSED_CODE:             inverse = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         symbol = f"{crypto_symbol}/{fiat_symbol}"
# REMOVED_UNUSED_CODE:         # Check if the fiat conversion you want is supported
# REMOVED_UNUSED_CODE:         if not self._is_supported_fiat(fiat=fiat_symbol):
# REMOVED_UNUSED_CODE:             raise ValueError(f"The fiat {fiat_symbol} is not supported.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         price = self._pair_price.get(symbol, None)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not price:
# REMOVED_UNUSED_CODE:             price = self._find_price(crypto_symbol=crypto_symbol, fiat_symbol=fiat_symbol)
# REMOVED_UNUSED_CODE:             if inverse and price != 0.0:
# REMOVED_UNUSED_CODE:                 price = 1 / price
# REMOVED_UNUSED_CODE:             self._pair_price[symbol] = price
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return price
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _is_supported_fiat(self, fiat: str) -> bool:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if the FIAT your want to convert to is supported
# REMOVED_UNUSED_CODE:         :param fiat: FIAT to check (e.g USD)
# REMOVED_UNUSED_CODE:         :return: bool, True supported, False not supported
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return fiat.upper() in SUPPORTED_FIAT
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _find_price(self, crypto_symbol: str, fiat_symbol: str) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Call CoinGecko API to retrieve the price in the FIAT
# REMOVED_UNUSED_CODE:         :param crypto_symbol: Crypto-currency you want to convert (e.g btc)
# REMOVED_UNUSED_CODE:         :param fiat_symbol: FIAT currency you want to convert to (e.g usd)
# REMOVED_UNUSED_CODE:         :return: float, price of the crypto-currency in Fiat
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Check if the fiat conversion you want is supported
# REMOVED_UNUSED_CODE:         if not self._is_supported_fiat(fiat=fiat_symbol):
# REMOVED_UNUSED_CODE:             raise ValueError(f"The fiat {fiat_symbol} is not supported.")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # No need to convert if both crypto and fiat are the same
# REMOVED_UNUSED_CODE:         if crypto_symbol == fiat_symbol:
# REMOVED_UNUSED_CODE:             return 1.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         _gecko_id = self._get_gecko_id(crypto_symbol)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if not _gecko_id:
# REMOVED_UNUSED_CODE:             # return 0 for unsupported stake currencies (fiat-convert should not break the bot)
# REMOVED_UNUSED_CODE:             self.log_once(
# REMOVED_UNUSED_CODE:                 f"unsupported crypto-symbol {crypto_symbol.upper()} - returning 0.0", logger.warning
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             return 0.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             return float(
# REMOVED_UNUSED_CODE:                 self._coingecko.get_price(ids=_gecko_id, vs_currencies=fiat_symbol)[_gecko_id][
# REMOVED_UNUSED_CODE:                     fiat_symbol
# REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         except Exception as exception:
# REMOVED_UNUSED_CODE:             logger.error("Error in _find_price: %s", exception)
# REMOVED_UNUSED_CODE:             return 0.0
