from datetime import datetime, timedelta, timezone

from freqtrade.persistence.models import Order, Trade


# REMOVED_UNUSED_CODE: MOCK_TRADE_COUNT = 6


def entry_side(is_short: bool):
    return "sell" if is_short else "buy"


def exit_side(is_short: bool):
    return "buy" if is_short else "sell"


def direc(is_short: bool):
    return "short" if is_short else "long"


def mock_order_1(is_short: bool):
    return {
        "id": f"1234_{direc(is_short)}",
        "symbol": "ETH/BTC",
        "status": "open",
        "side": entry_side(is_short),
        "type": "limit",
        "price": 0.123,
        "average": 0.123,
        "amount": 123.0,
        "filled": 50.0,
        "cost": 15.129,
        "remaining": 123.0 - 50.0,
    }


# REMOVED_UNUSED_CODE: def mock_trade_1(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="ETH/BTC",
# REMOVED_UNUSED_CODE:         stake_amount=0.001,
# REMOVED_UNUSED_CODE:         amount=50.0,
# REMOVED_UNUSED_CODE:         amount_requested=123.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         is_open=True,
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=17),
# REMOVED_UNUSED_CODE:         open_rate=0.123,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         strategy="StrategyTestV3",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_1(is_short), "ETH/BTC", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


def mock_order_2(is_short: bool):
    return {
        "id": f"1235_{direc(is_short)}",
        "symbol": "ETC/BTC",
        "status": "closed",
        "side": entry_side(is_short),
        "type": "limit",
        "price": 0.123,
        "amount": 123.0,
        "filled": 123.0,
        "cost": 15.129,
        "remaining": 0.0,
    }


def mock_order_2_sell(is_short: bool):
    return {
        "id": f"12366_{direc(is_short)}",
        "symbol": "ETC/BTC",
        "status": "closed",
        "side": exit_side(is_short),
        "type": "limit",
        "price": 0.128,
        "amount": 123.0,
        "filled": 123.0,
        "cost": 15.129,
        "remaining": 0.0,
    }


# REMOVED_UNUSED_CODE: def mock_trade_2(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Closed trade...
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="ETC/BTC",
# REMOVED_UNUSED_CODE:         stake_amount=0.001,
# REMOVED_UNUSED_CODE:         amount=123.0,
# REMOVED_UNUSED_CODE:         amount_requested=123.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_rate=0.123,
# REMOVED_UNUSED_CODE:         close_rate=0.128,
# REMOVED_UNUSED_CODE:         close_profit=-0.005 if is_short else 0.005,
# REMOVED_UNUSED_CODE:         close_profit_abs=-0.005584127 if is_short else 0.000584127,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         is_open=False,
# REMOVED_UNUSED_CODE:         strategy="StrategyTestV3",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         enter_tag="TEST1",
# REMOVED_UNUSED_CODE:         exit_reason="sell_signal",
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=20),
# REMOVED_UNUSED_CODE:         close_date=datetime.now(tz=timezone.utc) - timedelta(minutes=2),
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_2(is_short), "ETC/BTC", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_2_sell(is_short), "ETC/BTC", exit_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


def mock_order_3(is_short: bool):
    return {
        "id": f"41231a12a_{direc(is_short)}",
        "symbol": "XRP/BTC",
        "status": "closed",
        "side": entry_side(is_short),
        "type": "limit",
        "price": 0.05,
        "amount": 123.0,
        "filled": 123.0,
        "cost": 15.129,
        "remaining": 0.0,
    }


def mock_order_3_sell(is_short: bool):
    return {
        "id": f"41231a666a_{direc(is_short)}",
        "symbol": "XRP/BTC",
        "status": "closed",
        "side": exit_side(is_short),
        "type": "stop_loss_limit",
        "price": 0.06,
        "average": 0.06,
        "amount": 123.0,
        "filled": 123.0,
        "cost": 15.129,
        "remaining": 0.0,
    }


