# pragma pylint: disable=W0603
"""Wallet"""

import logging
from datetime import datetime, timedelta
from typing import Literal, NamedTuple

from freqtrade.constants import UNLIMITED_STAKE_AMOUNT, Config, IntOrInf
from freqtrade.enums import RunMode, TradingMode
from freqtrade.exceptions import DependencyException
from freqtrade.exchange import Exchange
from freqtrade.misc import safe_value_fallback
from freqtrade.persistence import LocalTrade, Trade
from freqtrade.util.datetime_helpers import dt_now


logger = logging.getLogger(__name__)


# wallet data structure
class Wallet(NamedTuple):
    currency: str
    free: float = 0
    used: float = 0
    total: float = 0


class PositionWallet(NamedTuple):
    symbol: str
    position: float = 0
    leverage: float | None = 0  # Don't use this - it's not guaranteed to be set
    collateral: float = 0
# REMOVED_UNUSED_CODE:     side: str = "long"


# REMOVED_UNUSED_CODE: class Wallets:
# REMOVED_UNUSED_CODE:     def __init__(self, config: Config, exchange: Exchange, is_backtest: bool = False) -> None:
# REMOVED_UNUSED_CODE:         self._config = config
# REMOVED_UNUSED_CODE:         self._is_backtest = is_backtest
# REMOVED_UNUSED_CODE:         self._exchange = exchange
# REMOVED_UNUSED_CODE:         self._wallets: dict[str, Wallet] = {}
# REMOVED_UNUSED_CODE:         self._positions: dict[str, PositionWallet] = {}
# REMOVED_UNUSED_CODE:         self._start_cap: dict[str, float] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._stake_currency = self._exchange.get_proxy_coin()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if isinstance(_start_cap := config["dry_run_wallet"], float | int):
# REMOVED_UNUSED_CODE:             self._start_cap[self._stake_currency] = _start_cap
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self._start_cap = _start_cap
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._last_wallet_refresh: datetime | None = None
# REMOVED_UNUSED_CODE:         self.update()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_free(self, currency: str) -> float:
# REMOVED_UNUSED_CODE:         balance = self._wallets.get(currency)
# REMOVED_UNUSED_CODE:         if balance and balance.free:
# REMOVED_UNUSED_CODE:             return balance.free
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_used(self, currency: str) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         balance = self._wallets.get(currency)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if balance and balance.used:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return balance.used
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_total(self, currency: str) -> float:
# REMOVED_UNUSED_CODE:         balance = self._wallets.get(currency)
# REMOVED_UNUSED_CODE:         if balance and balance.total:
# REMOVED_UNUSED_CODE:             return balance.total
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_collateral(self) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Get total collateral for liquidation price calculation.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._config.get("margin_mode") == "cross":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # free includes all balances and, combined with position collateral,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # is used as "wallet balance".
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return self.get_free(self._stake_currency) + sum(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pos.collateral for pos in self._positions.values()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self.get_total(self._stake_currency)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_owned(self, pair: str, base_currency: str) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Get currently owned value.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Designed to work across both spot and futures.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if self._config.get("trading_mode", "spot") != TradingMode.FUTURES:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return self.get_total(base_currency) or 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if pos := self._positions.get(pair):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return pos.position
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _update_dry(self) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Update from database in dry-run mode
# REMOVED_UNUSED_CODE:         - Apply profits of closed trades on top of stake amount
# REMOVED_UNUSED_CODE:         - Subtract currently tied up stake_amount in open trades
# REMOVED_UNUSED_CODE:         - update balances for currencies currently in trades
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         # Recreate _wallets to reset closed trade balances
# REMOVED_UNUSED_CODE:         _wallets = {}
# REMOVED_UNUSED_CODE:         _positions = {}
# REMOVED_UNUSED_CODE:         open_trades = Trade.get_trades_proxy(is_open=True)
# REMOVED_UNUSED_CODE:         if not self._is_backtest:
# REMOVED_UNUSED_CODE:             # Live / Dry-run mode
# REMOVED_UNUSED_CODE:             tot_profit = Trade.get_total_closed_profit()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Backtest mode
# REMOVED_UNUSED_CODE:             tot_profit = LocalTrade.bt_total_profit
# REMOVED_UNUSED_CODE:         tot_profit += sum(trade.realized_profit for trade in open_trades)
# REMOVED_UNUSED_CODE:         tot_in_trades = sum(trade.stake_amount for trade in open_trades)
# REMOVED_UNUSED_CODE:         used_stake = 0.0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._config.get("trading_mode", "spot") != TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:             for trade in open_trades:
# REMOVED_UNUSED_CODE:                 curr = self._exchange.get_pair_base_currency(trade.pair)
# REMOVED_UNUSED_CODE:                 used_stake += sum(
# REMOVED_UNUSED_CODE:                     o.stake_amount for o in trade.open_orders if o.ft_order_side == trade.entry_side
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 pending = sum(
# REMOVED_UNUSED_CODE:                     o.amount
# REMOVED_UNUSED_CODE:                     for o in trade.open_orders
# REMOVED_UNUSED_CODE:                     if o.amount and o.ft_order_side == trade.exit_side
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:                 curr_wallet_bal = self._start_cap.get(curr, 0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:                 _wallets[curr] = Wallet(
# REMOVED_UNUSED_CODE:                     curr,
# REMOVED_UNUSED_CODE:                     curr_wallet_bal + trade.amount - pending,
# REMOVED_UNUSED_CODE:                     pending,
# REMOVED_UNUSED_CODE:                     trade.amount + curr_wallet_bal,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             for position in open_trades:
# REMOVED_UNUSED_CODE:                 _positions[position.pair] = PositionWallet(
# REMOVED_UNUSED_CODE:                     position.pair,
# REMOVED_UNUSED_CODE:                     position=position.amount,
# REMOVED_UNUSED_CODE:                     leverage=position.leverage,
# REMOVED_UNUSED_CODE:                     collateral=position.stake_amount,
# REMOVED_UNUSED_CODE:                     side=position.trade_direction,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             used_stake = tot_in_trades
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         cross_margin = 0.0
# REMOVED_UNUSED_CODE:         if self._config.get("margin_mode") == "cross":
# REMOVED_UNUSED_CODE:             # In cross-margin mode, the total balance is used as collateral.
# REMOVED_UNUSED_CODE:             # This is moved as "free" into the stake currency balance.
# REMOVED_UNUSED_CODE:             # strongly tied to the get_collateral() implementation.
# REMOVED_UNUSED_CODE:             for curr, bal in self._start_cap.items():
# REMOVED_UNUSED_CODE:                 if curr == self._stake_currency:
# REMOVED_UNUSED_CODE:                     continue
# REMOVED_UNUSED_CODE:                 rate = self._exchange.get_conversion_rate(curr, self._stake_currency)
# REMOVED_UNUSED_CODE:                 if rate:
# REMOVED_UNUSED_CODE:                     cross_margin += bal * rate
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         current_stake = self._start_cap.get(self._stake_currency, 0) + tot_profit - tot_in_trades
# REMOVED_UNUSED_CODE:         total_stake = current_stake + used_stake
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         _wallets[self._stake_currency] = Wallet(
# REMOVED_UNUSED_CODE:             currency=self._stake_currency,
# REMOVED_UNUSED_CODE:             free=current_stake + cross_margin,
# REMOVED_UNUSED_CODE:             used=used_stake,
# REMOVED_UNUSED_CODE:             total=total_stake,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         for currency, bal in self._start_cap.items():
# REMOVED_UNUSED_CODE:             if currency not in _wallets:
# REMOVED_UNUSED_CODE:                 _wallets[currency] = Wallet(currency, bal, 0, bal)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self._wallets = _wallets
# REMOVED_UNUSED_CODE:         self._positions = _positions
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _update_live(self) -> None:
# REMOVED_UNUSED_CODE:         balances = self._exchange.get_balances()
# REMOVED_UNUSED_CODE:         _wallets = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         for currency in balances:
# REMOVED_UNUSED_CODE:             if isinstance(balances[currency], dict):
# REMOVED_UNUSED_CODE:                 _wallets[currency] = Wallet(
# REMOVED_UNUSED_CODE:                     currency,
# REMOVED_UNUSED_CODE:                     balances[currency].get("free", 0),
# REMOVED_UNUSED_CODE:                     balances[currency].get("used", 0),
# REMOVED_UNUSED_CODE:                     balances[currency].get("total", 0),
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         positions = self._exchange.fetch_positions()
# REMOVED_UNUSED_CODE:         _parsed_positions = {}
# REMOVED_UNUSED_CODE:         for position in positions:
# REMOVED_UNUSED_CODE:             symbol = position["symbol"]
# REMOVED_UNUSED_CODE:             if position["side"] is None or position["collateral"] == 0.0:
# REMOVED_UNUSED_CODE:                 # Position is not open ...
# REMOVED_UNUSED_CODE:                 continue
# REMOVED_UNUSED_CODE:             size = self._exchange._contracts_to_amount(symbol, position["contracts"])
# REMOVED_UNUSED_CODE:             collateral = safe_value_fallback(position, "collateral", "initialMargin", 0.0)
# REMOVED_UNUSED_CODE:             leverage = position.get("leverage")
# REMOVED_UNUSED_CODE:             _parsed_positions[symbol] = PositionWallet(
# REMOVED_UNUSED_CODE:                 symbol,
# REMOVED_UNUSED_CODE:                 position=size,
# REMOVED_UNUSED_CODE:                 leverage=leverage,
# REMOVED_UNUSED_CODE:                 collateral=collateral,
# REMOVED_UNUSED_CODE:                 side=position["side"],
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         self._positions = _parsed_positions
# REMOVED_UNUSED_CODE:         self._wallets = _wallets
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def update(self, require_update: bool = True) -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Updates wallets from the configured version.
# REMOVED_UNUSED_CODE:         By default, updates from the exchange.
# REMOVED_UNUSED_CODE:         Update-skipping should only be used for user-invoked /balance calls, since
# REMOVED_UNUSED_CODE:         for trading operations, the latest balance is needed.
# REMOVED_UNUSED_CODE:         :param require_update: Allow skipping an update if balances were recently refreshed
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         now = dt_now()
# REMOVED_UNUSED_CODE:         if (
# REMOVED_UNUSED_CODE:             require_update
# REMOVED_UNUSED_CODE:             or self._last_wallet_refresh is None
# REMOVED_UNUSED_CODE:             or (self._last_wallet_refresh + timedelta(seconds=3600) < now)
# REMOVED_UNUSED_CODE:         ):
# REMOVED_UNUSED_CODE:             if not self._config["dry_run"] or self._config.get("runmode") == RunMode.LIVE:
# REMOVED_UNUSED_CODE:                 self._update_live()
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 self._update_dry()
# REMOVED_UNUSED_CODE:             self._local_log("Wallets synced.")
# REMOVED_UNUSED_CODE:             self._last_wallet_refresh = dt_now()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_all_balances(self) -> dict[str, Wallet]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._wallets
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_all_positions(self) -> dict[str, PositionWallet]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._positions
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _check_exit_amount(self, trade: Trade) -> bool:
# REMOVED_UNUSED_CODE:         if trade.trading_mode != TradingMode.FUTURES:
# REMOVED_UNUSED_CODE:             # Slightly higher offset than in safe_exit_amount.
# REMOVED_UNUSED_CODE:             wallet_amount: float = self.get_total(trade.safe_base_currency) * (2 - 0.981)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # wallet_amount: float = self.wallets.get_free(trade.safe_base_currency)
# REMOVED_UNUSED_CODE:             position = self._positions.get(trade.pair)
# REMOVED_UNUSED_CODE:             if position is None:
# REMOVED_UNUSED_CODE:                 # We don't own anything :O
# REMOVED_UNUSED_CODE:                 return False
# REMOVED_UNUSED_CODE:             wallet_amount = position.position
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if wallet_amount >= trade.amount:
# REMOVED_UNUSED_CODE:             return True
# REMOVED_UNUSED_CODE:         return False
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def check_exit_amount(self, trade: Trade) -> bool:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Checks if the exit amount is available in the wallet.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param trade: Trade to check
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: True if the exit amount is available, False otherwise
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not self._check_exit_amount(trade):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Update wallets just to make sure
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.update()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return self._check_exit_amount(trade)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_starting_balance(self) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Retrieves starting balance - based on either available capital,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         or by using current balance subtracting
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if "available_capital" in self._config:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return self._config["available_capital"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             tot_profit = Trade.get_total_closed_profit()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             open_stakes = Trade.total_open_trades_stakes()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             available_balance = self.get_free(self._stake_currency)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return (available_balance - tot_profit + open_stakes) * self._config[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "tradable_balance_ratio"
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_total_stake_amount(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Return the total currently available balance in stake currency, including tied up stake and
# REMOVED_UNUSED_CODE:         respecting tradable_balance_ratio.
# REMOVED_UNUSED_CODE:         Calculated as
# REMOVED_UNUSED_CODE:         (<open_trade stakes> + free amount) * tradable_balance_ratio
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         val_tied_up = Trade.total_open_trades_stakes()
# REMOVED_UNUSED_CODE:         if "available_capital" in self._config:
# REMOVED_UNUSED_CODE:             starting_balance = self._config["available_capital"]
# REMOVED_UNUSED_CODE:             tot_profit = Trade.get_total_closed_profit()
# REMOVED_UNUSED_CODE:             available_amount = starting_balance + tot_profit
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             # Ensure <tradable_balance_ratio>% is used from the overall balance
# REMOVED_UNUSED_CODE:             # Otherwise we'd risk lowering stakes with each open trade.
# REMOVED_UNUSED_CODE:             # (tied up + current free) * ratio) - tied up
# REMOVED_UNUSED_CODE:             available_amount = (val_tied_up + self.get_free(self._stake_currency)) * self._config[
# REMOVED_UNUSED_CODE:                 "tradable_balance_ratio"
# REMOVED_UNUSED_CODE:             ]
# REMOVED_UNUSED_CODE:         return available_amount
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def get_available_stake_amount(self) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Return the total currently available balance in stake currency,
# REMOVED_UNUSED_CODE:         respecting tradable_balance_ratio.
# REMOVED_UNUSED_CODE:         Calculated as
# REMOVED_UNUSED_CODE:         (<open_trade stakes> + free amount) * tradable_balance_ratio - <open_trade stakes>
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         free = self.get_free(self._stake_currency)
# REMOVED_UNUSED_CODE:         return min(self.get_total_stake_amount() - Trade.total_open_trades_stakes(), free)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _calculate_unlimited_stake_amount(
# REMOVED_UNUSED_CODE:         self, available_amount: float, val_tied_up: float, max_open_trades: IntOrInf
# REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Calculate stake amount for "unlimited" stake amount
# REMOVED_UNUSED_CODE:         :return: 0 if max number of trades reached, else stake_amount to use.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if max_open_trades == 0:
# REMOVED_UNUSED_CODE:             return 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         possible_stake = (available_amount + val_tied_up) / max_open_trades
# REMOVED_UNUSED_CODE:         # Theoretical amount can be above available amount - therefore limit to available amount!
# REMOVED_UNUSED_CODE:         return min(possible_stake, available_amount)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _check_available_stake_amount(self, stake_amount: float, available_amount: float) -> float:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Check if stake amount can be fulfilled with the available balance
# REMOVED_UNUSED_CODE:         for the stake currency
# REMOVED_UNUSED_CODE:         :return: float: Stake amount
# REMOVED_UNUSED_CODE:         :raise: DependencyException if balance is lower than stake-amount
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if self._config["amend_last_stake_amount"]:
# REMOVED_UNUSED_CODE:             # Remaining amount needs to be at least stake_amount * last_stake_amount_min_ratio
# REMOVED_UNUSED_CODE:             # Otherwise the remaining amount is too low to trade.
# REMOVED_UNUSED_CODE:             if available_amount > (stake_amount * self._config["last_stake_amount_min_ratio"]):
# REMOVED_UNUSED_CODE:                 stake_amount = min(stake_amount, available_amount)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 stake_amount = 0
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         if available_amount < stake_amount:
# REMOVED_UNUSED_CODE:             raise DependencyException(
# REMOVED_UNUSED_CODE:                 f"Available balance ({available_amount} {self._config['stake_currency']}) is "
# REMOVED_UNUSED_CODE:                 f"lower than stake amount ({stake_amount} {self._config['stake_currency']})"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         return max(stake_amount, 0)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_trade_stake_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self, pair: str, max_open_trades: IntOrInf, edge=None, update: bool = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ) -> float:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Calculate stake amount for the trade
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :return: float: Stake amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :raise: DependencyException if the available stake amount is too low
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_amount: float
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         # Ensure wallets are up-to-date.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if update:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self.update()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         val_tied_up = Trade.total_open_trades_stakes()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         available_amount = self.get_available_stake_amount()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if edge:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             stake_amount = edge.stake_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 pair,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.get_free(self._stake_currency),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self.get_total(self._stake_currency),
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 val_tied_up,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             stake_amount = self._config["stake_amount"]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if stake_amount == UNLIMITED_STAKE_AMOUNT:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 stake_amount = self._calculate_unlimited_stake_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     available_amount, val_tied_up, max_open_trades
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return self._check_available_stake_amount(stake_amount, available_amount)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def validate_stake_amount(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         pair: str,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         stake_amount: float | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         min_stake_amount: float | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_stake_amount: float,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         trade_amount: float | None,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if not stake_amount:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._local_log(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Stake amount is {stake_amount}, ignoring possible trade for {pair}.",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 level="debug",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         max_allowed_stake = min(max_stake_amount, self.get_available_stake_amount())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if trade_amount:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # if in a trade, then the resulting trade size cannot go beyond the max stake
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             # Otherwise we could no longer exit.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             max_allowed_stake = min(max_allowed_stake, max_stake_amount - trade_amount)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if min_stake_amount is not None and min_stake_amount > max_allowed_stake:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._local_log(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "Minimum stake amount > available balance. "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"{min_stake_amount} > {max_allowed_stake}",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 level="warning",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             return 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if min_stake_amount is not None and stake_amount < min_stake_amount:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._local_log(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Stake amount for pair {pair} is too small "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"({stake_amount} < {min_stake_amount}), adjusting to {min_stake_amount}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             if stake_amount * 1.3 < min_stake_amount:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 # Top-cap stake-amount adjustments to +30%.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 self._local_log(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"Adjusted stake amount for pair {pair} is more than 30% bigger than "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"the desired stake amount of ({stake_amount:.8f} * 1.3 = "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                     f"{stake_amount * 1.3:.8f}) < {min_stake_amount}), ignoring trade."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 return 0
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             stake_amount = min_stake_amount
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         if stake_amount > max_allowed_stake:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             self._local_log(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"Stake amount for pair {pair} is too big "
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 f"({stake_amount} > {max_allowed_stake}), adjusting to {max_allowed_stake}."
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             stake_amount = max_allowed_stake
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return stake_amount
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def _local_log(self, msg: str, level: Literal["info", "warning", "debug"] = "info") -> None:
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Log a message to the local log.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if not self._is_backtest:
# REMOVED_UNUSED_CODE:             if level == "warning":
# REMOVED_UNUSED_CODE:                 logger.warning(msg)
# REMOVED_UNUSED_CODE:             elif level == "debug":
# REMOVED_UNUSED_CODE:                 logger.debug(msg)
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 logger.info(msg)
