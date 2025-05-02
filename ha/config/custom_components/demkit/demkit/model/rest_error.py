class RestError(Exception):  # noqa: D100
    """Custom exception class for REST API errors.

    Attributes:
        status_code (int): The HTTP status code associated with the error.
        message (str): A description of the error.

    Args:
        status_code (int): The HTTP status code to be associated with the error.
        message (str): A description of the error.

    """

    def __init__(self, status_code, message) -> None:
        """Initialize a RestError instance.

        Args:
            status_code (int): The HTTP status code associated with the error.
            message (str): A description of the error.

        """

        self.status_code = status_code
        self.message = message
        super().__init__(message)