# REMOVED_UNUSED_CODE: def mock_trade_3(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Closed trade
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="XRP/BTC",
# REMOVED_UNUSED_CODE:         stake_amount=0.001,
# REMOVED_UNUSED_CODE:         amount=123.0,
# REMOVED_UNUSED_CODE:         amount_requested=123.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_rate=0.05,
# REMOVED_UNUSED_CODE:         close_rate=0.06,
# REMOVED_UNUSED_CODE:         close_profit=-0.01 if is_short else 0.01,
# REMOVED_UNUSED_CODE:         close_profit_abs=-0.001155 if is_short else 0.000155,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         is_open=False,
# REMOVED_UNUSED_CODE:         strategy="StrategyTestV3",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         exit_reason="roi",
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=20),
# REMOVED_UNUSED_CODE:         close_date=datetime.now(tz=timezone.utc),
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_3(is_short), "XRP/BTC", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_3_sell(is_short), "XRP/BTC", exit_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


def mock_order_4(is_short: bool):
    return {
        "id": f"prod_buy_{direc(is_short)}_12345",
        "symbol": "ETC/BTC",
        "status": "open",
        "side": entry_side(is_short),
        "type": "limit",
        "price": 0.123,
        "amount": 123.0,
        "filled": 0.0,
        "cost": 15.129,
        "remaining": 123.0,
    }


# REMOVED_UNUSED_CODE: def mock_trade_4(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Simulate prod entry
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="ETC/BTC",
# REMOVED_UNUSED_CODE:         stake_amount=0.001,
# REMOVED_UNUSED_CODE:         amount=0.0,
# REMOVED_UNUSED_CODE:         amount_requested=124.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=14),
# REMOVED_UNUSED_CODE:         is_open=True,
# REMOVED_UNUSED_CODE:         open_rate=0.123,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         strategy="StrategyTestV3",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:         stop_loss_pct=0.10,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_4(is_short), "ETC/BTC", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


def mock_order_5(is_short: bool):
    return {
        "id": f"prod_buy_{direc(is_short)}_3455",
        "symbol": "XRP/BTC",
        "status": "closed",
        "side": entry_side(is_short),
        "type": "limit",
        "price": 0.123,
        "amount": 123.0,
        "filled": 123.0,
        "cost": 15.129,
        "remaining": 0.0,
    }


def mock_order_5_stoploss(is_short: bool):
    return {
        "id": f"prod_stoploss_{direc(is_short)}_3455",
        "symbol": "XRP/BTC",
        "status": "open",
        "side": exit_side(is_short),
        "type": "stop_loss_limit",
        "price": 0.123,
        "amount": 123.0,
        "filled": 0.0,
        "cost": 0.0,
        "remaining": 123.0,
    }


# REMOVED_UNUSED_CODE: def mock_trade_5(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Simulate prod entry with stoploss
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="XRP/BTC",
# REMOVED_UNUSED_CODE:         stake_amount=0.001,
# REMOVED_UNUSED_CODE:         amount=123.0,
# REMOVED_UNUSED_CODE:         amount_requested=124.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=12),
# REMOVED_UNUSED_CODE:         is_open=True,
# REMOVED_UNUSED_CODE:         open_rate=0.123,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         strategy="SampleStrategy",
# REMOVED_UNUSED_CODE:         enter_tag="TEST1",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:         stop_loss_pct=0.10,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_5(is_short), "XRP/BTC", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_5_stoploss(is_short), "XRP/BTC", "stoploss")
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


def mock_order_6(is_short: bool):
    return {
        "id": f"prod_buy_{direc(is_short)}_6",
        "symbol": "LTC/BTC",
        "status": "closed",
        "side": entry_side(is_short),
        "type": "limit",
        "price": 0.15,
        "amount": 2.0,
        "filled": 2.0,
        "cost": 0.3,
        "remaining": 0.0,
    }


def mock_order_6_sell(is_short: bool):
    return {
        "id": f"prod_sell_{direc(is_short)}_6",
        "symbol": "LTC/BTC",
        "status": "open",
        "side": exit_side(is_short),
        "type": "limit",
        "price": 0.15 if is_short else 0.20,
        "amount": 2.0,
        "filled": 0.0,
        "cost": 0.0,
        "remaining": 2.0,
    }


# REMOVED_UNUSED_CODE: def mock_trade_6(fee, is_short: bool):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Simulate prod entry with open exit order
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="LTC/BTC",
# REMOVED_UNUSED_CODE:         stake_amount=0.001,
# REMOVED_UNUSED_CODE:         amount=2.0,
# REMOVED_UNUSED_CODE:         amount_requested=2.0,
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=5),
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         is_open=True,
# REMOVED_UNUSED_CODE:         open_rate=0.15,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         strategy="SampleStrategy",
# REMOVED_UNUSED_CODE:         enter_tag="TEST2",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         is_short=is_short,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_6(is_short), "LTC/BTC", entry_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(mock_order_6_sell(is_short), "LTC/BTC", exit_side(is_short))
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


