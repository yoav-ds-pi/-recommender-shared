from signal import signal, SIGINT, SIGTERM

go = True


def is_go():
    global go
    return go


def exit_gracefully(*_o):
    global go
    go = False


signal(SIGINT, exit_gracefully)
signal(SIGTERM, exit_gracefully)
