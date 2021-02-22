def get_name() -> str:
    """
    Should return the name of the mapper
    """
    raise NotImplementedError()


def check_connection() -> bool:
    """
    Return whether there is an active connection
    """
    raise NotImplementedError()


def check_indexes() -> bool:
    """
    Checks (and potentially installs) search indexes
    """
    raise NotImplementedError()
