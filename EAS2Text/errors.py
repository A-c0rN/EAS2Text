class InvalidSAME(Exception):
    def __init__(self, error, message="Invalid Data in SAME Message"):
        self.message = message
        self.error = error
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.error}"


class MissingRequiredData(Exception):
    def __init__(self, error, message="Missing a required data input"):
        self.message = message
        self.error = error
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.error}"


class MissingSAME(Exception):
    def __init__(self, message="Missing SAME Message"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
