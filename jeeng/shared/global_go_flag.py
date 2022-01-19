from signal import signal, SIGINT, SIGTERM

_go = True


def is_go():
    global _go
    return _go


def exit_gracefully(*_o):
    global _go
    _go = False


signal(SIGINT, exit_gracefully)
signal(SIGTERM, exit_gracefully)
