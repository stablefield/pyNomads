"""

"""
from typing import Generic, Callable
from pyNomad.Capsules.Monads import Monad
from pyNomad import T


class Maybe(Monad, Generic[T]):
    """
    Monad to handle None values.
    THe value here will be set to None if it encounters a None value as
    a result of a function calls nature or execution error.
    ex.

    ```python

    Maybe(4) >> (lambda x: x + 4)  # will return Maybe(8)
    Maybe(None) >> (lambda x: x + 4)  # will return Maybe(None)

    ```

    Write functions as if they can't recieve None values.
    If Monad value is None, it will skip execution of function
    and remain as....

    None example under BaseMon
    ```python
    Maybe(None) >> (lambda x: x + 4)  # will remain None
    ```
    """

    def build_path(self, func: Callable) -> "Maybe":
        """
        Execute function on value, unless None
        (in which case return None monad)
        """
        if self.value is None:
            return Maybe(None)
        return Maybe(func(self.value))
