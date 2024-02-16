class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes
    - - - - - - - - - - - - - - - - - -

      expression : str
        Input expression in which the error ocurred.

      message : str
        Explaination of the error.
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class SigmaError(Error):
    """Exception raised for errors in the transition.

    Attributes
    - - - - - - - - - - - - - - - - - -

      expression : str
        Input expression in which the error ocurred.

      message : str
        Explanation of the error.
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
