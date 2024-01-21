"""
Contains the Signed Version of the Value and the Call Graph, and Functions to Manipulate them
if known to be safe (i.e. the value is not corrupted). A SafeFunction is a nomad that takes a
function and a value and returns a function that takes no arguments and returns the result of the
original function applied to the value. A SafeFunction is a NomadTask, which is a function that
takes a function and a value and returns a function that takes no arguments and returns the result
of the original function applied to the value.

But what is a Nomad? A Nomad is a Monad that has a task assigned to it. A Monad is a container
that can be assigned a task.

You can form a campaign of Nomads by chaining them together with the >> operator. You can safely execute
a chain of Nomads by calling the execute method on the first Nomad in the chain.

A CampaignExecutorNomad is a Nomad that can recover from errors and execute a campaign of functions
asynchronously. It supports async function chaining and call graph generation with error recovery and
alternative strategies, as well as state signing for value corruption detection and recovery from
errors without having to re-execute the entire call graph, as well as call graph generation for error
recovery and debugging both in the form of a string and a graphviz graph object at runtime, as well as
a method to generate a graph of the call graph.

If you use a SafeFunction to bind a function to a Nomad, the function will be executed when the Nomad
is unwrapped. If you assign it to another NomadTask and then bind it to a Nomad, it will be executed
when the NomadTask is executed.

A AsyncSafeFunction is a NomadTask that takes a function and a value and returns a function that takes
no arguments and returns the result of the original function applied to the value.
"""
import copy
import logging
import typing as t

from tqdm import asyncio

from pyNomad import T


class HiddenValue(t.Generic[T], asyncio.Future):
    """
    Contains the Signed Version of the Value and the Call Graph, and Functions to Manipulate them
    """

    def __init__(self, hardened=False):
        """
        Initialize the SignedValue
        Args:
            hardened: Whether the value is hardened, meaning that it cannot be changed without
            serious application of force
        """
        self.signature = None

    def init(self, value):
        """
        Initialize the SignedValue
        """
        self.signature = self.sign(value)
        self.value = copy.deepcopy(value)
        self.logger = logging.getLogger(__name__)
        self.task = None
        self


class SignedValue(object):
    """
    Contains the Signed Version of the Value and the Call Graph, and Functions to Manipulate them
    """

    def __init__(self, hardened=False):
        """
        Initialize the SignedValue
        Args:
            hardened: Whether the value is hardened, meaning that it cannot be changed without
            serious application of force
        """
        self.signature = None

    def init(self, value):
        """
        Initialize the SignedValue
        """
        self.signature = self.sign(value)
        self.value = copy.deepcopy(value)
        self.logger = logging.getLogger(__name__)
        self.task = None
        self
