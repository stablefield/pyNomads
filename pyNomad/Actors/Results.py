"""

"""



class Result(Monad, Generic[T]):
    """
    Monad to handle errors. Handle exceptions on unwrap:

    ```python
    x = (
        Result(3)
        >> (lamba x / 0)
    )

    x.value == None
    isinstance(x.exception, ZeroDivisionError)
    x.unwrap_or(4) == 4
    ```
    """

    def __init__(self, value: T, exception: Optional[Type[Exception]] = None):
        """
        Create Result monad with value and exception
        (one of which will always be None)
        """
        self.value: T = value
        self.exception = exception

    def bind(self, func):
        """
        Execute function on value, if error is raised,
        returned Monad will have value of "None" and an exception.

        Otherwise, exception will be None, and value will be return.

        If exception already exists, function won't be executed.
        """
        if self.exception:
            return self
        try:
            return Result(func(self.value))
        except Exception as exception:
            return Result(None, exception)

    def unwrap(self) -> T:
        """
        If exception is raised, will raise exception.
        Otherwise wil
        l evaluate to value.
        """
        if self.exception:
            raise self.exception
        return self.value

    def unwrap_or(self,
                  value: U) -> Union[T, U]:
        """
        If exception is raised, will default to given value.
        """
        if self.exception:
            return value
        return self.value

    def __str__(self) -> str:
        """
        Custom string representation
        """
        return f"{self.__class__.__name__}({self.exception or self.value})"
z