def short_order():
    return {
        "id": "1236",
        "symbol": "ETC/BTC",
        "status": "closed",
        "side": "sell",
        "type": "limit",
        "price": 0.123,
        "amount": 123.0,
        "filled": 123.0,
        "cost": 15.129,
        "remaining": 0.0,
    }


def exit_short_order():
    return {
        "id": "12367",
        "symbol": "ETC/BTC",
        "status": "closed",
        "side": "buy",
        "type": "limit",
        "price": 0.128,
        "amount": 123.0,
        "filled": 123.0,
        "cost": 15.744,
        "remaining": 0.0,
    }


# REMOVED_UNUSED_CODE: def short_trade(fee):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     10 minute short limit trade on binance
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Short trade
# REMOVED_UNUSED_CODE:     fee: 0.25% base
# REMOVED_UNUSED_CODE:     interest_rate: 0.05% per day
# REMOVED_UNUSED_CODE:     open_rate: 0.123 base
# REMOVED_UNUSED_CODE:     close_rate: 0.128 base
# REMOVED_UNUSED_CODE:     amount: 123.0 crypto
# REMOVED_UNUSED_CODE:     stake_amount: 15.129 base
# REMOVED_UNUSED_CODE:     borrowed: 123.0  crypto
# REMOVED_UNUSED_CODE:     time-periods: 10 minutes(rounds up to 1/24 time-period of 1 day)
# REMOVED_UNUSED_CODE:     interest: borrowed * interest_rate * time-periods
# REMOVED_UNUSED_CODE:                 = 123.0 * 0.0005 * 1/24 = 0.0025625 crypto
# REMOVED_UNUSED_CODE:     open_value: (amount * open_rate) - (amount * open_rate * fee)
# REMOVED_UNUSED_CODE:         = (123 * 0.123) - (123 * 0.123 * 0.0025)
# REMOVED_UNUSED_CODE:         = 15.091177499999999
# REMOVED_UNUSED_CODE:     amount_closed: amount + interest = 123 + 0.0025625 = 123.0025625
# REMOVED_UNUSED_CODE:     close_value: (amount_closed * close_rate) + (amount_closed * close_rate * fee)
# REMOVED_UNUSED_CODE:         = (123.0025625 * 0.128) + (123.0025625 * 0.128 * 0.0025)
# REMOVED_UNUSED_CODE:         = 15.78368882
# REMOVED_UNUSED_CODE:     total_profit = open_value - close_value
# REMOVED_UNUSED_CODE:         = 15.091177499999999 - 15.78368882
# REMOVED_UNUSED_CODE:         = -0.6925113200000013
# REMOVED_UNUSED_CODE:     total_profit_percentage = total_profit / stake_amount
# REMOVED_UNUSED_CODE:         = -0.6925113200000013 / 15.129
# REMOVED_UNUSED_CODE:         = -0.04577376693766946
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="ETC/BTC",
# REMOVED_UNUSED_CODE:         stake_amount=15.129,
# REMOVED_UNUSED_CODE:         amount=123.0,
# REMOVED_UNUSED_CODE:         amount_requested=123.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_rate=0.123,
# REMOVED_UNUSED_CODE:         # close_rate=0.128,
# REMOVED_UNUSED_CODE:         # close_profit=-0.04577376693766946,
# REMOVED_UNUSED_CODE:         # close_profit_abs=-0.6925113200000013,
# REMOVED_UNUSED_CODE:         exchange="binance",
# REMOVED_UNUSED_CODE:         is_open=True,
# REMOVED_UNUSED_CODE:         strategy="DefaultStrategy",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         exit_reason="sell_signal",
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=20),
# REMOVED_UNUSED_CODE:         # close_date=datetime.now(tz=timezone.utc) - timedelta(minutes=2),
# REMOVED_UNUSED_CODE:         is_short=True,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(short_order(), "ETC/BTC", "sell")
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(exit_short_order(), "ETC/BTC", "sell")
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade


def leverage_order():
    return {
        "id": "1237",
        "symbol": "DOGE/BTC",
        "status": "closed",
        "side": "buy",
        "type": "limit",
        "price": 0.123,
        "amount": 123.0,
        "filled": 123.0,
        "remaining": 0.0,
        "cost": 15.129,
        "leverage": 5.0,
    }


