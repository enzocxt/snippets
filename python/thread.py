try:
    import threading
except ImportError:
    import dummy_threading as threading  # type: ignore


class LogState(object):
    def __init__(self):
        self.indentation = 0


_log_state = LogState()
_log_state.indentation = 1
print _log_state.indentation
