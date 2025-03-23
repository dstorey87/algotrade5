# REMOVED_UNUSED_CODE: import asyncio
# REMOVED_UNUSED_CODE: import time


# REMOVED_UNUSED_CODE: class MessageStream:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     A message stream for consumers to subscribe to,
# REMOVED_UNUSED_CODE:     and for producers to publish to.
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(self):
# REMOVED_UNUSED_CODE:         self._loop = asyncio.get_running_loop()
# REMOVED_UNUSED_CODE:         self._waiter = self._loop.create_future()
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def publish(self, message):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Publish a message to this MessageStream
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param message: The message to publish
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         waiter, self._waiter = self._waiter, self._loop.create_future()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         waiter.set_result((message, time.time(), self._waiter))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     async def __aiter__(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Iterate over the messages in the message stream
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         waiter = self._waiter
# REMOVED_UNUSED_CODE:         while True:
# REMOVED_UNUSED_CODE:             # Shield the future from being cancelled by a task waiting on it
# REMOVED_UNUSED_CODE:             message, ts, waiter = await asyncio.shield(waiter)
# REMOVED_UNUSED_CODE:             yield message, ts
