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
Typed primitive recursive functions

This is a definition of primitive recursive functions that is, in my opinion, a
bit more elegant than the one in
:mod:`~mathdonewrong.primitive_recursive.primrec_exprs`. The main difference is
that here, there are two families of types (natural numbers, and tuples), and
every function takes exactly one parameter.

I made a misstep in my initial implementation of the type system: I tried to use
Python's native type hints to represent the types of the functions. However,
Python's native type hints are pretty difficult to deal with; it would be better
to define a new system of my own.

Expression classes
------------------

.. autoclass:: PrimRecExpr
.. autoclass:: Succ
.. autoclass:: Zero
.. autoclass:: Fork
.. autoclass:: Select
.. autoclass:: Id
.. autoclass:: Comp
.. autoclass:: Const
.. autoclass:: NatRecurse

The typechecking and evaluation algebras
----------------------------------------

.. autoclass:: TypecheckAlgebra
.. autoclass:: ToFuncAlgebra

List of members
---------------
"""

from __future__ import annotations

from typing import Callable, ParamSpec, TypeVar

from mathdonewrong.algebras import Algebra
from mathdonewrong.expressions import Expression, Literal, NamedOper

P = ParamSpec('P')
T, U, V = TypeVar('T'), TypeVar('U'), TypeVar('V')

class PrimRecExpr(Expression):
    def typecheck(self):
        return self.evaluate_in(TypecheckAlgebra())

    def to_func(self):
        return self.evaluate_in(ToFuncAlgebra())

class Succ(PrimRecExpr, NamedOper):
    r"""
    Successor function

    The expression ``Succ()`` represents the successor function, of type
    :math:`\mathbb{N} \to \mathbb{N}`.
    """

class Zero(PrimRecExpr, NamedOper):
    r"""
    Zero

    The expression ``Zero()`` represents the constantly-zero function, of type
    :math:`\mathbf{1} \to \mathbb{N}`.

    In the current implementation, evaluating ``Zero()`` produces a Python
    function which takes no arguments. That's probably a mistake; it should take
    one argument and ignore it.
    """

class Fork(PrimRecExpr, NamedOper):
    r"""
    Pair (fork) of functions

    Given a function ``f`` of type :math:`A \to B` and a function ``g`` of type
    :math:`A \to C`, the expression ``Fork(f, g)`` represents the function of
    type :math:`A \to B \times C` that takes an argument ``x`` and returns the
    pair ``(f(x), g(x))``.
    """

class Select(PrimRecExpr, NamedOper):
    r"""
    Tuple projection (selection)

    Given any two types :math:`A` and :math:`B`, the expression ``Select(0, A,
    B)`` represents the function of type :math:`A \times B \to A` that takes a
    pair ``(x, y)`` and returns the first component ``x``, and the expression
    ``Select(1, A, B)`` represents the function of type :math:`A \times B \to B`
    that takes a pair ``(x, y)`` and returns the second component ``y``.
    """

    def __init__(self, index: int, first: type, second: type):
        super().__init__(Literal(index), Literal(first), Literal(second))

    def __repr__(self):
        index, first, second = self.operands
        return f'Select({index.value}, {first.value}, {second.value})'

class Id(PrimRecExpr, NamedOper):
    r"""
    Identity function

    Given any type :math:`A`, the expression ``Id(A)`` represents the identity
    function of type :math:`A \to A`.
    """
    def __init__(self, domain: type):
        super().__init__(Literal(domain))

    def __repr__(self):
        domain, = self.operands
        return f'Id({domain.value})'

class Comp(PrimRecExpr, NamedOper):
    r"""
    Function composition

    Given a function ``f`` of type :math:`A \to B` and a function ``g`` of type
    :math:`B \to C`, the expression ``Comp(f, g)`` represents the composition of
    ``f`` and ``g``, of type :math:`A \to C`.
    """

class Const(PrimRecExpr, NamedOper):
    r"""
    Constant function

    Given any two types :math:`A` and :math:`B`, and a value ``x`` of type
    :math:`B`, the expression ``Const(A, B, x)`` represents the constant
    function of type :math:`A \to B` that ignores its argument and returns
    ``x``.
    """

    def __init__(self, domain: type, codomain: type, value: codomain):
        super().__init__(Literal(domain), Literal(codomain), Literal(value))

    def __repr__(self):
        domain, codomain, value = self.operands
        return f'Const({domain.value}, {codomain.value}, {value.value})'

class NatRecurse(PrimRecExpr, NamedOper):
    r"""
    Recursion on natural numbers

    Given a base case function ``base`` of type :math:`A \to B`, and a step case
    function ``step`` of type :math:`A \times B \to B`, the expression
    ``NatRecurse(base, step)`` represents the function of type :math:`A \times
    \mathbb{N} \to B` that does the following:

    - Take a pair :math:`(x, n)`, where :math:`x : A` is a "common parameter"
      and :math:`n : \mathbb{N}` is the number of times to iterate.
    - Evaluate ``base(x)`` and store its result in an accumulator variable
      :math:`y`.
    - Do the following :math:`n` times: evaluate ``step(x, y)`` and store its
      result in :math:`y`.
    - Return the final value of :math:`y`.
    """

class TypecheckAlgebra(Algebra):
    def succ(self):
        return Callable[[int], int]

    def zero(self):
        return Callable[[], int]

    def fork(self, first: type, second: type) -> type:
        first_args, first_result = first.__args__[:-1], first.__args__[-1]
        second_args, second_result = second.__args__[:-1], second.__args__[-1]

        if first_args == second_args:
            return Callable[first_args, tuple[first_result, second_result]]
        else:
            return None

    def select(self, index: int, first: type, second: type) -> type:
        result = [first, second][index]

        return Callable[[tuple[first, second]], result]

    def id(self, domain: type) -> type:
        return Callable[[domain], domain]

    def comp(self, first: type, second: type) -> type:
        first_args, first_result = first.__args__[:-1], first.__args__[-1]
        second_args, second_result = second.__args__[:-1], second.__args__[-1]
        
        if second_args == (first_result,):
            return Callable[first_args, second_result]
        else:
            return None

    def const(self, domain: type, codomain: type, value: codomain) -> type:
        return Callable[[domain], codomain]

    def nat_recurse(self, base: type, step: type) -> type:
        # TODO: return None if one of these destructions fails
        (base_arg,), base_result = base.__args__[:-1], base.__args__[-1]

        (step_arg,), step_result = step.__args__[:-1], step.__args__[-1]
        step_arg1, step_arg2 = step_arg.__args__

        # TODO: Make these checks work. As of this writing, this doesn't work
        # because None and NoneType are not recognized as being the same thing.

        #if base_arg != step_arg1:
        #    raise ValueError(f"mismatch: {base_arg=} != {step_arg1=}")
        #if not (base_result == step_arg2 == step_result):
        #    raise ValueError(f"mismatch: {base_result=} != {step_arg2=} != {step_result=}")

        return Callable[[tuple[base_arg, int]], base_result]

class ToFuncAlgebra(Algebra):
    def succ(self):
        def succ_func(x: int) -> int:
            return x + 1

        return succ_func

    def zero(self):
        def zero_func() -> int:
            return 0

        return zero_func

    def fork(self, first: Callable[P, T], second: Callable[P, U]) -> Callable[P, tuple[T, U]]:
        def fork_func(*args: P.args) -> tuple[T, U]:
            return (first(*args), second(*args))

        return fork_func

    def select(self, index, first, second):
        def select_func(t):
            return t[index]

        return select_func

    def id(self, domain: type) -> Callable[[domain], domain]:
        def id_func(x: domain) -> domain:
            return x

        return id_func

    def comp(self, first: Callable[P, U], second: Callable[[U], V]) -> Callable[P, V]:
        def comp_func(*args: P.args) -> V:
            return second(first(*args))

        return comp_func

    def const(self, domain: type, codomain: type, value: codomain) -> Callable[[domain], codomain]:
        def const_func(x: domain) -> codomain:
            return value

        return const_func

    def nat_recurse(self,
                    base: Callable[[T], U],
                    step: Callable[[tuple[T, U]], U]
                    ) -> Callable[[tuple[T, int]], U]:

        def nat_recurse_func(args: tuple[T, int]) -> U:
            parameter, count = args

            accumulator = base(parameter)
            for _ in range(count):
                accumulator = step((parameter, accumulator))

            return accumulator

        return nat_recurse_func
