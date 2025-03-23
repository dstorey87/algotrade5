# REMOVED_UNUSED_CODE: from collections.abc import Callable
# REMOVED_UNUSED_CODE: from typing import Any

# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from rich.console import ConsoleRenderable, Group, RichCast
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: from rich.progress import Progress, Task, TaskID


# REMOVED_UNUSED_CODE: class CustomProgress(Progress):
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         *args,
# REMOVED_UNUSED_CODE:         cust_objs: list[ConsoleRenderable] | None = None,
# REMOVED_UNUSED_CODE:         cust_callables: list[Callable[[], ConsoleRenderable]] | None = None,
# REMOVED_UNUSED_CODE:         ft_callback: Callable[[Task], None] | None = None,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         self._cust_objs = cust_objs or []
# REMOVED_UNUSED_CODE:         self._cust_callables = cust_callables or []
# REMOVED_UNUSED_CODE:         self._ft_callback = ft_callback
# REMOVED_UNUSED_CODE:         if self._ft_callback:
# REMOVED_UNUSED_CODE:             kwargs["disable"] = True
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         super().__init__(*args, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def update(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         task_id: TaskID,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         total: float | None = None,
# REMOVED_UNUSED_CODE:         completed: float | None = None,
# REMOVED_UNUSED_CODE:         advance: float | None = None,
# REMOVED_UNUSED_CODE:         description: str | None = None,
# REMOVED_UNUSED_CODE:         visible: bool | None = None,
# REMOVED_UNUSED_CODE:         refresh: bool = False,
# REMOVED_UNUSED_CODE:         **fields: Any,
# REMOVED_UNUSED_CODE:     ) -> None:
# REMOVED_UNUSED_CODE:         t = super().update(
# REMOVED_UNUSED_CODE:             task_id,
# REMOVED_UNUSED_CODE:             total=total,
# REMOVED_UNUSED_CODE:             completed=completed,
# REMOVED_UNUSED_CODE:             advance=advance,
# REMOVED_UNUSED_CODE:             description=description,
# REMOVED_UNUSED_CODE:             visible=visible,
# REMOVED_UNUSED_CODE:             refresh=refresh,
# REMOVED_UNUSED_CODE:             **fields,
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE:         if self._ft_callback:
# REMOVED_UNUSED_CODE:             self._ft_callback(
# REMOVED_UNUSED_CODE:                 self.tasks[task_id],
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         return t
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_renderable(self) -> ConsoleRenderable | RichCast | str:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         objs = [obj for obj in self._cust_objs]
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         for cust_call in self._cust_callables:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             objs.append(cust_call())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         renderable = Group(*objs, *self.get_renderables())
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return renderable
