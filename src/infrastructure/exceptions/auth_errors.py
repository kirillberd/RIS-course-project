class AuthError(Exception):
    def __init__(self, name, *args: object) -> None:
        super().__init__(*args)
        self.name = name

    def __str__(self) -> str:
        return f"Auth errorr: {self.name}"


class UserAlreadyExistsError(AuthError):
    def __init__(self, name, *args: object) -> None:
        super().__init__(name, *args)

    def __str__(self) -> str:
        return f"UserAlreadyExistsErorr: {self.name}"


