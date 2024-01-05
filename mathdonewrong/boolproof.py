# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from dataclasses import dataclass

from mathdonewrong.boolexpr import BoolExpr

class BoolProof:
    @property
    def lhs(self) -> BoolExpr:
        raise NotImplementedError

    @property
    def rhs(self) -> BoolExpr:
        raise NotImplementedError

@dataclass
class OrCommutativity:
    a: BoolExpr
    b: BoolExpr

    @property
    def lhs(self) -> BoolExpr:
        return self.a | self.b

    @property
    def rhs(self) -> BoolExpr:
        return self.b | self.a

@dataclass
class OrAssociativity:
    a: BoolExpr
    b: BoolExpr
    c: BoolExpr

    @property
    def lhs(self) -> BoolExpr:
        return self.a | (self.b | self.c)

    @property
    def rhs(self) -> BoolExpr:
        return (self.a | self.b) | self.c

@dataclass
class ComposedProof:
    proof1: BoolProof
    proof2: BoolProof

    def __post_init__(self):
        if self.proof1.rhs != self.proof2.lhs:
            raise ValueError(
                f"Proof sides don't match: the first proof ends with {self.proof1.rhs} but the second proof starts with {self.proof2.lhs}")

    @property
    def lhs(self) -> BoolExpr:
        return self.proof1.lhs

    @property
    def rhs(self) -> BoolExpr:
        return self.proof2.rhs
