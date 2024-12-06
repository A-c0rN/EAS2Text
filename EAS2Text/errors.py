class InvalidSAMEError(Exception):
    def __init__(self, error, message="Invalid Data in SAME Message"):
        self.message = message
        self.error = error
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.error}"


class InvalidParameterError(Exception):
    def __init__(self, error, message="Parameter is not valid input"):
        self.message = message
        self.error = error
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.error}"


class MissingSAMEError(Exception):
    def __init__(self, message="Missing SAME Message"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
