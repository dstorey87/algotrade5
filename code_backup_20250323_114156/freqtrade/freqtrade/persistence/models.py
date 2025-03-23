"""
This module contains the class to persist trades into SQLite
"""

import logging
import threading
from contextvars import ContextVar
# REMOVED_UNUSED_CODE: from typing import Any, Final

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from sqlalchemy import create_engine, inspect
# REMOVED_UNUSED_CODE: from sqlalchemy.exc import NoSuchModuleError
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from sqlalchemy.orm import scoped_session, sessionmaker
# REMOVED_UNUSED_CODE: from sqlalchemy.pool import StaticPool

# REMOVED_UNUSED_CODE: from freqtrade.exceptions import OperationalException
# REMOVED_UNUSED_CODE: from freqtrade.persistence.base import ModelBase
# REMOVED_UNUSED_CODE: from freqtrade.persistence.custom_data import _CustomData
# REMOVED_UNUSED_CODE: from freqtrade.persistence.key_value_store import _KeyValueStoreModel
# REMOVED_UNUSED_CODE: from freqtrade.persistence.migrations import check_migrate
# REMOVED_UNUSED_CODE: from freqtrade.persistence.pairlock import PairLock
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from freqtrade.persistence.trade_model import Order, Trade


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[str | None] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


# REMOVED_UNUSED_CODE: def get_request_or_thread_id() -> str | None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Helper method to get either async context (for fastapi requests), or thread id
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     request_id = _request_id_ctx_var.get()
# REMOVED_UNUSED_CODE:     if request_id is None:
# REMOVED_UNUSED_CODE:         # when not in request context - use thread id
# REMOVED_UNUSED_CODE:         request_id = str(threading.current_thread().ident)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return request_id


_SQL_DOCS_URL = "http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls"


# REMOVED_UNUSED_CODE: def init_db(db_url: str) -> None:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Initializes this module with the given config,
# REMOVED_UNUSED_CODE:     registers all known command handlers
# REMOVED_UNUSED_CODE:     and starts polling for message updates
# REMOVED_UNUSED_CODE:     :param db_url: Database to use
# REMOVED_UNUSED_CODE:     :return: None
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     kwargs: dict[str, Any] = {}
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if db_url == "sqlite:///":
# REMOVED_UNUSED_CODE:         raise OperationalException(
# REMOVED_UNUSED_CODE:             f"Bad db-url {db_url}. For in-memory database, please use `sqlite://`."
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     if db_url == "sqlite://":
# REMOVED_UNUSED_CODE:         kwargs.update(
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "poolclass": StaticPool,
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:     # Take care of thread ownership
# REMOVED_UNUSED_CODE:     if db_url.startswith("sqlite://"):
# REMOVED_UNUSED_CODE:         kwargs.update(
# REMOVED_UNUSED_CODE:             {
# REMOVED_UNUSED_CODE:                 "connect_args": {"check_same_thread": False},
# REMOVED_UNUSED_CODE:             }
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         engine = create_engine(db_url, future=True, **kwargs)
# REMOVED_UNUSED_CODE:     except NoSuchModuleError:
# REMOVED_UNUSED_CODE:         raise OperationalException(
# REMOVED_UNUSED_CODE:             f"Given value for db_url: '{db_url}' is no valid database URL! (See {_SQL_DOCS_URL})"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     # https://docs.sqlalchemy.org/en/13/orm/contextual.html#thread-local-scope
# REMOVED_UNUSED_CODE:     # Scoped sessions proxy requests to the appropriate thread-local session.
# REMOVED_UNUSED_CODE:     # Since we also use fastAPI, we need to make it aware of the request id, too
# REMOVED_UNUSED_CODE:     Trade.session = scoped_session(
# REMOVED_UNUSED_CODE:         sessionmaker(bind=engine, autoflush=False), scopefunc=get_request_or_thread_id
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE:     Order.session = Trade.session
# REMOVED_UNUSED_CODE:     PairLock.session = Trade.session
# REMOVED_UNUSED_CODE:     _KeyValueStoreModel.session = Trade.session
# REMOVED_UNUSED_CODE:     _CustomData.session = scoped_session(
# REMOVED_UNUSED_CODE:         sessionmaker(bind=engine, autoflush=True), scopefunc=get_request_or_thread_id
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     previous_tables = inspect(engine).get_table_names()
# REMOVED_UNUSED_CODE:     ModelBase.metadata.create_all(engine)
# REMOVED_UNUSED_CODE:     check_migrate(engine, decl_base=ModelBase, previous_tables=previous_tables)
