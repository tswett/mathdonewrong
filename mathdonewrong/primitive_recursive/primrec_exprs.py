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
from typing import Callable

from mathdonewrong.algebras import Algebra, operator
from mathdonewrong.expressions import Literal, NamedOper

class PConst(NamedOper):
    def __init__(self, value: int):
        super().__init__(Literal(value))

    def __repr__(self):
        operand, = self.operands
        return f"PConst({operand.value})"

class Succ(NamedOper):
    pass

class Proj(NamedOper):
    def __init__(self, index: int):
        super().__init__(Literal(index))
        pass

    def __repr__(self):
        operand, = self.operands
        return f"Proj({operand.value})"

class Comp(NamedOper):
    pass

class StandardPrimitiveRecursiveAlgebra(Algebra):
    @operator('PConst')
    def const(self, value: int) -> Callable:
        def const_func(*args: int) -> int:
            return value

        return const_func

    def succ(self) -> Callable[[int], int]:
        def succ_func(x):
            return x + 1

        return succ_func

    def proj(self, index: int) -> Callable:
        def proj_func(*args: int) -> int:
            return args[index]

        return proj_func

    def comp(self, f: Callable, *gs: Callable) -> Callable:
        def comp_func(*args: int) -> int:
            intermediates = [g(*args) for g in gs]
            return f(*intermediates)

        return comp_func
