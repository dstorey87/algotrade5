import sys
from collections.abc import Sequence
from typing import Any, TypeAlias

from pandas import DataFrame
from rich.console import Console
from rich.table import Column, Table
from rich.text import Text


TextOrString: TypeAlias = str | Text


# REMOVED_UNUSED_CODE: def print_rich_table(
# REMOVED_UNUSED_CODE:     tabular_data: Sequence[dict[str, Any] | Sequence[TextOrString]],
# REMOVED_UNUSED_CODE:     headers: Sequence[str],
# REMOVED_UNUSED_CODE:     summary: str | None = None,
# REMOVED_UNUSED_CODE:     *,
# REMOVED_UNUSED_CODE:     justify="right",
# REMOVED_UNUSED_CODE:     table_kwargs: dict[str, Any] | None = None,
# REMOVED_UNUSED_CODE: ) -> None:
# REMOVED_UNUSED_CODE:     table = Table(
# REMOVED_UNUSED_CODE:         *[c if isinstance(c, Column) else Column(c, justify=justify) for c in headers],
# REMOVED_UNUSED_CODE:         title=summary,
# REMOVED_UNUSED_CODE:         **(table_kwargs or {}),
# REMOVED_UNUSED_CODE:     )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for row in tabular_data:
# REMOVED_UNUSED_CODE:         if isinstance(row, dict):
# REMOVED_UNUSED_CODE:             table.add_row(
# REMOVED_UNUSED_CODE:                 *[
# REMOVED_UNUSED_CODE:                     row[header] if isinstance(row[header], Text) else str(row[header])
# REMOVED_UNUSED_CODE:                     for header in headers
# REMOVED_UNUSED_CODE:                 ]
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             row_to_add: list[str | Text] = [r if isinstance(r, Text) else str(r) for r in row]
# REMOVED_UNUSED_CODE:             table.add_row(*row_to_add)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     width = None
# REMOVED_UNUSED_CODE:     if any(module in ["pytest", "ipykernel"] for module in sys.modules):
# REMOVED_UNUSED_CODE:         width = 200
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     console = Console(width=width)
# REMOVED_UNUSED_CODE:     console.print(table)


def _format_value(value: Any, *, floatfmt: str) -> str:
    if isinstance(value, float):
        return f"{value:{floatfmt}}"
    return str(value)


# REMOVED_UNUSED_CODE: def print_df_rich_table(
# REMOVED_UNUSED_CODE:     tabular_data: DataFrame,
# REMOVED_UNUSED_CODE:     headers: Sequence[str],
# REMOVED_UNUSED_CODE:     summary: str | None = None,
# REMOVED_UNUSED_CODE:     *,
# REMOVED_UNUSED_CODE:     show_index=False,
# REMOVED_UNUSED_CODE:     index_name: str | None = None,
# REMOVED_UNUSED_CODE:     table_kwargs: dict[str, Any] | None = None,
# REMOVED_UNUSED_CODE: ) -> None:
# REMOVED_UNUSED_CODE:     table = Table(title=summary, **(table_kwargs or {}))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if show_index:
# REMOVED_UNUSED_CODE:         index_name = str(index_name) if index_name else tabular_data.index.name
# REMOVED_UNUSED_CODE:         table.add_column(index_name)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for header in headers:
# REMOVED_UNUSED_CODE:         table.add_column(header, justify="right")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     for value_list in tabular_data.itertuples(index=show_index):
# REMOVED_UNUSED_CODE:         row = [_format_value(x, floatfmt=".3f") for x in value_list]
# REMOVED_UNUSED_CODE:         table.add_row(*row)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     width = None
# REMOVED_UNUSED_CODE:     if any(module in ["pytest", "ipykernel"] for module in sys.modules):
# REMOVED_UNUSED_CODE:         width = 200
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     console = Console(width=width)
# REMOVED_UNUSED_CODE:     console.print(table)
