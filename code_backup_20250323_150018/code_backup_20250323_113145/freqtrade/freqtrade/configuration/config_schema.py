# Required json-schema for user specified config

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.constants import (
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     AVAILABLE_DATAHANDLERS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     AVAILABLE_PAIRLISTS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     BACKTEST_BREAKDOWNS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     DRY_RUN_WALLET,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     EXPORT_OPTIONS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     MARGIN_MODES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ORDERTIF_POSSIBILITIES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     ORDERTYPE_POSSIBILITIES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     PRICING_SIDES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     REQUIRED_ORDERTIF,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     STOPLOSS_PRICE_TYPES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     SUPPORTED_FIAT,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     TIMEOUT_UNITS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     TRADING_MODES,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     UNLIMITED_STAKE_AMOUNT,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     WEBHOOK_FORMAT_OPTIONS,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: )
# REMOVED_UNUSED_CODE: from freqtrade.enums import RPCMessageType


# REMOVED_UNUSED_CODE: __MESSAGE_TYPE_DICT: dict[str, dict[str, str]] = {x: {"type": "object"} for x in RPCMessageType}

# REMOVED_UNUSED_CODE: __IN_STRATEGY = "\nUsually specified in the strategy and missing in the configuration."

# REMOVED_UNUSED_CODE: CONF_SCHEMA = {
# REMOVED_UNUSED_CODE:     "type": "object",
# REMOVED_UNUSED_CODE:     "properties": {
# REMOVED_UNUSED_CODE:         "max_open_trades": {
# REMOVED_UNUSED_CODE:             "description": "Maximum number of open trades. -1 for unlimited.",
# REMOVED_UNUSED_CODE:             "type": ["integer", "number"],
# REMOVED_UNUSED_CODE:             "minimum": -1,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "timeframe": {
# REMOVED_UNUSED_CODE:             "description": (
# REMOVED_UNUSED_CODE:                 f"The timeframe to use (e.g `1m`, `5m`, `15m`, `30m`, `1h` ...). {__IN_STRATEGY}"
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "proxy_coin": {
# REMOVED_UNUSED_CODE:             "description": "Proxy coin - must be used for specific futures modes (e.g. BNFCR)",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "stake_currency": {
# REMOVED_UNUSED_CODE:             "description": "Currency used for staking.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "stake_amount": {
# REMOVED_UNUSED_CODE:             "description": "Amount to stake per trade.",
# REMOVED_UNUSED_CODE:             "type": ["number", "string"],
# REMOVED_UNUSED_CODE:             "minimum": 0.0001,
# REMOVED_UNUSED_CODE:             "pattern": UNLIMITED_STAKE_AMOUNT,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "tradable_balance_ratio": {
# REMOVED_UNUSED_CODE:             "description": "Ratio of balance that is tradable.",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "minimum": 0.0,
# REMOVED_UNUSED_CODE:             "maximum": 1,
# REMOVED_UNUSED_CODE:             "default": 0.99,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "available_capital": {
# REMOVED_UNUSED_CODE:             "description": "Total capital available for trading.",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "minimum": 0,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "amend_last_stake_amount": {
# REMOVED_UNUSED_CODE:             "description": "Whether to amend the last stake amount.",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:             "default": False,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "last_stake_amount_min_ratio": {
# REMOVED_UNUSED_CODE:             "description": "Minimum ratio for the last stake amount.",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "minimum": 0.0,
# REMOVED_UNUSED_CODE:             "maximum": 1.0,
# REMOVED_UNUSED_CODE:             "default": 0.5,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "fiat_display_currency": {
# REMOVED_UNUSED_CODE:             "description": "Fiat currency for display purposes.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:             "enum": SUPPORTED_FIAT,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "dry_run": {
# REMOVED_UNUSED_CODE:             "description": "Enable or disable dry run mode.",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "dry_run_wallet": {
# REMOVED_UNUSED_CODE:             "description": "Initial wallet balance for dry run mode.",
# REMOVED_UNUSED_CODE:             "type": ["number", "object"],
# REMOVED_UNUSED_CODE:             "default": DRY_RUN_WALLET,
# REMOVED_UNUSED_CODE:             "patternProperties": {r"^[a-zA-Z0-9]+$": {"type": "number"}},
# REMOVED_UNUSED_CODE:             "additionalProperties": False,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "cancel_open_orders_on_exit": {
# REMOVED_UNUSED_CODE:             "description": "Cancel open orders when exiting.",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:             "default": False,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "process_only_new_candles": {
# REMOVED_UNUSED_CODE:             "description": "Process only new candles.",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "minimal_roi": {
# REMOVED_UNUSED_CODE:             "description": f"Minimum return on investment. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "patternProperties": {"^[0-9.]+$": {"type": "number"}},
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "amount_reserve_percent": {
# REMOVED_UNUSED_CODE:             "description": "Percentage of amount to reserve.",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "minimum": 0.0,
# REMOVED_UNUSED_CODE:             "maximum": 0.5,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "stoploss": {
# REMOVED_UNUSED_CODE:             "description": f"Value (as ratio) to use as Stoploss value. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "maximum": 0,
# REMOVED_UNUSED_CODE:             "exclusiveMaximum": True,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "trailing_stop": {
# REMOVED_UNUSED_CODE:             "description": f"Enable or disable trailing stop. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "trailing_stop_positive": {
# REMOVED_UNUSED_CODE:             "description": f"Positive offset for trailing stop. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "minimum": 0,
# REMOVED_UNUSED_CODE:             "maximum": 1,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "trailing_stop_positive_offset": {
# REMOVED_UNUSED_CODE:             "description": f"Offset for trailing stop to activate. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "minimum": 0,
# REMOVED_UNUSED_CODE:             "maximum": 1,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "trailing_only_offset_is_reached": {
# REMOVED_UNUSED_CODE:             "description": f"Use trailing stop only when offset is reached. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "use_exit_signal": {
# REMOVED_UNUSED_CODE:             "description": f"Use exit signal for trades. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "exit_profit_only": {
# REMOVED_UNUSED_CODE:             "description": (
# REMOVED_UNUSED_CODE:                 "Exit only when in profit. Exit signals are ignored as "
# REMOVED_UNUSED_CODE:                 f"long as profit is < exit_profit_offset. {__IN_STRATEGY}"
# REMOVED_UNUSED_CODE:             ),
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "exit_profit_offset": {
# REMOVED_UNUSED_CODE:             "description": f"Offset for profit exit. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "fee": {
# REMOVED_UNUSED_CODE:             "description": "Trading fee percentage. Can help to simulate slippage in backtesting",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "minimum": 0,
# REMOVED_UNUSED_CODE:             "maximum": 0.1,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "ignore_roi_if_entry_signal": {
# REMOVED_UNUSED_CODE:             "description": f"Ignore ROI if entry signal is present. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "ignore_buying_expired_candle_after": {
# REMOVED_UNUSED_CODE:             "description": f"Ignore buying after candle expiration time. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "trading_mode": {
# REMOVED_UNUSED_CODE:             "description": "Mode of trading (e.g., spot, margin).",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:             "enum": TRADING_MODES,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "margin_mode": {
# REMOVED_UNUSED_CODE:             "description": "Margin mode for trading.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:             "enum": MARGIN_MODES,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "reduce_df_footprint": {
# REMOVED_UNUSED_CODE:             "description": "Reduce DataFrame footprint by casting columns to float32/int32.",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:             "default": False,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         # Lookahead analysis section
# REMOVED_UNUSED_CODE:         "minimum_trade_amount": {
# REMOVED_UNUSED_CODE:             "description": "Minimum amount for a trade - only used for lookahead-analysis",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "default": 10,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "targeted_trade_amount": {
# REMOVED_UNUSED_CODE:             "description": "Targeted trade amount for lookahead analysis.",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "default": 20,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "lookahead_analysis_exportfilename": {
# REMOVED_UNUSED_CODE:             "description": "csv Filename for lookahead analysis export.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "startup_candle": {
# REMOVED_UNUSED_CODE:             "description": "Startup candle configuration.",
# REMOVED_UNUSED_CODE:             "type": "array",
# REMOVED_UNUSED_CODE:             "uniqueItems": True,
# REMOVED_UNUSED_CODE:             "default": [199, 399, 499, 999, 1999],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "liquidation_buffer": {
# REMOVED_UNUSED_CODE:             "description": "Buffer ratio for liquidation.",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "minimum": 0.0,
# REMOVED_UNUSED_CODE:             "maximum": 0.99,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "backtest_breakdown": {
# REMOVED_UNUSED_CODE:             "description": "Breakdown configuration for backtesting.",
# REMOVED_UNUSED_CODE:             "type": "array",
# REMOVED_UNUSED_CODE:             "items": {"type": "string", "enum": BACKTEST_BREAKDOWNS},
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "bot_name": {
# REMOVED_UNUSED_CODE:             "description": "Name of the trading bot. Passed via API to a client.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "unfilledtimeout": {
# REMOVED_UNUSED_CODE:             "description": f"Timeout configuration for unfilled orders. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "entry": {
# REMOVED_UNUSED_CODE:                     "description": "Timeout for entry orders in unit.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 1,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "exit": {
# REMOVED_UNUSED_CODE:                     "description": "Timeout for exit orders in unit.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 1,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "exit_timeout_count": {
# REMOVED_UNUSED_CODE:                     "description": "Number of times to retry exit orders before giving up.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 0,
# REMOVED_UNUSED_CODE:                     "default": 0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "unit": {
# REMOVED_UNUSED_CODE:                     "description": "Unit of time for the timeout (e.g., seconds, minutes).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": TIMEOUT_UNITS,
# REMOVED_UNUSED_CODE:                     "default": "minutes",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "entry_pricing": {
# REMOVED_UNUSED_CODE:             "description": "Configuration for entry pricing.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "price_last_balance": {
# REMOVED_UNUSED_CODE:                     "description": "Balance ratio for the last price.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 0,
# REMOVED_UNUSED_CODE:                     "maximum": 1,
# REMOVED_UNUSED_CODE:                     "exclusiveMaximum": False,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "price_side": {
# REMOVED_UNUSED_CODE:                     "description": "Side of the price to use (e.g., bid, ask, same).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": PRICING_SIDES,
# REMOVED_UNUSED_CODE:                     "default": "same",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "use_order_book": {
# REMOVED_UNUSED_CODE:                     "description": "Whether to use the order book for pricing.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "order_book_top": {
# REMOVED_UNUSED_CODE:                     "description": "Top N levels of the order book to consider.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "minimum": 1,
# REMOVED_UNUSED_CODE:                     "maximum": 50,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "check_depth_of_market": {
# REMOVED_UNUSED_CODE:                     "description": "Configuration for checking the depth of the market.",
# REMOVED_UNUSED_CODE:                     "type": "object",
# REMOVED_UNUSED_CODE:                     "properties": {
# REMOVED_UNUSED_CODE:                         "enabled": {
# REMOVED_UNUSED_CODE:                             "description": "Enable or disable depth of market check.",
# REMOVED_UNUSED_CODE:                             "type": "boolean",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "bids_to_ask_delta": {
# REMOVED_UNUSED_CODE:                             "description": "Delta between bids and asks to consider.",
# REMOVED_UNUSED_CODE:                             "type": "number",
# REMOVED_UNUSED_CODE:                             "minimum": 0,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                     },
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": ["price_side"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "exit_pricing": {
# REMOVED_UNUSED_CODE:             "description": "Configuration for exit pricing.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "price_side": {
# REMOVED_UNUSED_CODE:                     "description": "Side of the price to use (e.g., bid, ask, same).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": PRICING_SIDES,
# REMOVED_UNUSED_CODE:                     "default": "same",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "price_last_balance": {
# REMOVED_UNUSED_CODE:                     "description": "Balance ratio for the last price.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 0,
# REMOVED_UNUSED_CODE:                     "maximum": 1,
# REMOVED_UNUSED_CODE:                     "exclusiveMaximum": False,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "use_order_book": {
# REMOVED_UNUSED_CODE:                     "description": "Whether to use the order book for pricing.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "order_book_top": {
# REMOVED_UNUSED_CODE:                     "description": "Top N levels of the order book to consider.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "minimum": 1,
# REMOVED_UNUSED_CODE:                     "maximum": 50,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": ["price_side"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "custom_price_max_distance_ratio": {
# REMOVED_UNUSED_CODE:             "description": "Maximum distance ratio between current and custom entry or exit price.",
# REMOVED_UNUSED_CODE:             "type": "number",
# REMOVED_UNUSED_CODE:             "minimum": 0.0,
# REMOVED_UNUSED_CODE:             "maximum": 1,
# REMOVED_UNUSED_CODE:             "default": 0.02,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "order_types": {
# REMOVED_UNUSED_CODE:             "description": f"Configuration of order types. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "entry": {
# REMOVED_UNUSED_CODE:                     "description": "Order type for entry (e.g., limit, market).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": ORDERTYPE_POSSIBILITIES,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "exit": {
# REMOVED_UNUSED_CODE:                     "description": "Order type for exit (e.g., limit, market).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": ORDERTYPE_POSSIBILITIES,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "force_exit": {
# REMOVED_UNUSED_CODE:                     "description": "Order type for forced exit (e.g., limit, market).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": ORDERTYPE_POSSIBILITIES,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "force_entry": {
# REMOVED_UNUSED_CODE:                     "description": "Order type for forced entry (e.g., limit, market).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": ORDERTYPE_POSSIBILITIES,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "emergency_exit": {
# REMOVED_UNUSED_CODE:                     "description": "Order type for emergency exit (e.g., limit, market).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": ORDERTYPE_POSSIBILITIES,
# REMOVED_UNUSED_CODE:                     "default": "market",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "stoploss": {
# REMOVED_UNUSED_CODE:                     "description": "Order type for stop loss (e.g., limit, market).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": ORDERTYPE_POSSIBILITIES,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "stoploss_on_exchange": {
# REMOVED_UNUSED_CODE:                     "description": "Whether to place stop loss on the exchange.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "stoploss_price_type": {
# REMOVED_UNUSED_CODE:                     "description": "Price type for stop loss (e.g., last, mark, index).",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": STOPLOSS_PRICE_TYPES,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "stoploss_on_exchange_interval": {
# REMOVED_UNUSED_CODE:                     "description": "Interval for stop loss on exchange in seconds.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "stoploss_on_exchange_limit_ratio": {
# REMOVED_UNUSED_CODE:                     "description": "Limit ratio for stop loss on exchange.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 0.0,
# REMOVED_UNUSED_CODE:                     "maximum": 1.0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": ["entry", "exit", "stoploss", "stoploss_on_exchange"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "order_time_in_force": {
# REMOVED_UNUSED_CODE:             "description": f"Time in force configuration for orders. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "entry": {
# REMOVED_UNUSED_CODE:                     "description": "Time in force for entry orders.",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": ORDERTIF_POSSIBILITIES,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "exit": {
# REMOVED_UNUSED_CODE:                     "description": "Time in force for exit orders.",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": ORDERTIF_POSSIBILITIES,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": REQUIRED_ORDERTIF,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "coingecko": {
# REMOVED_UNUSED_CODE:             "description": "Configuration for CoinGecko API.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "is_demo": {
# REMOVED_UNUSED_CODE:                     "description": "Whether to use CoinGecko in demo mode.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": True,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "api_key": {"description": "API key for accessing CoinGecko.", "type": "string"},
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": ["is_demo", "api_key"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "exchange": {
# REMOVED_UNUSED_CODE:             "description": "Exchange configuration.",
# REMOVED_UNUSED_CODE:             "$ref": "#/definitions/exchange",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "edge": {
# REMOVED_UNUSED_CODE:             "description": "Edge configuration.",
# REMOVED_UNUSED_CODE:             "$ref": "#/definitions/edge",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "freqai": {
# REMOVED_UNUSED_CODE:             "description": "FreqAI configuration.",
# REMOVED_UNUSED_CODE:             "$ref": "#/definitions/freqai",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "external_message_consumer": {
# REMOVED_UNUSED_CODE:             "description": "Configuration for external message consumer.",
# REMOVED_UNUSED_CODE:             "$ref": "#/definitions/external_message_consumer",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "experimental": {
# REMOVED_UNUSED_CODE:             "description": "Experimental configuration.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {"block_bad_exchanges": {"type": "boolean"}},
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "pairlists": {
# REMOVED_UNUSED_CODE:             "description": "Configuration for pairlists.",
# REMOVED_UNUSED_CODE:             "type": "array",
# REMOVED_UNUSED_CODE:             "items": {
# REMOVED_UNUSED_CODE:                 "type": "object",
# REMOVED_UNUSED_CODE:                 "properties": {
# REMOVED_UNUSED_CODE:                     "method": {
# REMOVED_UNUSED_CODE:                         "description": "Method used for generating the pairlist.",
# REMOVED_UNUSED_CODE:                         "type": "string",
# REMOVED_UNUSED_CODE:                         "enum": AVAILABLE_PAIRLISTS,
# REMOVED_UNUSED_CODE:                     },
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "required": ["method"],
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         # RPC section
# REMOVED_UNUSED_CODE:         "telegram": {
# REMOVED_UNUSED_CODE:             "description": "Telegram settings.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "enabled": {
# REMOVED_UNUSED_CODE:                     "description": "Enable Telegram notifications.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "token": {"description": "Telegram bot token.", "type": "string"},
# REMOVED_UNUSED_CODE:                 "chat_id": {
# REMOVED_UNUSED_CODE:                     "description": "Telegram chat or group ID",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "topic_id": {
# REMOVED_UNUSED_CODE:                     "description": "Telegram topic ID - only applicable for group chats",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "allow_custom_messages": {
# REMOVED_UNUSED_CODE:                     "description": "Allow sending custom messages from the Strategy.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": True,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "balance_dust_level": {
# REMOVED_UNUSED_CODE:                     "description": "Minimum balance level to consider as dust.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 0.0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "notification_settings": {
# REMOVED_UNUSED_CODE:                     "description": "Settings for different types of notifications.",
# REMOVED_UNUSED_CODE:                     "type": "object",
# REMOVED_UNUSED_CODE:                     "default": {},
# REMOVED_UNUSED_CODE:                     "properties": {
# REMOVED_UNUSED_CODE:                         "status": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for status updates.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "warning": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for warnings.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "startup": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for startup messages.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "entry": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for entry signals.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "entry_fill": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for entry fill signals.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                             "default": "off",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "entry_cancel": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for entry cancel signals.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "exit": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for exit signals.",
# REMOVED_UNUSED_CODE:                             "type": ["string", "object"],
# REMOVED_UNUSED_CODE:                             "additionalProperties": {
# REMOVED_UNUSED_CODE:                                 "type": "string",
# REMOVED_UNUSED_CODE:                                 "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                             },
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "exit_fill": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for exit fill signals.",
# REMOVED_UNUSED_CODE:                             "type": ["string", "object"],
# REMOVED_UNUSED_CODE:                             "additionalProperties": {
# REMOVED_UNUSED_CODE:                                 "type": "string",
# REMOVED_UNUSED_CODE:                                 "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                             },
# REMOVED_UNUSED_CODE:                             "default": "on",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "exit_cancel": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for exit cancel signals.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "protection_trigger": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for protection triggers.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                             "default": "on",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "protection_trigger_global": {
# REMOVED_UNUSED_CODE:                             "description": "Telegram setting for global protection triggers.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "enum": TELEGRAM_SETTING_OPTIONS,
# REMOVED_UNUSED_CODE:                             "default": "on",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                     },
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "reload": {
# REMOVED_UNUSED_CODE:                     "description": "Add Reload button to certain messages.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": ["enabled", "token", "chat_id"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "webhook": {
# REMOVED_UNUSED_CODE:             "description": "Webhook settings.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "enabled": {"type": "boolean"},
# REMOVED_UNUSED_CODE:                 "url": {"type": "string"},
# REMOVED_UNUSED_CODE:                 "format": {"type": "string", "enum": WEBHOOK_FORMAT_OPTIONS, "default": "form"},
# REMOVED_UNUSED_CODE:                 "retries": {"type": "integer", "minimum": 0},
# REMOVED_UNUSED_CODE:                 "retry_delay": {"type": "number", "minimum": 0},
# REMOVED_UNUSED_CODE:                 **__MESSAGE_TYPE_DICT,
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "discord": {
# REMOVED_UNUSED_CODE:             "description": "Discord settings.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "enabled": {"type": "boolean"},
# REMOVED_UNUSED_CODE:                 "webhook_url": {"type": "string"},
# REMOVED_UNUSED_CODE:                 "exit_fill": {
# REMOVED_UNUSED_CODE:                     "type": "array",
# REMOVED_UNUSED_CODE:                     "items": {"type": "object"},
# REMOVED_UNUSED_CODE:                     "default": [
# REMOVED_UNUSED_CODE:                         {"Trade ID": "{trade_id}"},
# REMOVED_UNUSED_CODE:                         {"Exchange": "{exchange}"},
# REMOVED_UNUSED_CODE:                         {"Pair": "{pair}"},
# REMOVED_UNUSED_CODE:                         {"Direction": "{direction}"},
# REMOVED_UNUSED_CODE:                         {"Open rate": "{open_rate}"},
# REMOVED_UNUSED_CODE:                         {"Close rate": "{close_rate}"},
# REMOVED_UNUSED_CODE:                         {"Amount": "{amount}"},
# REMOVED_UNUSED_CODE:                         {"Open date": "{open_date:%Y-%m-%d %H:%M:%S}"},
# REMOVED_UNUSED_CODE:                         {"Close date": "{close_date:%Y-%m-%d %H:%M:%S}"},
# REMOVED_UNUSED_CODE:                         {"Profit": "{profit_amount} {stake_currency}"},
# REMOVED_UNUSED_CODE:                         {"Profitability": "{profit_ratio:.2%}"},
# REMOVED_UNUSED_CODE:                         {"Enter tag": "{enter_tag}"},
# REMOVED_UNUSED_CODE:                         {"Exit Reason": "{exit_reason}"},
# REMOVED_UNUSED_CODE:                         {"Strategy": "{strategy}"},
# REMOVED_UNUSED_CODE:                         {"Timeframe": "{timeframe}"},
# REMOVED_UNUSED_CODE:                     ],
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "entry_fill": {
# REMOVED_UNUSED_CODE:                     "type": "array",
# REMOVED_UNUSED_CODE:                     "items": {"type": "object"},
# REMOVED_UNUSED_CODE:                     "default": [
# REMOVED_UNUSED_CODE:                         {"Trade ID": "{trade_id}"},
# REMOVED_UNUSED_CODE:                         {"Exchange": "{exchange}"},
# REMOVED_UNUSED_CODE:                         {"Pair": "{pair}"},
# REMOVED_UNUSED_CODE:                         {"Direction": "{direction}"},
# REMOVED_UNUSED_CODE:                         {"Open rate": "{open_rate}"},
# REMOVED_UNUSED_CODE:                         {"Amount": "{amount}"},
# REMOVED_UNUSED_CODE:                         {"Open date": "{open_date:%Y-%m-%d %H:%M:%S}"},
# REMOVED_UNUSED_CODE:                         {"Enter tag": "{enter_tag}"},
# REMOVED_UNUSED_CODE:                         {"Strategy": "{strategy} {timeframe}"},
# REMOVED_UNUSED_CODE:                     ],
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "api_server": {
# REMOVED_UNUSED_CODE:             "description": "API server settings.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "enabled": {"description": "Whether the API server is enabled.", "type": "boolean"},
# REMOVED_UNUSED_CODE:                 "listen_ip_address": {
# REMOVED_UNUSED_CODE:                     "description": "IP address the API server listens on.",
# REMOVED_UNUSED_CODE:                     "format": "ipv4",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "listen_port": {
# REMOVED_UNUSED_CODE:                     "description": "Port the API server listens on.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "minimum": 1024,
# REMOVED_UNUSED_CODE:                     "maximum": 65535,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "username": {
# REMOVED_UNUSED_CODE:                     "description": "Username for API server authentication.",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "password": {
# REMOVED_UNUSED_CODE:                     "description": "Password for API server authentication.",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "ws_token": {
# REMOVED_UNUSED_CODE:                     "description": "WebSocket token for API server.",
# REMOVED_UNUSED_CODE:                     "type": ["string", "array"],
# REMOVED_UNUSED_CODE:                     "items": {"type": "string"},
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "jwt_secret_key": {
# REMOVED_UNUSED_CODE:                     "description": "Secret key for JWT authentication.",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "CORS_origins": {
# REMOVED_UNUSED_CODE:                     "description": "List of allowed CORS origins.",
# REMOVED_UNUSED_CODE:                     "type": "array",
# REMOVED_UNUSED_CODE:                     "items": {"type": "string"},
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "verbosity": {
# REMOVED_UNUSED_CODE:                     "description": "Logging verbosity level.",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "enum": ["error", "info"],
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": ["enabled", "listen_ip_address", "listen_port", "username", "password"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         # end of RPC section
# REMOVED_UNUSED_CODE:         "db_url": {
# REMOVED_UNUSED_CODE:             "description": "Database connection URL.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "export": {
# REMOVED_UNUSED_CODE:             "description": "Type of data to export.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:             "enum": EXPORT_OPTIONS,
# REMOVED_UNUSED_CODE:             "default": "trades",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "disableparamexport": {
# REMOVED_UNUSED_CODE:             "description": "Disable parameter export.",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "initial_state": {
# REMOVED_UNUSED_CODE:             "description": "Initial state of the system.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:             "enum": ["running", "stopped"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "force_entry_enable": {
# REMOVED_UNUSED_CODE:             "description": "Force enable entry.",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "disable_dataframe_checks": {
# REMOVED_UNUSED_CODE:             "description": "Disable checks on dataframes.",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "internals": {
# REMOVED_UNUSED_CODE:             "description": "Internal settings.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "default": {},
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "process_throttle_secs": {
# REMOVED_UNUSED_CODE:                     "description": "Minimum loop duration for one bot iteration in seconds.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "interval": {
# REMOVED_UNUSED_CODE:                     "description": "Interval time in seconds.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "sd_notify": {
# REMOVED_UNUSED_CODE:                     "description": "Enable systemd notify.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "dataformat_ohlcv": {
# REMOVED_UNUSED_CODE:             "description": "Data format for OHLCV data.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:             "enum": AVAILABLE_DATAHANDLERS,
# REMOVED_UNUSED_CODE:             "default": "feather",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "dataformat_trades": {
# REMOVED_UNUSED_CODE:             "description": "Data format for trade data.",
# REMOVED_UNUSED_CODE:             "type": "string",
# REMOVED_UNUSED_CODE:             "enum": AVAILABLE_DATAHANDLERS,
# REMOVED_UNUSED_CODE:             "default": "feather",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "position_adjustment_enable": {
# REMOVED_UNUSED_CODE:             "description": f"Enable position adjustment. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         # Download data section
# REMOVED_UNUSED_CODE:         "new_pairs_days": {
# REMOVED_UNUSED_CODE:             "description": "Download data of new pairs for given number of days",
# REMOVED_UNUSED_CODE:             "type": "integer",
# REMOVED_UNUSED_CODE:             "default": 30,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "download_trades": {
# REMOVED_UNUSED_CODE:             "description": "Download trades data by default (instead of ohlcv data).",
# REMOVED_UNUSED_CODE:             "type": "boolean",
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "max_entry_position_adjustment": {
# REMOVED_UNUSED_CODE:             "description": f"Maximum entry position adjustment allowed. {__IN_STRATEGY}",
# REMOVED_UNUSED_CODE:             "type": ["integer", "number"],
# REMOVED_UNUSED_CODE:             "minimum": -1,
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "add_config_files": {
# REMOVED_UNUSED_CODE:             "description": "Additional configuration files to load.",
# REMOVED_UNUSED_CODE:             "type": "array",
# REMOVED_UNUSED_CODE:             "items": {"type": "string"},
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "orderflow": {
# REMOVED_UNUSED_CODE:             "description": "Settings related to order flow.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "cache_size": {
# REMOVED_UNUSED_CODE:                     "description": "Size of the cache for order flow data.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 1,
# REMOVED_UNUSED_CODE:                     "default": 1500,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "max_candles": {
# REMOVED_UNUSED_CODE:                     "description": "Maximum number of candles to consider.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 1,
# REMOVED_UNUSED_CODE:                     "default": 1500,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "scale": {
# REMOVED_UNUSED_CODE:                     "description": "Scale factor for order flow data.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 0.0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "stacked_imbalance_range": {
# REMOVED_UNUSED_CODE:                     "description": "Range for stacked imbalance.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "imbalance_volume": {
# REMOVED_UNUSED_CODE:                     "description": "Volume threshold for imbalance.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "imbalance_ratio": {
# REMOVED_UNUSED_CODE:                     "description": "Ratio threshold for imbalance.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "minimum": 0.0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": [
# REMOVED_UNUSED_CODE:                 "max_candles",
# REMOVED_UNUSED_CODE:                 "scale",
# REMOVED_UNUSED_CODE:                 "stacked_imbalance_range",
# REMOVED_UNUSED_CODE:                 "imbalance_volume",
# REMOVED_UNUSED_CODE:                 "imbalance_ratio",
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     },
# REMOVED_UNUSED_CODE:     "definitions": {
# REMOVED_UNUSED_CODE:         "exchange": {
# REMOVED_UNUSED_CODE:             "description": "Exchange configuration settings.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "name": {"description": "Name of the exchange.", "type": "string"},
# REMOVED_UNUSED_CODE:                 "enable_ws": {
# REMOVED_UNUSED_CODE:                     "description": "Enable WebSocket connections to the exchange.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": True,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "key": {
# REMOVED_UNUSED_CODE:                     "description": "API key for the exchange.",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "default": "",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "secret": {
# REMOVED_UNUSED_CODE:                     "description": "API secret for the exchange.",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "default": "",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "password": {
# REMOVED_UNUSED_CODE:                     "description": "Password for the exchange, if required.",
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "default": "",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "uid": {"description": "User ID for the exchange, if required.", "type": "string"},
# REMOVED_UNUSED_CODE:                 "pair_whitelist": {
# REMOVED_UNUSED_CODE:                     "description": "List of whitelisted trading pairs.",
# REMOVED_UNUSED_CODE:                     "type": "array",
# REMOVED_UNUSED_CODE:                     "items": {"type": "string"},
# REMOVED_UNUSED_CODE:                     "uniqueItems": True,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "pair_blacklist": {
# REMOVED_UNUSED_CODE:                     "description": "List of blacklisted trading pairs.",
# REMOVED_UNUSED_CODE:                     "type": "array",
# REMOVED_UNUSED_CODE:                     "items": {"type": "string"},
# REMOVED_UNUSED_CODE:                     "uniqueItems": True,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "log_responses": {
# REMOVED_UNUSED_CODE:                     "description": (
# REMOVED_UNUSED_CODE:                         "Log responses from the exchange."
# REMOVED_UNUSED_CODE:                         "Useful/required to debug issues with order processing."
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": False,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "unknown_fee_rate": {
# REMOVED_UNUSED_CODE:                     "description": "Fee rate for unknown markets.",
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "outdated_offset": {
# REMOVED_UNUSED_CODE:                     "description": "Offset for outdated data in minutes.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "minimum": 1,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "markets_refresh_interval": {
# REMOVED_UNUSED_CODE:                     "description": "Interval for refreshing market data in minutes.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "default": 60,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "ccxt_config": {"description": "CCXT configuration settings.", "type": "object"},
# REMOVED_UNUSED_CODE:                 "ccxt_async_config": {
# REMOVED_UNUSED_CODE:                     "description": "CCXT asynchronous configuration settings.",
# REMOVED_UNUSED_CODE:                     "type": "object",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": ["name"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "edge": {
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "enabled": {"type": "boolean"},
# REMOVED_UNUSED_CODE:                 "process_throttle_secs": {"type": "integer", "minimum": 600},
# REMOVED_UNUSED_CODE:                 "calculate_since_number_of_days": {"type": "integer"},
# REMOVED_UNUSED_CODE:                 "allowed_risk": {"type": "number"},
# REMOVED_UNUSED_CODE:                 "stoploss_range_min": {"type": "number"},
# REMOVED_UNUSED_CODE:                 "stoploss_range_max": {"type": "number"},
# REMOVED_UNUSED_CODE:                 "stoploss_range_step": {"type": "number"},
# REMOVED_UNUSED_CODE:                 "minimum_winrate": {"type": "number"},
# REMOVED_UNUSED_CODE:                 "minimum_expectancy": {"type": "number"},
# REMOVED_UNUSED_CODE:                 "min_trade_number": {"type": "number"},
# REMOVED_UNUSED_CODE:                 "max_trade_duration_minute": {"type": "integer"},
# REMOVED_UNUSED_CODE:                 "remove_pumps": {"type": "boolean"},
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": ["process_throttle_secs", "allowed_risk"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "external_message_consumer": {
# REMOVED_UNUSED_CODE:             "description": "Configuration for external message consumer.",
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "enabled": {
# REMOVED_UNUSED_CODE:                     "description": "Whether the external message consumer is enabled.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": False,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "producers": {
# REMOVED_UNUSED_CODE:                     "description": "List of producers for the external message consumer.",
# REMOVED_UNUSED_CODE:                     "type": "array",
# REMOVED_UNUSED_CODE:                     "items": {
# REMOVED_UNUSED_CODE:                         "type": "object",
# REMOVED_UNUSED_CODE:                         "properties": {
# REMOVED_UNUSED_CODE:                             "name": {
# REMOVED_UNUSED_CODE:                                 "description": "Name of the producer.",
# REMOVED_UNUSED_CODE:                                 "type": "string",
# REMOVED_UNUSED_CODE:                             },
# REMOVED_UNUSED_CODE:                             "host": {
# REMOVED_UNUSED_CODE:                                 "description": "Host of the producer.",
# REMOVED_UNUSED_CODE:                                 "type": "string",
# REMOVED_UNUSED_CODE:                             },
# REMOVED_UNUSED_CODE:                             "port": {
# REMOVED_UNUSED_CODE:                                 "description": "Port of the producer.",
# REMOVED_UNUSED_CODE:                                 "type": "integer",
# REMOVED_UNUSED_CODE:                                 "default": 8080,
# REMOVED_UNUSED_CODE:                                 "minimum": 0,
# REMOVED_UNUSED_CODE:                                 "maximum": 65535,
# REMOVED_UNUSED_CODE:                             },
# REMOVED_UNUSED_CODE:                             "secure": {
# REMOVED_UNUSED_CODE:                                 "description": "Whether to use SSL to connect to the producer.",
# REMOVED_UNUSED_CODE:                                 "type": "boolean",
# REMOVED_UNUSED_CODE:                                 "default": False,
# REMOVED_UNUSED_CODE:                             },
# REMOVED_UNUSED_CODE:                             "ws_token": {
# REMOVED_UNUSED_CODE:                                 "description": "WebSocket token for the producer.",
# REMOVED_UNUSED_CODE:                                 "type": "string",
# REMOVED_UNUSED_CODE:                             },
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "required": ["name", "host", "ws_token"],
# REMOVED_UNUSED_CODE:                     },
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "wait_timeout": {
# REMOVED_UNUSED_CODE:                     "description": "Wait timeout in seconds.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "minimum": 0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "sleep_time": {
# REMOVED_UNUSED_CODE:                     "description": "Sleep time in seconds before retrying to connect.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "minimum": 0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "ping_timeout": {
# REMOVED_UNUSED_CODE:                     "description": "Ping timeout in seconds.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "minimum": 0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "remove_entry_exit_signals": {
# REMOVED_UNUSED_CODE:                     "description": "Remove signal columns from the dataframe (set them to 0)",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": False,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "initial_candle_limit": {
# REMOVED_UNUSED_CODE:                     "description": "Initial candle limit.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "minimum": 0,
# REMOVED_UNUSED_CODE:                     "maximum": 1500,
# REMOVED_UNUSED_CODE:                     "default": 1500,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "message_size_limit": {
# REMOVED_UNUSED_CODE:                     "description": "Message size limit in megabytes.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "minimum": 1,
# REMOVED_UNUSED_CODE:                     "maximum": 20,
# REMOVED_UNUSED_CODE:                     "default": 8,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": ["producers"],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:         "freqai": {
# REMOVED_UNUSED_CODE:             "type": "object",
# REMOVED_UNUSED_CODE:             "properties": {
# REMOVED_UNUSED_CODE:                 "enabled": {
# REMOVED_UNUSED_CODE:                     "description": "Whether freqAI is enabled.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": False,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "keras": {
# REMOVED_UNUSED_CODE:                     "description": "Use Keras for model training.",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": False,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "write_metrics_to_disk": {
# REMOVED_UNUSED_CODE:                     "description": "Write metrics to disk?",
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": False,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "purge_old_models": {
# REMOVED_UNUSED_CODE:                     "description": "Number of models to keep on disk.",
# REMOVED_UNUSED_CODE:                     "type": ["boolean", "number"],
# REMOVED_UNUSED_CODE:                     "default": 2,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "conv_width": {
# REMOVED_UNUSED_CODE:                     "description": "The width of a neural network input tensor.",
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "default": 1,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "train_period_days": {
# REMOVED_UNUSED_CODE:                     "description": (
# REMOVED_UNUSED_CODE:                         "Number of days to use for the training data (width of the sliding window)"
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                     "type": "integer",
# REMOVED_UNUSED_CODE:                     "default": 0,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "backtest_period_days": {
# REMOVED_UNUSED_CODE:                     "description": (
# REMOVED_UNUSED_CODE:                         "Number of days to inference from the trained model before sliding the "
# REMOVED_UNUSED_CODE:                         "`train_period_days` window "
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                     "type": "number",
# REMOVED_UNUSED_CODE:                     "default": 7,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "identifier": {
# REMOVED_UNUSED_CODE:                     "description": (
# REMOVED_UNUSED_CODE:                         "A unique ID for the current model. "
# REMOVED_UNUSED_CODE:                         "Must be changed when modifying features."
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                     "type": "string",
# REMOVED_UNUSED_CODE:                     "default": "example",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "wait_for_training_iteration_on_reload": {
# REMOVED_UNUSED_CODE:                     "description": (
# REMOVED_UNUSED_CODE:                         "Wait for the next training iteration to complete after /reload or ctrl+c."
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                     "type": "boolean",
# REMOVED_UNUSED_CODE:                     "default": True,
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "feature_parameters": {
# REMOVED_UNUSED_CODE:                     "description": "The parameters used to engineer the feature set",
# REMOVED_UNUSED_CODE:                     "type": "object",
# REMOVED_UNUSED_CODE:                     "properties": {
# REMOVED_UNUSED_CODE:                         "include_corr_pairlist": {
# REMOVED_UNUSED_CODE:                             "description": "List of correlated pairs to include in the features.",
# REMOVED_UNUSED_CODE:                             "type": "array",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "include_timeframes": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "A list of timeframes that all indicators in "
# REMOVED_UNUSED_CODE:                                 "`feature_engineering_expand_*()` will be created for."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "array",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "label_period_candles": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Number of candles into the future to use for labeling the period."
# REMOVED_UNUSED_CODE:                                 "This can be used in `set_freqai_targets()`."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "integer",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "include_shifted_candles": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Add features from previous candles to subsequent candles with "
# REMOVED_UNUSED_CODE:                                 "the intent of adding historical information."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "integer",
# REMOVED_UNUSED_CODE:                             "default": 0,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "DI_threshold": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Activates the use of the Dissimilarity Index for "
# REMOVED_UNUSED_CODE:                                 "outlier detection when set to > 0."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "number",
# REMOVED_UNUSED_CODE:                             "default": 0,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "weight_factor": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Weight training data points according to their recency."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "number",
# REMOVED_UNUSED_CODE:                             "default": 0,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "principal_component_analysis": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Automatically reduce the dimensionality of the data set using "
# REMOVED_UNUSED_CODE:                                 "Principal Component Analysis"
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "boolean",
# REMOVED_UNUSED_CODE:                             "default": False,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "use_SVM_to_remove_outliers": {
# REMOVED_UNUSED_CODE:                             "description": "Use SVM to remove outliers from the features.",
# REMOVED_UNUSED_CODE:                             "type": "boolean",
# REMOVED_UNUSED_CODE:                             "default": False,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "plot_feature_importances": {
# REMOVED_UNUSED_CODE:                             "description": "Create feature importance plots for each model.",
# REMOVED_UNUSED_CODE:                             "type": "integer",
# REMOVED_UNUSED_CODE:                             "default": 0,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "svm_params": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "All parameters available in Sklearn's `SGDOneClassSVM()`."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "object",
# REMOVED_UNUSED_CODE:                             "properties": {
# REMOVED_UNUSED_CODE:                                 "shuffle": {
# REMOVED_UNUSED_CODE:                                     "description": "Whether to shuffle data before applying SVM.",
# REMOVED_UNUSED_CODE:                                     "type": "boolean",
# REMOVED_UNUSED_CODE:                                     "default": False,
# REMOVED_UNUSED_CODE:                                 },
# REMOVED_UNUSED_CODE:                                 "nu": {
# REMOVED_UNUSED_CODE:                                     "type": "number",
# REMOVED_UNUSED_CODE:                                     "default": 0.1,
# REMOVED_UNUSED_CODE:                                 },
# REMOVED_UNUSED_CODE:                             },
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "shuffle_after_split": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Split the data into train and test sets, and then shuffle "
# REMOVED_UNUSED_CODE:                                 "both sets individually."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "boolean",
# REMOVED_UNUSED_CODE:                             "default": False,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "buffer_train_data_candles": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Cut `buffer_train_data_candles` off the beginning and end of the "
# REMOVED_UNUSED_CODE:                                 "training data *after* the indicators were populated."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "integer",
# REMOVED_UNUSED_CODE:                             "default": 0,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                     },
# REMOVED_UNUSED_CODE:                     "required": [
# REMOVED_UNUSED_CODE:                         "include_timeframes",
# REMOVED_UNUSED_CODE:                         "include_corr_pairlist",
# REMOVED_UNUSED_CODE:                     ],
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "data_split_parameters": {
# REMOVED_UNUSED_CODE:                     "descriptions": (
# REMOVED_UNUSED_CODE:                         "Additional parameters for scikit-learn's test_train_split() function."
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                     "type": "object",
# REMOVED_UNUSED_CODE:                     "properties": {
# REMOVED_UNUSED_CODE:                         "test_size": {"type": "number"},
# REMOVED_UNUSED_CODE:                         "random_state": {"type": "integer"},
# REMOVED_UNUSED_CODE:                         "shuffle": {"type": "boolean", "default": False},
# REMOVED_UNUSED_CODE:                     },
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "model_training_parameters": {
# REMOVED_UNUSED_CODE:                     "description": (
# REMOVED_UNUSED_CODE:                         "Flexible dictionary that includes all parameters available by "
# REMOVED_UNUSED_CODE:                         "the selected model library. "
# REMOVED_UNUSED_CODE:                     ),
# REMOVED_UNUSED_CODE:                     "type": "object",
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:                 "rl_config": {
# REMOVED_UNUSED_CODE:                     "type": "object",
# REMOVED_UNUSED_CODE:                     "properties": {
# REMOVED_UNUSED_CODE:                         "drop_ohlc_from_features": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Do not include the normalized ohlc data in the feature set."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "boolean",
# REMOVED_UNUSED_CODE:                             "default": False,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "train_cycles": {
# REMOVED_UNUSED_CODE:                             "description": "Number of training cycles to perform.",
# REMOVED_UNUSED_CODE:                             "type": "integer",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "max_trade_duration_candles": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Guides the agent training to keep trades below desired length."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "integer",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "add_state_info": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Include state information in the feature set for "
# REMOVED_UNUSED_CODE:                                 "training and inference."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "boolean",
# REMOVED_UNUSED_CODE:                             "default": False,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "max_training_drawdown_pct": {
# REMOVED_UNUSED_CODE:                             "description": "Maximum allowed drawdown percentage during training.",
# REMOVED_UNUSED_CODE:                             "type": "number",
# REMOVED_UNUSED_CODE:                             "default": 0.02,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "cpu_count": {
# REMOVED_UNUSED_CODE:                             "description": "Number of threads/CPU's to use for training.",
# REMOVED_UNUSED_CODE:                             "type": "integer",
# REMOVED_UNUSED_CODE:                             "default": 1,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "model_type": {
# REMOVED_UNUSED_CODE:                             "description": "Model string from stable_baselines3 or SBcontrib.",
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "default": "PPO",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "policy_type": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "One of the available policy types from stable_baselines3."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "string",
# REMOVED_UNUSED_CODE:                             "default": "MlpPolicy",
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "net_arch": {
# REMOVED_UNUSED_CODE:                             "description": "Architecture of the neural network.",
# REMOVED_UNUSED_CODE:                             "type": "array",
# REMOVED_UNUSED_CODE:                             "default": [128, 128],
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "randomize_starting_position": {
# REMOVED_UNUSED_CODE:                             "description": (
# REMOVED_UNUSED_CODE:                                 "Randomize the starting point of each episode to avoid overfitting."
# REMOVED_UNUSED_CODE:                             ),
# REMOVED_UNUSED_CODE:                             "type": "boolean",
# REMOVED_UNUSED_CODE:                             "default": False,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "progress_bar": {
# REMOVED_UNUSED_CODE:                             "description": "Display a progress bar with the current progress.",
# REMOVED_UNUSED_CODE:                             "type": "boolean",
# REMOVED_UNUSED_CODE:                             "default": True,
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                         "model_reward_parameters": {
# REMOVED_UNUSED_CODE:                             "description": "Parameters for configuring the reward model.",
# REMOVED_UNUSED_CODE:                             "type": "object",
# REMOVED_UNUSED_CODE:                             "properties": {
# REMOVED_UNUSED_CODE:                                 "rr": {
# REMOVED_UNUSED_CODE:                                     "type": "number",
# REMOVED_UNUSED_CODE:                                     "default": 1,
# REMOVED_UNUSED_CODE:                                     "description": "Reward ratio parameter.",
# REMOVED_UNUSED_CODE:                                 },
# REMOVED_UNUSED_CODE:                                 "profit_aim": {
# REMOVED_UNUSED_CODE:                                     "type": "number",
# REMOVED_UNUSED_CODE:                                     "default": 0.025,
# REMOVED_UNUSED_CODE:                                     "description": "Profit aim parameter.",
# REMOVED_UNUSED_CODE:                                 },
# REMOVED_UNUSED_CODE:                             },
# REMOVED_UNUSED_CODE:                         },
# REMOVED_UNUSED_CODE:                     },
# REMOVED_UNUSED_CODE:                 },
# REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE:             "required": [
# REMOVED_UNUSED_CODE:                 "enabled",
# REMOVED_UNUSED_CODE:                 "train_period_days",
# REMOVED_UNUSED_CODE:                 "backtest_period_days",
# REMOVED_UNUSED_CODE:                 "identifier",
# REMOVED_UNUSED_CODE:                 "feature_parameters",
# REMOVED_UNUSED_CODE:                 "data_split_parameters",
# REMOVED_UNUSED_CODE:             ],
# REMOVED_UNUSED_CODE:         },
# REMOVED_UNUSED_CODE:     },
# REMOVED_UNUSED_CODE: }

# REMOVED_UNUSED_CODE: SCHEMA_TRADE_REQUIRED = [
# REMOVED_UNUSED_CODE:     "exchange",
# REMOVED_UNUSED_CODE:     "timeframe",
# REMOVED_UNUSED_CODE:     "max_open_trades",
# REMOVED_UNUSED_CODE:     "stake_currency",
# REMOVED_UNUSED_CODE:     "stake_amount",
# REMOVED_UNUSED_CODE:     "tradable_balance_ratio",
# REMOVED_UNUSED_CODE:     "last_stake_amount_min_ratio",
# REMOVED_UNUSED_CODE:     "dry_run",
# REMOVED_UNUSED_CODE:     "dry_run_wallet",
# REMOVED_UNUSED_CODE:     "exit_pricing",
# REMOVED_UNUSED_CODE:     "entry_pricing",
# REMOVED_UNUSED_CODE:     "stoploss",
# REMOVED_UNUSED_CODE:     "minimal_roi",
# REMOVED_UNUSED_CODE:     "internals",
# REMOVED_UNUSED_CODE:     "dataformat_ohlcv",
# REMOVED_UNUSED_CODE:     "dataformat_trades",
# REMOVED_UNUSED_CODE: ]

SCHEMA_BACKTEST_REQUIRED = [
    "exchange",
    "stake_currency",
    "stake_amount",
    "dry_run_wallet",
    "dataformat_ohlcv",
    "dataformat_trades",
]
SCHEMA_BACKTEST_REQUIRED_FINAL = SCHEMA_BACKTEST_REQUIRED + [
    "stoploss",
    "minimal_roi",
    "max_open_trades",
]

# REMOVED_UNUSED_CODE: SCHEMA_MINIMAL_REQUIRED = [
# REMOVED_UNUSED_CODE:     "exchange",
# REMOVED_UNUSED_CODE:     "dry_run",
# REMOVED_UNUSED_CODE:     "dataformat_ohlcv",
# REMOVED_UNUSED_CODE:     "dataformat_trades",
# REMOVED_UNUSED_CODE: ]
# REMOVED_UNUSED_CODE: SCHEMA_MINIMAL_WEBSERVER = SCHEMA_MINIMAL_REQUIRED + [
# REMOVED_UNUSED_CODE:     "api_server",
# REMOVED_UNUSED_CODE: ]
