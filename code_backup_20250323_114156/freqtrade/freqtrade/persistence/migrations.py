import logging

# REMOVED_UNUSED_CODE: from sqlalchemy import inspect, select, text, update

# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.persistence.trade_model import Order, Trade


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


# REMOVED_UNUSED_CODE: def get_table_names_for_table(inspector, tabletype) -> list[str]:
# REMOVED_UNUSED_CODE:     return [t for t in inspector.get_table_names() if t.startswith(tabletype)]


def has_column(columns: list, searchname: str) -> bool:
    return len(list(filter(lambda x: x["name"] == searchname, columns))) == 1


def get_column_def(columns: list, column: str, default: str) -> str:
    return default if not has_column(columns, column) else column


# REMOVED_UNUSED_CODE: def get_backup_name(tabs: list[str], backup_prefix: str):
# REMOVED_UNUSED_CODE:     table_back_name = backup_prefix
# REMOVED_UNUSED_CODE:     for i, table_back_name in enumerate(tabs):
# REMOVED_UNUSED_CODE:         table_back_name = f"{backup_prefix}{i}"
# REMOVED_UNUSED_CODE:         logger.debug(f"trying {table_back_name}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return table_back_name


# REMOVED_UNUSED_CODE: def get_last_sequence_ids(engine, trade_back_name: str, order_back_name: str):
# REMOVED_UNUSED_CODE:     order_id: int | None = None
# REMOVED_UNUSED_CODE:     trade_id: int | None = None
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if engine.name == "postgresql":
# REMOVED_UNUSED_CODE:         with engine.begin() as connection:
# REMOVED_UNUSED_CODE:             trade_id = connection.execute(text("select nextval('trades_id_seq')")).fetchone()[0]
# REMOVED_UNUSED_CODE:             order_id = connection.execute(text("select nextval('orders_id_seq')")).fetchone()[0]
# REMOVED_UNUSED_CODE:         with engine.begin() as connection:
# REMOVED_UNUSED_CODE:             connection.execute(
# REMOVED_UNUSED_CODE:                 text(f"ALTER SEQUENCE orders_id_seq rename to {order_back_name}_id_seq_bak")
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             connection.execute(
# REMOVED_UNUSED_CODE:                 text(f"ALTER SEQUENCE trades_id_seq rename to {trade_back_name}_id_seq_bak")
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:     return order_id, trade_id


# REMOVED_UNUSED_CODE: def set_sequence_ids(engine, order_id, trade_id, pairlock_id=None):
# REMOVED_UNUSED_CODE:     if engine.name == "postgresql":
# REMOVED_UNUSED_CODE:         with engine.begin() as connection:
# REMOVED_UNUSED_CODE:             if order_id:
# REMOVED_UNUSED_CODE:                 connection.execute(text(f"ALTER SEQUENCE orders_id_seq RESTART WITH {order_id}"))
# REMOVED_UNUSED_CODE:             if trade_id:
# REMOVED_UNUSED_CODE:                 connection.execute(text(f"ALTER SEQUENCE trades_id_seq RESTART WITH {trade_id}"))
# REMOVED_UNUSED_CODE:             if pairlock_id:
# REMOVED_UNUSED_CODE:                 connection.execute(
# REMOVED_UNUSED_CODE:                     text(f"ALTER SEQUENCE pairlocks_id_seq RESTART WITH {pairlock_id}")
# REMOVED_UNUSED_CODE:                 )


# REMOVED_UNUSED_CODE: def drop_index_on_table(engine, inspector, table_bak_name):
# REMOVED_UNUSED_CODE:     with engine.begin() as connection:
# REMOVED_UNUSED_CODE:         # drop indexes on backup table in new session
# REMOVED_UNUSED_CODE:         for index in inspector.get_indexes(table_bak_name):
# REMOVED_UNUSED_CODE:             if engine.name == "mysql":
# REMOVED_UNUSED_CODE:                 connection.execute(text(f"drop index {index['name']} on {table_bak_name}"))
# REMOVED_UNUSED_CODE:             else:
# REMOVED_UNUSED_CODE:                 connection.execute(text(f"drop index {index['name']}"))


# REMOVED_UNUSED_CODE: def migrate_trades_and_orders_table(
# REMOVED_UNUSED_CODE:     decl_base,
# REMOVED_UNUSED_CODE:     inspector,
# REMOVED_UNUSED_CODE:     engine,
# REMOVED_UNUSED_CODE:     trade_back_name: str,
# REMOVED_UNUSED_CODE:     cols: list,
# REMOVED_UNUSED_CODE:     order_back_name: str,
# REMOVED_UNUSED_CODE:     cols_order: list,
# REMOVED_UNUSED_CODE: ):
# REMOVED_UNUSED_CODE:     base_currency = get_column_def(cols, "base_currency", "null")
# REMOVED_UNUSED_CODE:     stake_currency = get_column_def(cols, "stake_currency", "null")
# REMOVED_UNUSED_CODE:     fee_open = get_column_def(cols, "fee_open", "fee")
# REMOVED_UNUSED_CODE:     fee_open_cost = get_column_def(cols, "fee_open_cost", "null")
# REMOVED_UNUSED_CODE:     fee_open_currency = get_column_def(cols, "fee_open_currency", "null")
# REMOVED_UNUSED_CODE:     fee_close = get_column_def(cols, "fee_close", "fee")
# REMOVED_UNUSED_CODE:     fee_close_cost = get_column_def(cols, "fee_close_cost", "null")
# REMOVED_UNUSED_CODE:     fee_close_currency = get_column_def(cols, "fee_close_currency", "null")
# REMOVED_UNUSED_CODE:     open_rate_requested = get_column_def(cols, "open_rate_requested", "null")
# REMOVED_UNUSED_CODE:     close_rate_requested = get_column_def(cols, "close_rate_requested", "null")
# REMOVED_UNUSED_CODE:     stop_loss = get_column_def(cols, "stop_loss", "0.0")
# REMOVED_UNUSED_CODE:     stop_loss_pct = get_column_def(cols, "stop_loss_pct", "null")
# REMOVED_UNUSED_CODE:     initial_stop_loss = get_column_def(cols, "initial_stop_loss", "0.0")
# REMOVED_UNUSED_CODE:     initial_stop_loss_pct = get_column_def(cols, "initial_stop_loss_pct", "null")
# REMOVED_UNUSED_CODE:     is_stop_loss_trailing = get_column_def(
# REMOVED_UNUSED_CODE:         cols,
# REMOVED_UNUSED_CODE:         "is_stop_loss_trailing",
# REMOVED_UNUSED_CODE:         f"coalesce({stop_loss_pct}, 0.0) <> coalesce({initial_stop_loss_pct}, 0.0)",
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     max_rate = get_column_def(cols, "max_rate", "0.0")
# REMOVED_UNUSED_CODE:     min_rate = get_column_def(cols, "min_rate", "null")
# REMOVED_UNUSED_CODE:     exit_reason = get_column_def(cols, "sell_reason", get_column_def(cols, "exit_reason", "null"))
# REMOVED_UNUSED_CODE:     strategy = get_column_def(cols, "strategy", "null")
# REMOVED_UNUSED_CODE:     enter_tag = get_column_def(cols, "buy_tag", get_column_def(cols, "enter_tag", "null"))
# REMOVED_UNUSED_CODE:     realized_profit = get_column_def(cols, "realized_profit", "0.0")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     trading_mode = get_column_def(cols, "trading_mode", "null")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Leverage Properties
# REMOVED_UNUSED_CODE:     leverage = get_column_def(cols, "leverage", "1.0")
# REMOVED_UNUSED_CODE:     liquidation_price = get_column_def(
# REMOVED_UNUSED_CODE:         cols, "liquidation_price", get_column_def(cols, "isolated_liq", "null")
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     # sqlite does not support literals for booleans
# REMOVED_UNUSED_CODE:     if engine.name == "postgresql":
# REMOVED_UNUSED_CODE:         is_short = get_column_def(cols, "is_short", "false")
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         is_short = get_column_def(cols, "is_short", "0")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Futures Properties
# REMOVED_UNUSED_CODE:     interest_rate = get_column_def(cols, "interest_rate", "0.0")
# REMOVED_UNUSED_CODE:     funding_fees = get_column_def(cols, "funding_fees", "0.0")
# REMOVED_UNUSED_CODE:     funding_fee_running = get_column_def(cols, "funding_fee_running", "null")
# REMOVED_UNUSED_CODE:     max_stake_amount = get_column_def(cols, "max_stake_amount", "stake_amount")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # If ticker-interval existed use that, else null.
# REMOVED_UNUSED_CODE:     if has_column(cols, "ticker_interval"):
# REMOVED_UNUSED_CODE:         timeframe = get_column_def(cols, "timeframe", "ticker_interval")
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         timeframe = get_column_def(cols, "timeframe", "null")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     open_trade_value = get_column_def(
# REMOVED_UNUSED_CODE:         cols, "open_trade_value", f"amount * open_rate * (1 + {fee_open})"
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     close_profit_abs = get_column_def(
# REMOVED_UNUSED_CODE:         cols, "close_profit_abs", f"(amount * close_rate * (1 - {fee_close})) - {open_trade_value}"
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     exit_order_status = get_column_def(
# REMOVED_UNUSED_CODE:         cols, "exit_order_status", get_column_def(cols, "sell_order_status", "null")
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     amount_requested = get_column_def(cols, "amount_requested", "amount")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     amount_precision = get_column_def(cols, "amount_precision", "null")
# REMOVED_UNUSED_CODE:     price_precision = get_column_def(cols, "price_precision", "null")
# REMOVED_UNUSED_CODE:     precision_mode = get_column_def(cols, "precision_mode", "null")
# REMOVED_UNUSED_CODE:     contract_size = get_column_def(cols, "contract_size", "null")
# REMOVED_UNUSED_CODE:     precision_mode_price = get_column_def(
# REMOVED_UNUSED_CODE:         cols, "precision_mode_price", get_column_def(cols, "precision_mode", "null")
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Schema migration necessary
# REMOVED_UNUSED_CODE:     with engine.begin() as connection:
# REMOVED_UNUSED_CODE:         connection.execute(text(f"alter table trades rename to {trade_back_name}"))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     drop_index_on_table(engine, inspector, trade_back_name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     order_id, trade_id = get_last_sequence_ids(engine, trade_back_name, order_back_name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     drop_orders_table(engine, order_back_name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # let SQLAlchemy create the schema as required
# REMOVED_UNUSED_CODE:     decl_base.metadata.create_all(engine)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Copy data back - following the correct schema
# REMOVED_UNUSED_CODE:     with engine.begin() as connection:
# REMOVED_UNUSED_CODE:         connection.execute(
# REMOVED_UNUSED_CODE:             text(
# REMOVED_UNUSED_CODE:                 f"""insert into trades
# REMOVED_UNUSED_CODE:             (id, exchange, pair, base_currency, stake_currency, is_open,
# REMOVED_UNUSED_CODE:             fee_open, fee_open_cost, fee_open_currency,
# REMOVED_UNUSED_CODE:             fee_close, fee_close_cost, fee_close_currency, open_rate,
# REMOVED_UNUSED_CODE:             open_rate_requested, close_rate, close_rate_requested, close_profit,
# REMOVED_UNUSED_CODE:             stake_amount, amount, amount_requested, open_date, close_date,
# REMOVED_UNUSED_CODE:             stop_loss, stop_loss_pct, initial_stop_loss, initial_stop_loss_pct,
# REMOVED_UNUSED_CODE:             is_stop_loss_trailing,
# REMOVED_UNUSED_CODE:             max_rate, min_rate, exit_reason, exit_order_status, strategy, enter_tag,
# REMOVED_UNUSED_CODE:             timeframe, open_trade_value, close_profit_abs,
# REMOVED_UNUSED_CODE:             trading_mode, leverage, liquidation_price, is_short,
# REMOVED_UNUSED_CODE:             interest_rate, funding_fees, funding_fee_running, realized_profit,
# REMOVED_UNUSED_CODE:             amount_precision, price_precision, precision_mode, precision_mode_price, contract_size,
# REMOVED_UNUSED_CODE:             max_stake_amount
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         select id, lower(exchange), pair, {base_currency} base_currency,
# REMOVED_UNUSED_CODE:             {stake_currency} stake_currency,
# REMOVED_UNUSED_CODE:             is_open, {fee_open} fee_open, {fee_open_cost} fee_open_cost,
# REMOVED_UNUSED_CODE:             {fee_open_currency} fee_open_currency, {fee_close} fee_close,
# REMOVED_UNUSED_CODE:             {fee_close_cost} fee_close_cost, {fee_close_currency} fee_close_currency,
# REMOVED_UNUSED_CODE:             open_rate, {open_rate_requested} open_rate_requested, close_rate,
# REMOVED_UNUSED_CODE:             {close_rate_requested} close_rate_requested, close_profit,
# REMOVED_UNUSED_CODE:             stake_amount, amount, {amount_requested}, open_date, close_date,
# REMOVED_UNUSED_CODE:             {stop_loss} stop_loss, {stop_loss_pct} stop_loss_pct,
# REMOVED_UNUSED_CODE:             {initial_stop_loss} initial_stop_loss,
# REMOVED_UNUSED_CODE:             {initial_stop_loss_pct} initial_stop_loss_pct,
# REMOVED_UNUSED_CODE:             {is_stop_loss_trailing} is_stop_loss_trailing,
# REMOVED_UNUSED_CODE:             {max_rate} max_rate, {min_rate} min_rate,
# REMOVED_UNUSED_CODE:             case when {exit_reason} = 'sell_signal' then 'exit_signal'
# REMOVED_UNUSED_CODE:                  when {exit_reason} = 'custom_sell' then 'custom_exit'
# REMOVED_UNUSED_CODE:                  when {exit_reason} = 'force_sell' then 'force_exit'
# REMOVED_UNUSED_CODE:                  when {exit_reason} = 'emergency_sell' then 'emergency_exit'
# REMOVED_UNUSED_CODE:                  else {exit_reason}
# REMOVED_UNUSED_CODE:             end exit_reason,
# REMOVED_UNUSED_CODE:             {exit_order_status} exit_order_status,
# REMOVED_UNUSED_CODE:             {strategy} strategy, {enter_tag} enter_tag, {timeframe} timeframe,
# REMOVED_UNUSED_CODE:             {open_trade_value} open_trade_value, {close_profit_abs} close_profit_abs,
# REMOVED_UNUSED_CODE:             {trading_mode} trading_mode, {leverage} leverage, {liquidation_price} liquidation_price,
# REMOVED_UNUSED_CODE:             {is_short} is_short, {interest_rate} interest_rate,
# REMOVED_UNUSED_CODE:             {funding_fees} funding_fees, {funding_fee_running} funding_fee_running,
# REMOVED_UNUSED_CODE:             {realized_profit} realized_profit,
# REMOVED_UNUSED_CODE:             {amount_precision} amount_precision, {price_precision} price_precision,
# REMOVED_UNUSED_CODE:             {precision_mode} precision_mode, {precision_mode_price} precision_mode_price,
# REMOVED_UNUSED_CODE:             {contract_size} contract_size, {max_stake_amount} max_stake_amount
# REMOVED_UNUSED_CODE:             from {trade_back_name}
# REMOVED_UNUSED_CODE:             """
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     migrate_orders_table(engine, order_back_name, cols_order)
# REMOVED_UNUSED_CODE:     set_sequence_ids(engine, order_id, trade_id)


# REMOVED_UNUSED_CODE: def drop_orders_table(engine, table_back_name: str):
# REMOVED_UNUSED_CODE:     # Drop and recreate orders table as backup
# REMOVED_UNUSED_CODE:     # This drops foreign keys, too.
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     with engine.begin() as connection:
# REMOVED_UNUSED_CODE:         connection.execute(text(f"create table {table_back_name} as select * from orders"))
# REMOVED_UNUSED_CODE:         connection.execute(text("drop table orders"))


# REMOVED_UNUSED_CODE: def migrate_orders_table(engine, table_back_name: str, cols_order: list):
# REMOVED_UNUSED_CODE:     ft_fee_base = get_column_def(cols_order, "ft_fee_base", "null")
# REMOVED_UNUSED_CODE:     average = get_column_def(cols_order, "average", "null")
# REMOVED_UNUSED_CODE:     stop_price = get_column_def(cols_order, "stop_price", "null")
# REMOVED_UNUSED_CODE:     funding_fee = get_column_def(cols_order, "funding_fee", "0.0")
# REMOVED_UNUSED_CODE:     ft_amount = get_column_def(cols_order, "ft_amount", "coalesce(amount, 0.0)")
# REMOVED_UNUSED_CODE:     ft_price = get_column_def(cols_order, "ft_price", "coalesce(price, 0.0)")
# REMOVED_UNUSED_CODE:     ft_cancel_reason = get_column_def(cols_order, "ft_cancel_reason", "null")
# REMOVED_UNUSED_CODE:     ft_order_tag = get_column_def(cols_order, "ft_order_tag", "null")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # sqlite does not support literals for booleans
# REMOVED_UNUSED_CODE:     with engine.begin() as connection:
# REMOVED_UNUSED_CODE:         connection.execute(
# REMOVED_UNUSED_CODE:             text(
# REMOVED_UNUSED_CODE:                 f"""
# REMOVED_UNUSED_CODE:             insert into orders (id, ft_trade_id, ft_order_side, ft_pair, ft_is_open, order_id,
# REMOVED_UNUSED_CODE:             status, symbol, order_type, side, price, amount, filled, average, remaining, cost,
# REMOVED_UNUSED_CODE:             stop_price, order_date, order_filled_date, order_update_date, ft_fee_base, funding_fee,
# REMOVED_UNUSED_CODE:             ft_amount, ft_price, ft_cancel_reason, ft_order_tag
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             select id, ft_trade_id, ft_order_side, ft_pair, ft_is_open, order_id,
# REMOVED_UNUSED_CODE:             status, symbol, order_type, side, price, amount, filled, {average} average, remaining,
# REMOVED_UNUSED_CODE:             cost, {stop_price} stop_price, order_date, order_filled_date,
# REMOVED_UNUSED_CODE:             order_update_date, {ft_fee_base} ft_fee_base, {funding_fee} funding_fee,
# REMOVED_UNUSED_CODE:             {ft_amount} ft_amount, {ft_price} ft_price, {ft_cancel_reason} ft_cancel_reason,
# REMOVED_UNUSED_CODE:             {ft_order_tag} ft_order_tag
# REMOVED_UNUSED_CODE:             from {table_back_name}
# REMOVED_UNUSED_CODE:             """
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: def migrate_pairlocks_table(decl_base, inspector, engine, pairlock_back_name: str, cols: list):
# REMOVED_UNUSED_CODE:     # Schema migration necessary
# REMOVED_UNUSED_CODE:     with engine.begin() as connection:
# REMOVED_UNUSED_CODE:         connection.execute(text(f"alter table pairlocks rename to {pairlock_back_name}"))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     drop_index_on_table(engine, inspector, pairlock_back_name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     side = get_column_def(cols, "side", "'*'")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # let SQLAlchemy create the schema as required
# REMOVED_UNUSED_CODE:     decl_base.metadata.create_all(engine)
# REMOVED_UNUSED_CODE:     # Copy data back - following the correct schema
# REMOVED_UNUSED_CODE:     with engine.begin() as connection:
# REMOVED_UNUSED_CODE:         connection.execute(
# REMOVED_UNUSED_CODE:             text(
# REMOVED_UNUSED_CODE:                 f"""insert into pairlocks
# REMOVED_UNUSED_CODE:         (id, pair, side, reason, lock_time,
# REMOVED_UNUSED_CODE:          lock_end_time, active)
# REMOVED_UNUSED_CODE:         select id, pair, {side} side, reason, lock_time,
# REMOVED_UNUSED_CODE:          lock_end_time, active
# REMOVED_UNUSED_CODE:         from {pairlock_back_name}
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         )


# REMOVED_UNUSED_CODE: def set_sqlite_to_wal(engine):
# REMOVED_UNUSED_CODE:     if engine.name == "sqlite" and str(engine.url) != "sqlite://":
# REMOVED_UNUSED_CODE:         # Set Mode to
# REMOVED_UNUSED_CODE:         with engine.begin() as connection:
# REMOVED_UNUSED_CODE:             connection.execute(text("PRAGMA journal_mode=wal"))


# REMOVED_UNUSED_CODE: def fix_old_dry_orders(engine):
# REMOVED_UNUSED_CODE:     with engine.begin() as connection:
# REMOVED_UNUSED_CODE:         # Update current dry-run Orders where
# REMOVED_UNUSED_CODE:         # - stoploss order is Open (will be replaced eventually)
# REMOVED_UNUSED_CODE:         # 2nd query:
# REMOVED_UNUSED_CODE:         # - current Order is open
# REMOVED_UNUSED_CODE:         # - current Trade is closed
# REMOVED_UNUSED_CODE:         # - current Order trade_id not equal to current Trade.id
# REMOVED_UNUSED_CODE:         # - current Order not stoploss
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         stmt = (
# REMOVED_UNUSED_CODE:             update(Order)
# REMOVED_UNUSED_CODE:             .where(
# REMOVED_UNUSED_CODE:                 Order.ft_is_open.is_(True),
# REMOVED_UNUSED_CODE:                 Order.ft_order_side == "stoploss",
# REMOVED_UNUSED_CODE:                 Order.order_id.like("dry%"),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             .values(ft_is_open=False)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         connection.execute(stmt)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Close dry-run orders for closed trades.
# REMOVED_UNUSED_CODE:         stmt = (
# REMOVED_UNUSED_CODE:             update(Order)
# REMOVED_UNUSED_CODE:             .where(
# REMOVED_UNUSED_CODE:                 Order.ft_is_open.is_(True),
# REMOVED_UNUSED_CODE:                 Order.ft_trade_id.not_in(select(Trade.id).where(Trade.is_open.is_(True))),
# REMOVED_UNUSED_CODE:                 Order.ft_order_side != "stoploss",
# REMOVED_UNUSED_CODE:                 Order.order_id.like("dry%"),
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:             .values(ft_is_open=False)
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         connection.execute(stmt)


# REMOVED_UNUSED_CODE: def check_migrate(engine, decl_base, previous_tables) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Checks if migration is necessary and migrates if necessary
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     inspector = inspect(engine)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     cols_trades = inspector.get_columns("trades")
# REMOVED_UNUSED_CODE:     cols_orders = inspector.get_columns("orders")
# REMOVED_UNUSED_CODE:     cols_pairlocks = inspector.get_columns("pairlocks")
# REMOVED_UNUSED_CODE:     tabs = get_table_names_for_table(inspector, "trades")
# REMOVED_UNUSED_CODE:     table_back_name = get_backup_name(tabs, "trades_bak")
# REMOVED_UNUSED_CODE:     order_tabs = get_table_names_for_table(inspector, "orders")
# REMOVED_UNUSED_CODE:     order_table_bak_name = get_backup_name(order_tabs, "orders_bak")
# REMOVED_UNUSED_CODE:     pairlock_tabs = get_table_names_for_table(inspector, "pairlocks")
# REMOVED_UNUSED_CODE:     pairlock_table_bak_name = get_backup_name(pairlock_tabs, "pairlocks_bak")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # Check if migration necessary
# REMOVED_UNUSED_CODE:     # Migrates both trades and orders table!
# REMOVED_UNUSED_CODE:     # if ('orders' not in previous_tables
# REMOVED_UNUSED_CODE:     # or not has_column(cols_orders, 'funding_fee')):
# REMOVED_UNUSED_CODE:     migrating = False
# REMOVED_UNUSED_CODE:     if not has_column(cols_trades, "precision_mode_price"):
# REMOVED_UNUSED_CODE:         # if not has_column(cols_orders, "ft_order_tag"):
# REMOVED_UNUSED_CODE:         migrating = True
# REMOVED_UNUSED_CODE:         logger.info(
# REMOVED_UNUSED_CODE:             f"Running database migration for trades - "
# REMOVED_UNUSED_CODE:             f"backup: {table_back_name}, {order_table_bak_name}"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         migrate_trades_and_orders_table(
# REMOVED_UNUSED_CODE:             decl_base,
# REMOVED_UNUSED_CODE:             inspector,
# REMOVED_UNUSED_CODE:             engine,
# REMOVED_UNUSED_CODE:             table_back_name,
# REMOVED_UNUSED_CODE:             cols_trades,
# REMOVED_UNUSED_CODE:             order_table_bak_name,
# REMOVED_UNUSED_CODE:             cols_orders,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if not has_column(cols_pairlocks, "side"):
# REMOVED_UNUSED_CODE:         migrating = True
# REMOVED_UNUSED_CODE:         logger.info(f"Running database migration for pairlocks - backup: {pairlock_table_bak_name}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         migrate_pairlocks_table(
# REMOVED_UNUSED_CODE:             decl_base, inspector, engine, pairlock_table_bak_name, cols_pairlocks
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     if "orders" not in previous_tables and "trades" in previous_tables:
# REMOVED_UNUSED_CODE:         raise OperationalException(
# REMOVED_UNUSED_CODE:             "Your database seems to be very old. "
# REMOVED_UNUSED_CODE:             "Please update to freqtrade 2022.3 to migrate this database or "
# REMOVED_UNUSED_CODE:             "start with a fresh database."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     set_sqlite_to_wal(engine)
# REMOVED_UNUSED_CODE:     fix_old_dry_orders(engine)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if migrating:
# REMOVED_UNUSED_CODE:         logger.info("Database migration finished.")
