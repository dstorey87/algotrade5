from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from freqtrade.enums import MarginMode, TradingMode
from tests.conftest import EXMS, get_patched_exchange


@pytest.mark.usefixtures("init_persistence")
def test_fetch_stoploss_order_gate(default_conf, mocker):
    exchange = get_patched_exchange(mocker, default_conf, exchange="gate")

    fetch_order_mock = MagicMock()
    exchange.fetch_order = fetch_order_mock

    exchange.fetch_stoploss_order("1234", "ETH/BTC")
    assert fetch_order_mock.call_count == 1
    assert fetch_order_mock.call_args_list[0][1]["order_id"] == "1234"
    assert fetch_order_mock.call_args_list[0][1]["pair"] == "ETH/BTC"
    assert fetch_order_mock.call_args_list[0][1]["params"] == {"stop": True}

    default_conf["trading_mode"] = "futures"
    default_conf["margin_mode"] = "isolated"

    exchange = get_patched_exchange(mocker, default_conf, exchange="gate")

    exchange.fetch_order = MagicMock(
        return_value={
            "status": "closed",
            "id": "1234",
            "stopPrice": 5.62,
            "info": {"trade_id": "222555"},
        }
    )

    exchange.fetch_stoploss_order("1234", "ETH/BTC")
    assert exchange.fetch_order.call_count == 2
    assert exchange.fetch_order.call_args_list[0][1]["order_id"] == "1234"
    assert exchange.fetch_order.call_args_list[1][1]["order_id"] == "222555"


def test_cancel_stoploss_order_gate(default_conf, mocker):
    exchange = get_patched_exchange(mocker, default_conf, exchange="gate")

    cancel_order_mock = MagicMock()
# REMOVED_UNUSED_CODE:     exchange.cancel_order = cancel_order_mock

    exchange.cancel_stoploss_order("1234", "ETH/BTC")
    assert cancel_order_mock.call_count == 1
    assert cancel_order_mock.call_args_list[0][1]["order_id"] == "1234"
    assert cancel_order_mock.call_args_list[0][1]["pair"] == "ETH/BTC"
    assert cancel_order_mock.call_args_list[0][1]["params"] == {"stop": True}


@pytest.mark.parametrize(
    "sl1,sl2,sl3,side", [(1501, 1499, 1501, "sell"), (1499, 1501, 1499, "buy")]
)
# REMOVED_UNUSED_CODE: def test_stoploss_adjust_gate(mocker, default_conf, sl1, sl2, sl3, side):
# REMOVED_UNUSED_CODE:     exchange = get_patched_exchange(mocker, default_conf, exchange="gate")
# REMOVED_UNUSED_CODE:     order = {
# REMOVED_UNUSED_CODE:         "price": 1500,
# REMOVED_UNUSED_CODE:         "stopPrice": 1500,
# REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     assert exchange.stoploss_adjust(sl1, order, side)
# REMOVED_UNUSED_CODE:     assert not exchange.stoploss_adjust(sl2, order, side)


@pytest.mark.parametrize(
    "takerormaker,rate,cost",
    [
        ("taker", 0.0005, 0.0001554325),
        ("maker", 0.0, 0.0),
    ],
)
# REMOVED_UNUSED_CODE: def test_fetch_my_trades_gate(mocker, default_conf, takerormaker, rate, cost):
# REMOVED_UNUSED_CODE:     mocker.patch(f"{EXMS}.exchange_has", return_value=True)
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     tick = {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         "ETH/USDT:USDT": {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "info": {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "user_id": "",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "taker_fee": "0.0018",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "maker_fee": "0.0018",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "gt_discount": False,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "gt_taker_fee": "0",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "gt_maker_fee": "0",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "loan_fee": "0.18",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "point_type": "1",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "futures_taker_fee": "0.0005",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "futures_maker_fee": "0",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             },
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "symbol": "ETH/USDT:USDT",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "maker": 0.0,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             "taker": 0.0005,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     }
# REMOVED_UNUSED_CODE:     default_conf["dry_run"] = False
# REMOVED_UNUSED_CODE:     default_conf["trading_mode"] = TradingMode.FUTURES
# REMOVED_UNUSED_CODE:     default_conf["margin_mode"] = MarginMode.ISOLATED
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     api_mock = MagicMock()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     api_mock.fetch_my_trades = MagicMock(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return_value=[
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "fee": {"cost": None},
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "price": 3108.65,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "cost": 0.310865,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "order": "22255",
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "takerOrMaker": takerormaker,
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:                 "amount": 1,  # 1 contract
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         ]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     exchange = get_patched_exchange(mocker, default_conf, api_mock=api_mock, exchange="gate")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     exchange._trading_fees = tick
# REMOVED_UNUSED_CODE:     trades = exchange.get_trades_for_order("22255", "ETH/USDT:USDT", datetime.now(timezone.utc))
# REMOVED_UNUSED_CODE:     trade = trades[0]
# REMOVED_UNUSED_CODE:     assert trade["fee"]
# REMOVED_UNUSED_CODE:     assert trade["fee"]["rate"] == rate
# REMOVED_UNUSED_CODE:     assert trade["fee"]["currency"] == "USDT"
# REMOVED_UNUSED_CODE:     assert trade["fee"]["cost"] == cost
