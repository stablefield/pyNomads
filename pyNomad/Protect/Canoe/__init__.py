"""
Base type for Nomad value types to be resistant to type coercion
and to be able to be used in a type-safe manner in pyNomad - the
base type is a Monad, which is a type that can be wrapped in a logical
container and unwrapped. These types are not monadic in the sense of
functional programming, but they are monadic in the sense that they
represent a value that can be wrapped and unwrapped with a logical
protection against their state being changed by the outside world.

1. Canoe - a lightweight base found in the base of pyNomad.Protect.Canoe
