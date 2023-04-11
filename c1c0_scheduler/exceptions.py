class DisconnectedClient(RuntimeError):
    """
    Raised when a client was dropped without properly closing.

    In production (or demo), should be ignored.
    """
    def __init__(self, client_name, *args: object) -> None:
        super().__init__(client_name, *args)