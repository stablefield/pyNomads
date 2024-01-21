# pyNomad - Monadic Nomadic Delegates
## A stable, predictive, execution framework.

Delicious monads for functional programming patterns in python!

[Check out the api docs for reference](https://benrutter.github.io/monads/monadcontainers.html)

![Coverage Badge](https://img.shields.io/badge/coverage-100-green) ![Static Badge](https://img.shields.io/badge/python-%3E%3D3.8-blue)

## Project Goals

This library is meant to be a simple class for functional chaining in python in a way that:

- Can be intergrated quickly/simply with existing code
- Maintains type safety
- Depends only on the standard library


## Quick Start

Install libary with pip:

```bash
pip install monadcontainers
```

You can now import monad classes for handling functional chains over data.

Say we want to pass a value through a list of functions like so:

```python
def add_six(x: int) -> int:
  return x + 6

def minus_two(x: int) -> int:
  return x - 2

x = minus_two(add_six(4))  # x == 8
```

This can be a little messy with long calls, more importantly monads can handle repeated work for us with each call (but we'll cover that in a sec).

A basic identity Monad implementing the above looks like this:

```python
from monadcontainers.monads import Monad

x = (
    Monad(4)
    .build_path(add_six)
    .build_path(minus_two)
)  # x == Monad(8)

y = x.value  # y == 8
```

This above pattern chains the Monad contained value through the relevant functions. For alternative syntactical sugar to the `bind` method, you can use `>>`:

```python
x = (
  Monad(4)
  >> add_six
  >> minus_two
)  # x == Monad(8)
```

We can also use Monads to handle additional functionality for us, like error handling with the `Encapsulate` monad:

```python
def divide_by_zero(x: int) -> int:
    return x / 0

x = (
  Encapsulate(4)
  >> add_six
  >> divide_by_zero
  >> minus_two
)  # x is a result monad

x.unwrap()  # <- raises divide by zero exception
x.unwrap_or(42)  # <- evaluates to 42
x.value  # <- is None (since exception has been raised)
x.exception  # <- is a ZeroDivisionError
```

Monad's can be a helpful pattern for functional programming, see the docs for more info on available Monad classes.

Enjoy! 👍

