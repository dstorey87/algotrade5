# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from datetime import datetime, timedelta, timezone

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.persistence.models import Order, Trade


# REMOVED_UNUSED_CODE: MOCK_TRADE_COUNT = 6


# REMOVED_UNUSED_CODE: def entry_side(is_short: bool):
# REMOVED_UNUSED_CODE:     return "sell" if is_short else "buy"


# REMOVED_UNUSED_CODE: def exit_side(is_short: bool):
# REMOVED_UNUSED_CODE:     return "buy" if is_short else "sell"


# REMOVED_UNUSED_CODE: def direc(is_short: bool):
# REMOVED_UNUSED_CODE:     return "short" if is_short else "long"


# REMOVED_UNUSED_CODE: def mock_order_usdt_1(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"prod_entry_1_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "LTC/USDT",
# REMOVED_UNUSED_CODE:         "status": "closed",
# REMOVED_UNUSED_CODE:         "side": entry_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 10.0,
# REMOVED_UNUSED_CODE:         "amount": 2.0,
# REMOVED_UNUSED_CODE:         "filled": 2.0,
# REMOVED_UNUSED_CODE:         "remaining": 0.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_order_usdt_1_exit(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"prod_exit_1_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "LTC/USDT",
# REMOVED_UNUSED_CODE:         "status": "open",
# REMOVED_UNUSED_CODE:         "side": exit_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 8.0,
# REMOVED_UNUSED_CODE:         "amount": 2.0,
# REMOVED_UNUSED_CODE:         "filled": 0.0,
# REMOVED_UNUSED_CODE:         "remaining": 2.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_trade_usdt_1(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Simulate prod entry with open sell order
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="LTC/USDT",
# REMOVED_UNUSED_CODE:         stake_amount=20.0,
# REMOVED_UNUSED_CODE:         amount=2.0,
# REMOVED_UNUSED_CODE:         amount_requested=2.0,
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(days=2, minutes=20),
# REMOVED_UNUSED_CODE:         close_date=datetime.now(tz=timezone.utc) - timedelta(days=2, minutes=5),
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         is_open=False,
# REMOVED_UNUSED_CODE:         open_rate=10.0,
# REMOVED_UNUSED_CODE:         close_rate=8.0,
# REMOVED_UNUSED_CODE:         close_profit=-0.2,
# REMOVED_UNUSED_CODE:         close_profit_abs=-4.09,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         strategy="SampleStrategy",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_usdt_1(is_short), "LTC/USDT", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(
# REMOVED_UNUSED_CODE:         mock_order_usdt_1_exit(is_short), "LTC/USDT", exit_side(is_short)
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


