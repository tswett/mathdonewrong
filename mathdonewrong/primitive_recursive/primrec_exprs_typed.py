# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from typing import Callable, ParamSpec, TypeVar

from mathdonewrong.algebras import Algebra
from mathdonewrong.expressions import Expression, NamedOper

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

class Comp(PrimRecExpr, NamedOper):
    pass

class TypecheckAlgebra(Algebra):
    def succ(self):
        return Callable[[int], int]

    def zero(self):
        return Callable[[], int]

    def comp(self, first: type, second: type) -> type:
        first_args, first_result = first.__args__[:-1], first.__args__[-1]
        second_args, second_result = second.__args__[:-1], second.__args__[-1]
        
        if second_args == (first_result,):
            # TODO: return the right thing
            return first
        else:
            return None

class ToFuncAlgebra(Algebra):
    def succ(self):
        def succ_func(x: int) -> int:
            return x + 1

        return succ_func

    def zero(self):
        def zero_func() -> int:
            return 0

        return zero_func

    def comp(self, first: Callable[P, U], second: Callable[[U], V]) -> Callable[P, V]:
        def comp_func(*args: P.args) -> V:
            return second(first(*args))

        return comp_func