def leverage_order_sell():
    return {
        "id": "12368",
        "symbol": "DOGE/BTC",
        "status": "closed",
        "side": "sell",
        "type": "limit",
        "price": 0.128,
        "amount": 123.0,
        "filled": 123.0,
        "remaining": 0.0,
        "cost": 15.744,
        "leverage": 5.0,
    }


# REMOVED_UNUSED_CODE: def leverage_trade(fee):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     5 hour short limit trade on kraken
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Short trade
# REMOVED_UNUSED_CODE:     fee: 0.25% base
# REMOVED_UNUSED_CODE:     interest_rate: 0.05% per day
# REMOVED_UNUSED_CODE:     open_rate: 0.123 base
# REMOVED_UNUSED_CODE:     close_rate: 0.128 base
# REMOVED_UNUSED_CODE:     amount: 615 crypto
# REMOVED_UNUSED_CODE:     stake_amount: 15.129 base
# REMOVED_UNUSED_CODE:     borrowed: 60.516  base
# REMOVED_UNUSED_CODE:     leverage: 5
# REMOVED_UNUSED_CODE:     hours: 5
# REMOVED_UNUSED_CODE:     interest: borrowed * interest_rate * ceil(1 + hours/4)
# REMOVED_UNUSED_CODE:                 = 60.516 * 0.0005 * ceil(1 + 5/4) = 0.090774 base
# REMOVED_UNUSED_CODE:     open_value: (amount * open_rate) + (amount * open_rate * fee)
# REMOVED_UNUSED_CODE:         = (615.0 * 0.123) + (615.0 * 0.123 * 0.0025)
# REMOVED_UNUSED_CODE:         = 75.83411249999999
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     close_value: (amount_closed * close_rate) - (amount_closed * close_rate * fee) - interest
# REMOVED_UNUSED_CODE:         = (615.0 * 0.128) - (615.0 * 0.128 * 0.0025) - 0.090774
# REMOVED_UNUSED_CODE:         = 78.432426
# REMOVED_UNUSED_CODE:     total_profit = close_value - open_value
# REMOVED_UNUSED_CODE:         = 78.432426 - 75.83411249999999
# REMOVED_UNUSED_CODE:         = 2.5983135000000175
# REMOVED_UNUSED_CODE:     total_profit_percentage = ((close_value/open_value)-1) * leverage
# REMOVED_UNUSED_CODE:         = ((78.432426/75.83411249999999)-1) * 5
# REMOVED_UNUSED_CODE:         = 0.1713156134055116
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     trade = Trade(
# REMOVED_UNUSED_CODE:         pair="DOGE/BTC",
# REMOVED_UNUSED_CODE:         stake_amount=15.129,
# REMOVED_UNUSED_CODE:         amount=615.0,
# REMOVED_UNUSED_CODE:         leverage=5.0,
# REMOVED_UNUSED_CODE:         amount_requested=615.0,
# REMOVED_UNUSED_CODE:         fee_open=fee.return_value,
# REMOVED_UNUSED_CODE:         fee_close=fee.return_value,
# REMOVED_UNUSED_CODE:         open_rate=0.123,
# REMOVED_UNUSED_CODE:         close_rate=0.128,
# REMOVED_UNUSED_CODE:         close_profit=0.1713156134055116,
# REMOVED_UNUSED_CODE:         close_profit_abs=2.5983135000000175,
# REMOVED_UNUSED_CODE:         exchange="kraken",
# REMOVED_UNUSED_CODE:         is_open=False,
# REMOVED_UNUSED_CODE:         strategy="DefaultStrategy",
# REMOVED_UNUSED_CODE:         timeframe=5,
# REMOVED_UNUSED_CODE:         exit_reason="sell_signal",
# REMOVED_UNUSED_CODE:         open_date=datetime.now(tz=timezone.utc) - timedelta(minutes=300),
# REMOVED_UNUSED_CODE:         close_date=datetime.now(tz=timezone.utc),
# REMOVED_UNUSED_CODE:         interest_rate=0.0005,
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(leverage_order(), "DOGE/BTC", "sell")
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     o = Order.parse_from_ccxt_object(leverage_order_sell(), "DOGE/BTC", "sell")
# REMOVED_UNUSED_CODE:     trade.orders.append(o)
# REMOVED_UNUSED_CODE:     return trade
