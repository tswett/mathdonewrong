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
from dataclasses import dataclass
from typing import TypeVar

from mathdonewrong.boolexpr import BoolExpr

T = TypeVar('T')

class BoolProof:
    @property
    def lhs(self) -> BoolExpr:
        raise NotImplementedError

    @property
    def rhs(self) -> BoolExpr:
        raise NotImplementedError

    def destruct(self, destructor: BoolProofDestructor[T]) -> T:
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

    def destruct(self, destructor: BoolProofDestructor[T]) -> T:
        return destructor.or_commutativity(self.a, self.b)

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

    def destruct(self, destructor: BoolProofDestructor[T]) -> T:
        return destructor.or_associativity(self.a, self.b)

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

    def destruct(self, destructor: BoolProofDestructor[T]) -> T:
        proof1_ = self.proof1.destruct(destructor)
        proof2_ = self.proof2.destruct(destructor)

        return destructor.composed_proof(proof1_, proof2_)

class BoolProofDestructor:
    def or_associativity(self, a: BoolExpr, b: BoolExpr) -> T:
        raise NotImplementedError

    def or_commutativity(self, a: BoolExpr, b: BoolExpr) -> T:
        raise NotImplementedError

    def composed_proof(self, proof1: T, proof2: T) -> T:
        raise NotImplementedError
