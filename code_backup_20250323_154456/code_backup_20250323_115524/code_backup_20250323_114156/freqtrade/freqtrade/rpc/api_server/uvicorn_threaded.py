import threading
import time

import uvicorn


def asyncio_setup() -> None:  # pragma: no cover
    # Set eventloop for win32 setups
    # Reverts a change done in uvicorn 0.15.0 - which now sets the eventloop
    # via policy.
    # TODO: is this workaround actually needed?
    import sys

    if sys.version_info >= (3, 8) and sys.platform == "win32":
        import asyncio
        import selectors

        selector = selectors.SelectSelector()
        loop = asyncio.SelectorEventLoop(selector)
        asyncio.set_event_loop(loop)


# REMOVED_UNUSED_CODE: class UvicornServer(uvicorn.Server):
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Multithreaded server - as found in https://github.com/encode/uvicorn/issues/742
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Removed install_signal_handlers() override based on changes from this commit:
# REMOVED_UNUSED_CODE:         https://github.com/encode/uvicorn/commit/ce2ef45a9109df8eae038c0ec323eb63d644cbc6
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Cannot rely on asyncio.get_event_loop() to create new event loop because of this check:
# REMOVED_UNUSED_CODE:         https://github.com/python/cpython/blob/4d7f11e05731f67fd2c07ec2972c6cb9861d52be/Lib/asyncio/events.py#L638
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     Fix by overriding run() and forcing creation of new event loop if uvloop is available
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def run(self, sockets=None):
# REMOVED_UNUSED_CODE:         import asyncio
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Parent implementation calls self.config.setup_event_loop(),
# REMOVED_UNUSED_CODE:             but we need to create uvloop event loop manually
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             import uvloop  # noqa
# REMOVED_UNUSED_CODE:         except ImportError:  # pragma: no cover
# REMOVED_UNUSED_CODE:             asyncio_setup()
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             asyncio.set_event_loop(uvloop.new_event_loop())
# REMOVED_UNUSED_CODE:         try:
# REMOVED_UNUSED_CODE:             loop = asyncio.get_running_loop()
# REMOVED_UNUSED_CODE:         except RuntimeError:
# REMOVED_UNUSED_CODE:             # When running in a thread, we'll not have an eventloop yet.
# REMOVED_UNUSED_CODE:             loop = asyncio.new_event_loop()
# REMOVED_UNUSED_CODE:         loop.run_until_complete(self.serve(sockets=sockets))
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def run_in_thread(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.thread = threading.Thread(target=self.run, name="FTUvicorn")
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.thread.start()
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         while not self.started:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             time.sleep(1e-3)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def cleanup(self):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.should_exit = True
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         self.thread.join()
