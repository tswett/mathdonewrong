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
from typing import Any, Callable

from mathdonewrong.algebras import Algebra, operator
from mathdonewrong.expressions import Literal, NamedOper

PRValue = Any

class PConst(NamedOper):
    def __init__(self, value: PRValue):
        super().__init__(Literal(value))

    def __repr__(self):
        operand, = self.operands
        return f"PConst({operand.value})"

class Succ(NamedOper):
    pass

class Proj(NamedOper):
    def __init__(self, index: PRValue):
        super().__init__(Literal(index))
        pass

    def __repr__(self):
        operand, = self.operands
        return f"Proj({operand.value})"

class Stack(NamedOper):
    pass

class Comp(NamedOper):
    pass

class PrimRec(NamedOper):
    pass

class StandardPrimitiveRecursiveAlgebra(Algebra):
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
        def prim_rec_func(x: PRValue) -> PRValue:
            # TODO: provide the correct first argument for step, and pass the pass-through parameters
            value = base()
            for i in range(x):
                value = step(0, value)
            return value

        return prim_rec_func
