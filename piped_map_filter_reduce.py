"""Versions of map, filter, and reduce that support partial application and piping."""

from abc import abstractmethod
from functools import reduce


class PartialBase:
    """Base class for partial transformations that are applied to an iterable."""

    @property
    @abstractmethod
    def transformation(self):
        """
        Getter for the transformation to be applied to iterable.

        When finally applied to an iterable (see definition of __call__):

            self.tranformation(function, iterable, *args, **kwargs)
        """

    def __init__(self, function, *args, **kwargs):
        """Initialize with the function (and args) that the transformation will use."""
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self, iterable, *args, **kwargs):
        """Let the meta_function apply the stored function on the iterable."""
        updated_kwargs = {**self.kwargs, **kwargs}

        return self.transformation(
            self.function, iterable, *self.args, *args, **updated_kwargs
        )

    def __ror__(self, iterable):
        """If the object is on the rhs of a pipe call the object on the lhs iterable."""
        return self(iterable)


def emap(function, iterable=None):
    """Extend map function to support partial application and pipes."""
    if iterable:
        return map(function, iterable)

    class PartialMap(PartialBase):  # pylint: disable=R0903
        """PartialMap objects are partially applied and support pipes."""

        @property
        def transformation(self):
            return map

    return PartialMap(function)


def efilter(function, iterable=None):
    """Extend filter function to support partial application and pipes."""
    if iterable:
        return filter(function, iterable)

    class PartialFilter(PartialBase):  # pylint: disable=R0903
        """PartialFilter objects are partially applied and support pipes."""

        @property
        def transformation(self):
            return filter

    return PartialFilter(function)


def ereduce(function, *args):
    """Extend reduce function to support partial application and pipes."""
    if args and hasattr(args[0], "__iter__"):
        return reduce(function, *args)

    class PartialReduce(PartialBase):  # pylint: disable=R0903
        """PartialReduce objects are partially applied and support pipes."""

        @property
        def transformation(self):
            return reduce

    return PartialReduce(function, *args)
