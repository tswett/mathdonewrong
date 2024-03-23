# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

"""
Untyped primitive recursive functions

This module contains one definition of primitive recursive functions.

The definition here is based on `this definition from Wikipedia
<https://en.wikipedia.org/w/index.php?title=Primitive_recursive_function&oldid=1210922588#Definition>`_.
The main difference is that the composition operator from Wikipedia (which takes
a list of "first" functions and passes all their results into the "second"
function) is replaced with two separate operators: :class:`Stack`, which takes a
list of functions and combines them into a single function that returns a list
of results, and :class:`Comp`, which takes one "first" function and passes all
of its results into the "second" function.

Expression classes
------------------

.. autoclass:: PConst
.. autoclass:: Succ
.. autoclass:: Proj
.. autoclass:: Stack
.. autoclass:: Comp
.. autoclass:: PrimRec

The evaluation algebra
----------------------

.. autoclass:: StandardPrimitiveRecursiveAlgebra

List of members
---------------
"""

from __future__ import annotations
from typing import Any, Callable

from mathdonewrong.algebras import Algebra, operator
from mathdonewrong.expressions import Literal, NamedOper

PRValue = Any

class PConst(NamedOper):
    """
    Constant function

    For any value ``x``, ``PConst(x)`` represents a function that ignores its
    arguments and returns ``x``.
    """
    def __init__(self, value: PRValue):
        super().__init__(Literal(value))

    def __repr__(self):
        operand, = self.operands
        return f"PConst({operand.value})"

class Succ(NamedOper):
    """
    Successor function

    The expression ``Succ()`` represents a function that takes any natural
    number :math:`x` and returns :math:`x + 1`.
    """

class Proj(NamedOper):
    """
    Projection function

    For any number ``index``, ``Proj(index)`` represents a function that takes
    any number of arguments (as long as it is at least ``index + 1``) and
    returns argument number ``index`` (starting at 0).
    """
    def __init__(self, index: PRValue):
        super().__init__(Literal(index))

    def __repr__(self):
        operand, = self.operands
        return f"Proj({operand.value})"

class Stack(NamedOper):
    """
    Stack of functions

    Given a collection of functions ``f1``, ``f2``, ..., ``fn``, the expression
    ``Stack(f1, f2, ..., fn)`` represents a function that takes any number of
    arguments ``*args`` and returns the list ``[f1(*args), f2(*args), ...,
    fn(*args)]``.
    """

class Comp(NamedOper):
    """
    Composition of functions (left-to-right)

    Given two functions ``f`` and ``g``, the expression ``Comp(f, g)``
    represents a function which takes any number of arguments ``*args`` and
    returns ``g(*f(*args))``. Note that ``f`` is applied first, and the results
    are unpacked before being passed to ``g``.
    """

class PrimRec(NamedOper):
    """
    Primitive recursion

    Given two functions ``base`` and ``step``, the expression ``PrimRec(base,
    step)`` represents a function which performs primitive recursion. To be
    precise, it represents a function which behaves like this::

        def prim_rec(x, *args):
            value = base(*args)
            for i in range(x):
                value = step(i, value, *args)
            return value
    """

class StandardPrimitiveRecursiveAlgebra(Algebra):
    """
    The evaluation algebra for primitive recursive functions

    An instance of ``StandardPrimitiveRecursiveAlgebra`` is an algebra that
    evaluates a primitive recursive expression (as defined in this module) and
    returns a function that behaves in the expected way.

    For example::

        >>> alg = StandardPrimitiveRecursiveAlgebra()
        >>> expr = Stack(Succ(), PConst(2))
        >>> func = expr.evaluate_in(alg)
        >>> func(10)
        [11, 2]
    """
    @operator('PConst')
    def const(self, value: PRValue) -> Callable:
        def const_func(*args: PRValue) -> PRValue:
            return value

        return const_func

    def succ(self) -> Callable[[int], int]:
        def succ_func(x):
            return x + 1

        return succ_func

    def proj(self, index: int) -> Callable:
        def proj_func(*args: PRValue) -> PRValue:
            return args[index]

        return proj_func

    def stack(self, *funcs: Callable) -> Callable:
        def stacked_func(*args: PRValue) -> list[PRValue]:
            return [f(*args) for f in funcs]

        return stacked_func

    def comp(self, f: Callable, g: Callable) -> Callable:
        def comp_func(*args: PRValue) -> PRValue:
            intermediate = g(*args)
            return f(*intermediate)

        return comp_func

    def prim_rec(self, base: Callable, step: Callable) -> Callable:
        def prim_rec_func(x: PRValue, *args: PRValue) -> PRValue:
            value = base(*args)
            for i in range(x):
                value = step(i, value, *args)
            return value

        return prim_rec_func
