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
from functools import reduce
import inspect
from typing import Any, Callable, TypeVar, Union
from mathdonewrong.algebras import Algebra, operator

from mathdonewrong.expressions import Expression, Literal, NamedOper, Var

class MonoidExpr(Expression):
    def __mul__(self, other: MonoidExpr) -> MonoidExpr:
        return MonOper(self, other)

class MonLiteral(MonoidExpr, Literal):
    pass

class MonVar(MonoidExpr, Var):
    pass

class Id(MonoidExpr, NamedOper):
    pass

class MonOper(MonoidExpr, NamedOper):
    def __init__(self, left: MonoidExpr, right: MonoidExpr):
        super().__init__(left, right)

class Assoc(MonoidExpr, NamedOper):
    pass

class Monoid(Algebra):
    T: type

    @property
    def id(self) -> T:
        return self.id_()

    @operator('Id')
    def id_(self) -> T:
        raise NotImplementedError

    @operator('MonOper')
    def oper_(self, a: T, b: T) -> T:
        raise NotImplementedError

    def oper(self, *args: T) -> T:
        return reduce(self.oper_, args, self.id)

    # TODO: add methods for left and right identity and associativity

class CommutativeMonoid(Monoid):
    pass

class AdditiveMonoid(Monoid):
    def oper_(self, a: T, b: T) -> T:
        return a + b

class MultiplicativeMonoid(Monoid):
    def oper_(self, a: T, b: T) -> T:
        return a * b

class IntAddition(CommutativeMonoid, AdditiveMonoid):
    T = int

    @property
    def id(self) -> int:
        return 0

int_addition = IntAddition()

class IntMultiplication(CommutativeMonoid, MultiplicativeMonoid):
    T = int

    @property
    def id(self) -> int:
        return 1

int_multiplication = IntMultiplication()

class StringMonoid(AdditiveMonoid):
    T = str

    @property
    def id(self) -> str:
        return ''

string_monoid = StringMonoid()

class TupleMonoid(AdditiveMonoid):
    def __init__(self, T: type):
        self.T = tuple[T, ...]

    @property
    def id(self) -> tuple[T, ...]:
        return ()

tuple_monoid = TupleMonoid(Any)

class MonoidHomomorphism:
    def __init__(self, f: Callable, domain: Monoid = None, codomain: Monoid = None):
        if domain is None:
            first_parameter_name = list(inspect.signature(f).parameters)[0]
            domain = inspect.get_annotations(f, eval_str=True)[first_parameter_name]
        if codomain is None:
            codomain = inspect.get_annotations(f, eval_str=True)['return']

        self.domain = domain
        self.codomain = codomain
        self.f = f

    def __call__(self, x: domain.T) -> codomain.T:
        return self.f(x)

@MonoidHomomorphism
def string_length(x: string_monoid) -> int_addition:
    return len(x)

def int_scale(x: int) -> MonoidHomomorphism:
    @MonoidHomomorphism
    def f(y: int_addition) -> int_addition:
        return x * y

    return f

@dataclass
class MonoidEquation:
    lhs: MonoidExpr
    rhs: MonoidExpr
    valid: bool

    @staticmethod
    def id() -> MonoidEquation:
        return MonoidEquation.refl(Id())

    def __mul__(self, other: MonoidEquation) -> MonoidEquation:
        return MonoidEquation(
            self.lhs * other.lhs,
            self.rhs * other.rhs,
            self.valid and other.valid)

    def assoc(self, b: MonoidEquation, c: MonoidEquation) -> MonoidEquation:
        return MonoidEquation(
            ((self * b) * c).lhs,
            (self * (b * c)).rhs,
            valid=self.valid and b.valid and c.valid)

    @staticmethod
    def refl(a: MonoidExpr) -> MonoidEquation:
        return MonoidEquation(a, a, valid=True)

    def symm(self) -> MonoidEquation:
        return MonoidEquation(self.rhs, self.lhs, self.valid)

    def trans(self, other: MonoidEquation) -> MonoidEquation:
        valid = self.valid and other.valid and self.rhs == other.lhs
        return MonoidEquation(self.lhs, other.rhs, valid)

class MonoidEqualityAlgebra(Monoid):
    T = MonoidEquation

    def id_(self) -> MonoidEquation:
        return MonoidEquation.id()

    def oper_(self, a: MonoidEquation, b: MonoidEquation) -> MonoidEquation:
        return a * b

    def assoc(self, a: MonoidEquation, b: MonoidEquation, c: MonoidEquation) -> MonoidEquation:
        return a.assoc(b, c)

    def eq_symm(self, a: MonoidEquation) -> MonoidEquation:
        return a.symm()

    def eq_trans(self, a: MonoidEquation, b: MonoidEquation) -> MonoidEquation:
        return a.trans(b)
