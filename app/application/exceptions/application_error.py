class ApplicationError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        context: dict | None = None
    ) -> None:
        self.code = code
        self.message = message
        self.context = context or {}

        super().__init__(message)