# REMOVED_UNUSED_CODE: def mock_order_usdt_2(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"1235_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "NEO/USDT",
# REMOVED_UNUSED_CODE:         "status": "closed",
# REMOVED_UNUSED_CODE:         "side": entry_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 2.0,
# REMOVED_UNUSED_CODE:         "amount": 100.0,
# REMOVED_UNUSED_CODE:         "filled": 100.0,
# REMOVED_UNUSED_CODE:         "remaining": 0.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_order_usdt_2_exit(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"12366_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "NEO/USDT",
# REMOVED_UNUSED_CODE:         "status": "open",
# REMOVED_UNUSED_CODE:         "side": exit_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 2.05,
# REMOVED_UNUSED_CODE:         "amount": 100.0,
# REMOVED_UNUSED_CODE:         "filled": 0.0,
# REMOVED_UNUSED_CODE:         "remaining": 100.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_trade_usdt_2(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Closed trade...
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="NEO/USDT",
# REMOVED_UNUSED_CODE:         stake_amount=200.0,
# REMOVED_UNUSED_CODE:         amount=100.0,
# REMOVED_UNUSED_CODE:         amount_requested=100.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_rate=2.0,
# REMOVED_UNUSED_CODE:         close_rate=2.05,
# REMOVED_UNUSED_CODE:         close_profit=0.05,
# REMOVED_UNUSED_CODE:         close_profit_abs=3.9875,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         is_open=False,
# REMOVED_UNUSED_CODE:         strategy="StrategyTestV2",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         enter_tag="TEST1",
# REMOVED_UNUSED_CODE:         exit_reason="exit_signal",
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=20),
# REMOVED_UNUSED_CODE:         close_date=datetime.now(tz=timezone.utc) - timedelta(minutes=2),
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_usdt_2(is_short), "NEO/USDT", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(
# REMOVED_UNUSED_CODE:         mock_order_usdt_2_exit(is_short), "NEO/USDT", exit_side(is_short)
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


# REMOVED_UNUSED_CODE: def mock_order_usdt_3(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"41231a12a_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "XRP/USDT",
# REMOVED_UNUSED_CODE:         "status": "closed",
# REMOVED_UNUSED_CODE:         "side": entry_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 1.0,
# REMOVED_UNUSED_CODE:         "amount": 30.0,
# REMOVED_UNUSED_CODE:         "filled": 30.0,
# REMOVED_UNUSED_CODE:         "remaining": 0.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_order_usdt_3_exit(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"41231a666a_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "XRP/USDT",
# REMOVED_UNUSED_CODE:         "status": "closed",
# REMOVED_UNUSED_CODE:         "side": exit_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "stop_loss_limit",
# REMOVED_UNUSED_CODE:         "price": 1.1,
# REMOVED_UNUSED_CODE:         "average": 1.1,
# REMOVED_UNUSED_CODE:         "amount": 30.0,
# REMOVED_UNUSED_CODE:         "filled": 30.0,
# REMOVED_UNUSED_CODE:         "remaining": 0.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_trade_usdt_3(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Closed trade
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="XRP/USDT",
# REMOVED_UNUSED_CODE:         stake_amount=30.0,
# REMOVED_UNUSED_CODE:         amount=30.0,
# REMOVED_UNUSED_CODE:         amount_requested=30.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_rate=1.0,
# REMOVED_UNUSED_CODE:         close_rate=1.1,
# REMOVED_UNUSED_CODE:         close_profit=0.1,
# REMOVED_UNUSED_CODE:         close_profit_abs=2.8425,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         is_open=False,
# REMOVED_UNUSED_CODE:         strategy="StrategyTestV2",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         enter_tag="TEST3",
# REMOVED_UNUSED_CODE:         exit_reason="roi",
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=20),
# REMOVED_UNUSED_CODE:         close_date=datetime.now(tz=timezone.utc),
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_usdt_3(is_short), "XRP/USDT", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(
# REMOVED_UNUSED_CODE:         mock_order_usdt_3_exit(is_short), "XRP/USDT", exit_side(is_short)
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


# REMOVED_UNUSED_CODE: def mock_order_usdt_4(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"prod_buy_12345_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "NEO/USDT",
# REMOVED_UNUSED_CODE:         "status": "open",
# REMOVED_UNUSED_CODE:         "side": entry_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 2.0,
# REMOVED_UNUSED_CODE:         "amount": 10.0,
# REMOVED_UNUSED_CODE:         "filled": 0.0,
# REMOVED_UNUSED_CODE:         "remaining": 30.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_trade_usdt_4(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Simulate prod entry
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="NEO/USDT",
# REMOVED_UNUSED_CODE:         stake_amount=20.0,
# REMOVED_UNUSED_CODE:         amount=0.0,
# REMOVED_UNUSED_CODE:         amount_requested=10.01,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=14),
# REMOVED_UNUSED_CODE:         is_open=True,
# REMOVED_UNUSED_CODE:         open_rate=2.0,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         strategy="StrategyTestV2",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_usdt_4(is_short), "NEO/USDT", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


# REMOVED_UNUSED_CODE: def mock_order_usdt_5(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"prod_buy_3455_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "XRP/USDT",
# REMOVED_UNUSED_CODE:         "status": "closed",
# REMOVED_UNUSED_CODE:         "side": entry_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 2.0,
# REMOVED_UNUSED_CODE:         "amount": 10.0,
# REMOVED_UNUSED_CODE:         "filled": 10.0,
# REMOVED_UNUSED_CODE:         "remaining": 0.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_order_usdt_5_stoploss(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"prod_stoploss_3455_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "XRP/USDT",
# REMOVED_UNUSED_CODE:         "status": "open",
# REMOVED_UNUSED_CODE:         "side": exit_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "stop_loss_limit",
# REMOVED_UNUSED_CODE:         "price": 2.0,
# REMOVED_UNUSED_CODE:         "amount": 10.0,
# REMOVED_UNUSED_CODE:         "filled": 0.0,
# REMOVED_UNUSED_CODE:         "remaining": 30.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_trade_usdt_5(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Simulate prod entry with stoploss
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="XRP/USDT",
# REMOVED_UNUSED_CODE:         stake_amount=20.0,
# REMOVED_UNUSED_CODE:         amount=10.0,
# REMOVED_UNUSED_CODE:         amount_requested=10.01,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=12),
# REMOVED_UNUSED_CODE:         is_open=True,
# REMOVED_UNUSED_CODE:         open_rate=2.0,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         strategy="SampleStrategy",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_usdt_5(is_short), "XRP/USDT", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_usdt_5_stoploss(is_short), "XRP/USDT", "stoploss")
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


# REMOVED_UNUSED_CODE: def mock_order_usdt_6(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"prod_entry_6_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "LTC/USDT",
# REMOVED_UNUSED_CODE:         "status": "closed",
# REMOVED_UNUSED_CODE:         "side": entry_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 10.0,
# REMOVED_UNUSED_CODE:         "amount": 2.0,
# REMOVED_UNUSED_CODE:         "filled": 2.0,
# REMOVED_UNUSED_CODE:         "remaining": 0.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_order_usdt_6_exit(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"prod_exit_6_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "LTC/USDT",
# REMOVED_UNUSED_CODE:         "status": "open",
# REMOVED_UNUSED_CODE:         "side": exit_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 12.0,
# REMOVED_UNUSED_CODE:         "amount": 2.0,
# REMOVED_UNUSED_CODE:         "filled": 0.0,
# REMOVED_UNUSED_CODE:         "remaining": 2.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_trade_usdt_6(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Simulate prod entry with open sell order
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="LTC/USDT",
# REMOVED_UNUSED_CODE:         stake_amount=20.0,
# REMOVED_UNUSED_CODE:         amount=2.0,
# REMOVED_UNUSED_CODE:         amount_requested=2.0,
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=5),
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         is_open=True,
# REMOVED_UNUSED_CODE:         open_rate=10.0,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         strategy="SampleStrategy",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_usdt_6(is_short), "LTC/USDT", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(
# REMOVED_UNUSED_CODE:         mock_order_usdt_6_exit(is_short), "LTC/USDT", exit_side(is_short)
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


