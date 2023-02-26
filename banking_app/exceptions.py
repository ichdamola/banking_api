class AccountNotFoundError(Exception):
    """
    Exception raised when an account is not found.
    """

    def __init__(self, message="Account not found"):
        self.message = message
        super().__init__(self.message)


class InsufficientFundsError(Exception):
    """
    Exception raised when there are insufficient funds in an account for a transaction.
    """

    def __init__(self, message="Insufficient funds"):
        self.message = message
        super().__init__(self.message)


class InvalidTransactionTypeError(Exception):
    """
    Exception raised when an invalid transaction type is specified.
    """

    def __init__(self, message="Invalid transaction type"):
        self.message = message
        super().__init__(self.message)
