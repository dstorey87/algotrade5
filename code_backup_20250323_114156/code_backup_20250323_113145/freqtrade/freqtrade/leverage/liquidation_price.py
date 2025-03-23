import logging

# REMOVED_UNUSED_CODE: from freqtrade.enums import MarginMode
# REMOVED_UNUSED_CODE: from freqtrade.exceptions import DependencyException
# REMOVED_UNUSED_CODE: from freqtrade.exchange import Exchange
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.persistence import LocalTrade, Trade
# REMOVED_UNUSED_CODE: from freqtrade.wallets import Wallets


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def update_liquidation_prices(
# REMOVED_UNUSED_CODE:     trade: LocalTrade | None = None,
# REMOVED_UNUSED_CODE:     *,
# REMOVED_UNUSED_CODE:     exchange: Exchange,
# REMOVED_UNUSED_CODE:     wallets: Wallets,
# REMOVED_UNUSED_CODE:     stake_currency: str,
# REMOVED_UNUSED_CODE:     dry_run: bool = False,
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Update trade liquidation price in isolated margin mode.
# REMOVED_UNUSED_CODE:     Updates liquidation price for all trades in cross margin mode.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         if exchange.margin_mode == MarginMode.CROSS:
# REMOVED_UNUSED_CODE:             total_wallet_stake = 0.0
# REMOVED_UNUSED_CODE:             if dry_run:
# REMOVED_UNUSED_CODE:                 # Parameters only needed for cross margin
# REMOVED_UNUSED_CODE:                 total_wallet_stake = wallets.get_collateral()
# REMOVED_UNUSED_CODE:                 logger.info(
# REMOVED_UNUSED_CODE:                     "Updating liquidation price for all open trades. "
# REMOVED_UNUSED_CODE:                     f"Collateral {total_wallet_stake} {stake_currency}."
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:             open_trades: list[Trade] = Trade.get_open_trades()
# REMOVED_UNUSED_CODE:             for t in open_trades:
# REMOVED_UNUSED_CODE:                 if t.has_open_position:
# REMOVED_UNUSED_CODE:                     # TODO: This should be done in a batch update
# REMOVED_UNUSED_CODE:                     t.set_liquidation_price(
# REMOVED_UNUSED_CODE:                         exchange.get_liquidation_price(
# REMOVED_UNUSED_CODE:                             pair=t.pair,
# REMOVED_UNUSED_CODE:                             open_rate=t.open_rate,
# REMOVED_UNUSED_CODE:                             is_short=t.is_short,
# REMOVED_UNUSED_CODE:                             amount=t.amount,
# REMOVED_UNUSED_CODE:                             stake_amount=t.stake_amount,
# REMOVED_UNUSED_CODE:                             leverage=t.leverage,
# REMOVED_UNUSED_CODE:                             wallet_balance=total_wallet_stake,
# REMOVED_UNUSED_CODE:                             open_trades=open_trades,
# REMOVED_UNUSED_CODE:                         )
# REMOVED_UNUSED_CODE:                     )
# REMOVED_UNUSED_CODE:         elif trade:
# REMOVED_UNUSED_CODE:             trade.set_liquidation_price(
# REMOVED_UNUSED_CODE:                 exchange.get_liquidation_price(
# REMOVED_UNUSED_CODE:                     pair=trade.pair,
# REMOVED_UNUSED_CODE:                     open_rate=trade.open_rate,
# REMOVED_UNUSED_CODE:                     is_short=trade.is_short,
# REMOVED_UNUSED_CODE:                     amount=trade.amount,
# REMOVED_UNUSED_CODE:                     stake_amount=trade.stake_amount,
# REMOVED_UNUSED_CODE:                     leverage=trade.leverage,
# REMOVED_UNUSED_CODE:                     wallet_balance=trade.stake_amount,
# REMOVED_UNUSED_CODE:                 )
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             raise DependencyException(
# REMOVED_UNUSED_CODE:                 "Trade object is required for updating liquidation price in isolated margin mode."
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:     except DependencyException:
# REMOVED_UNUSED_CODE:         logger.warning("Unable to calculate liquidation price")