# REMOVED_UNUSED_CODE: def mock_order_usdt_7(is_short: bool):
# REMOVED_UNUSED_CODE:     return {
# REMOVED_UNUSED_CODE:         "id": f"1234_{direc(is_short)}",
# REMOVED_UNUSED_CODE:         "symbol": "ADA/USDT",
# REMOVED_UNUSED_CODE:         "status": "closed",
# REMOVED_UNUSED_CODE:         "side": entry_side(is_short),
# REMOVED_UNUSED_CODE:         "type": "limit",
# REMOVED_UNUSED_CODE:         "price": 2.0,
# REMOVED_UNUSED_CODE:         "amount": 10.0,
# REMOVED_UNUSED_CODE:         "filled": 10.0,
# REMOVED_UNUSED_CODE:         "remaining": 0.0,
# REMOVED_UNUSED_CODE:     }


# REMOVED_UNUSED_CODE: def mock_trade_usdt_7(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="ADA/USDT",
# REMOVED_UNUSED_CODE:         stake_amount=20.0,
# REMOVED_UNUSED_CODE:         amount=10.0,
# REMOVED_UNUSED_CODE:         amount_requested=10.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         is_open=True,
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=17),
# REMOVED_UNUSED_CODE:         open_rate=2.0,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         strategy="StrategyTestV2",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_usdt_7(is_short), "ADA/USDT", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade
