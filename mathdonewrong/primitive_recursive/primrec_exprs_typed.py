# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

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
    pass

class Zero(PrimRecExpr, NamedOper):
    pass

class Fork(PrimRecExpr, NamedOper):
    pass

class Select(PrimRecExpr, NamedOper):
    def __init__(self, index: int, first: type, second: type):
        super().__init__(Literal(index), Literal(first), Literal(second))

    def __repr__(self):
        index, first, second = self.operands
        return f'Select({index.value}, {first.value}, {second.value})'

class Comp(PrimRecExpr, NamedOper):
    pass

class Const(PrimRecExpr, NamedOper):
    def __init__(self, domain: type, codomain: type, value: codomain):
        super().__init__(Literal(domain), Literal(codomain), Literal(value))

    def __repr__(self):
        domain, codomain, value = self.operands
        return f'Const({domain.value}, {codomain.value}, {value.value})'

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

    def comp(self, first: type, second: type) -> type:
        first_args, first_result = first.__args__[:-1], first.__args__[-1]
        second_args, second_result = second.__args__[:-1], second.__args__[-1]
        
        if second_args == (first_result,):
            return Callable[first_args, second_result]
        else:
            return None

    def const(self, domain: type, codomain: type, value: codomain) -> type:
        return Callable[[domain], codomain]

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

    def comp(self, first: Callable[P, U], second: Callable[[U], V]) -> Callable[P, V]:
        def comp_func(*args: P.args) -> V:
            return second(first(*args))

        return comp_func

    def const(self, domain: type, codomain: type, value: codomain) -> Callable[[domain], codomain]:
        def const_func(x: domain) -> codomain:
            return value

        return const_func
