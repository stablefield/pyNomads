from typing import Any, Callable, Generic, Tuple
from typing import List as ListType
from typing import Optional, Type, TypeVar, Union
import asyncio
import hashlib
import traceback

T = TypeVar("T")
U = TypeVar("U")


class Monad(Generic[T]):
    """
    Identity monad (also the parent class for all other monads).

    No additional work is handled on function calls, apart from returning
    a new monad with an updated result.

    Can be used like so:

    ```python
    def make_loud(x:str) -> str:
        return x.upper()

    x = Monad("hello world!") >> make_loud

    print(x.value)
    # prints out "HELLO WORLD!"
    ```
    """
    def __init__(self: Any, value: T) -> None:
        """
        Initialise a monad with the given value
        """
        self.value: T = value

    def bind(self, func) -> "Monad":
        """
        Method to apply function to value of Monad.
        Returns a monad with the updated value.

        Example:
        ```python
        Monad(2).bind(lambda x: x+1) == Monad(3)
        ```

        Can be aliased with `>>` symbol:
        ```python
        (Monad(2) >> (lambda x: x+1)) == Monad(3)
        """
        return Monad(func(self.value))

    def __rshift__(self, other) -> "Monad":
        """
        Dunder method to alias bind into >>
        """
        return self.bind(other)

    def __lshift__(self, other) -> "Monad":
        """
        Dunder method to alias bind into <<
        return self.bind(other)
        """
        return self.bind(other)

    def unwrap(self) -> T:
        """
        Return only the value of the monad without wrapping
        it.

        ```python
        Monad(4).unwrap() == 4
        ```
        """
        return self.value

    def __str__(self) -> str:
        """
        String representation
        """
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self) -> str:
        """
        For repls
        """
        return self.__str__()


class Maybe(Monad, Generic[T]):
    """
    Monad to handle None values.
    Linear operations will be skipped if None is encountered.
    This is useful for handling errors, as well as how you compute a null
    space in linear algebra. It allows you to write code as if you're
    always dealing with a value, and then handle the None case at the end.

    Write functions as if they can't recieve None values.
    If Monad value is None, it will skip execution of function
    and remain as.... (edit) the original state as instability of
    an operation that was, virtually and mathematically, undefined..imaginary.
    The more imaginary components we have in our system, the more features
    for no cost but instead a gain in complexity of imaginary components is
    the matrix stabillity calculation. So let's say we have a 4x4 matrix..., the bijection
    so 2 statees (1,0) (0,1) and (1,1) and (0,0) are the 4 states. So we have 4x4 matrix
    Yes, No, Maybe, and Observer, each with a do something value or not (no cost) 2 operations
    for 1 when you add a responsive error handler to the observer and can do, not do, halfway do, and report.
    So its a 4x4 matrix but it gives us the ability to do them all
    and record the outcomes and preserve the state
    So we have 4x4 matrix but a logarithmic cpu spin up time and a linear memory cost
    which is nothing as its vectorized and the memory is just a pointer to the state

    None example:
    ```python
    Maybe(None) >> (lambda x: x + 4)  # will remain None
    ```
    """
    def bind(self, func: Callable) -> "Maybe":
        """
        Execute function on value, unless None
        (in which case return None monad)
        """
        if self.value is None:
            return Maybe(None)
        return Maybe(func(self.value))


class List(Monad, Generic[T]):
    """
    Monad to apply function to all items in list.

    Write functions as if they act on a single value.

    Example:
    ```python
    x = (
        List([1, 3, 7])
        >> (lambda x: x + 1)
        >> (lambda x: x / 2)
    )
    # x will evaluate to List([1, 2, 4])
    """
    def __init__(self: Any, value: ListType[T]) -> None:
        """
        Initialise a monad with the given list
        """
        self.value: ListType[T] = value

    def bind(self, func: Callable) -> "List":
        """
        Map function on every element of list:

        ```python
        def make_exciting(text: str) -> str:
            return test.upper() + "!!!"

        fun_stuff = (
            List(["hats", "cats", "bats"])
            >> make_exciting
        ).unwrap()

        fun_stuff == ["HATS!!!", "CATS!!!", "BATS!!!"]
        """
        return List([func(x) for x in self.value])

    def filter(self, func: Callable) -> "List":
        """
        Filter list to only elements with true return:

        ```python
        x = (
            List([1, 2, 3, 4])
            .filter(lambda x: x % 2 == 0)
        ).unwrap()

        x == [2, 4]
        """
        return List([i for i in self.value if func(i)])

    def unwrap(self) -> ListType[T]:
        """
        Return only the value of the monad without wrapping
        it.

        ```python
        List([4]).unwrap() == [4]
        ```
        """
        return self.value


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
        Otherwise will evaluate to value.
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






class CompoundMonad(Monad, Generic[T]):
    def __init__(self: Any, value: T) -> None:
        super().__init__(value)
        self.call_graph = []  # Initialize call graph
        self.error = None
        self.signature = self.sign(value)
        self.value = copy.

    def sign(self, value: T) -> str:
        return hashlib.sha256(str(value).encode()).hexdigest()

    async def bind(self, func) -> "Monad":
        self.call_graph.append(func)  # Update call graph
        try:
            if asyncio.iscoroutinefunction(func):
                self.value = await func(self.value)
            else:
                self.value = func(self.value)
            self.check(self.value, self.signature)  # Check the value
        except ZeroDivisionError:
            self.value = self.retry(func, lambda x: 0)  # Retry with alternative strategy
        except Exception as e:
            self.error = e
        return self

    def check(self, value: T, signature: str) -> None:
        assert self.sign(value) == signature, "Value corruption detected"

    def __lshift__(self, other) -> "Monad":
        self.call_graph.append(other)  # Update call graph
        return asyncio.run(self.bind(other))

    def retry(self, func, alternative) -> "Monad":
        try:
            return self >> func  # Try the original operation
        except Exception:
            return self >> alternative  # If it fails, try the alternative

    def unwrap(self) -> Tuple[T, Optional[Exception], str]:
        return self.value, self.error, str(self.call_graph)

    def generate_graph(self) -> str:
        graph = "graph TD\n"
        for i, func in enumerate(self.call_graph):
            graph += f"A{i}[{func.__name__}]\n"
            if i > 0:
                graph += f"A{i-1} --> A{i}\n"
        return graph
    async def alternate_bind(self, func, alternative, final) -> "Monad":
        """
        Bind function to monad, retrying with alternative if it fails.
        """
        try:
            return await self.bind(func)
        except TypeError as e:  # Catching NoneType exception
            try:
                return await self.retry(func, alternative)
            finally: