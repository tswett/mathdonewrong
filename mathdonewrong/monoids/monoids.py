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
Monoids

This module defines monoids—that is, sets equipped with an operation which is
associative and has an identity element.

The ``Monoid`` class and related classes
========================================

.. autoclass:: mathdonewrong.monoids.monoids.Monoid

.. autoclass:: mathdonewrong.monoids.monoids.MonoidHomomorphism

Example monoids
===============

.. autoclass:: mathdonewrong.monoids.monoids.IntAddition

.. autoclass:: mathdonewrong.monoids.monoids.BoolDisjunction

List of members
===============
"""

from __future__ import annotations
from dataclasses import dataclass
from functools import reduce
import inspect
from typing import Any, Callable, TypeVar, Union
from mathdonewrong.algebras import Algebra, operator, relation

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
    """
    Set with associative operator with identity

    I should be able to use ``autofunction`` to document some of these methods,
    right? How does that work? It seems like one of the directives here should
    work but none of them seem to be doing anything.

    .. autofunction::mathdonewrong.monoids.monoids.Monoid.id_
    .. autofunction::mathdonewrong.monoids.monoids.Monoid.oper_
    .. autofunction::Monoid.id_
    .. autofunction::id_

    Since that doesn't seem to be working, here's some information about the
    most important members of this class:

    .. attribute:: T: type

       The underlying set or type of this monoid.

    .. function:: id_(self) -> T

       Get the identity element of this monoid.

    .. function:: oper_(self, a: T, b: T) -> T:

       Perform the monoid operation on two elements of this monoid.
    """

    T: type

    @property
    def id(self) -> T:
        return self.id_()

    @operator('Id')
    def id_(self) -> T:
        """here's a docstring"""
        raise NotImplementedError

    @operator('MonOper')
    def oper_(self, a: T, b: T) -> T:
        """here's another docstring"""
        raise NotImplementedError

    def oper(self, *args: T) -> T:
        return reduce(self.oper_, args, self.id)

    @relation()
    def left_id(self, a: T):
        return self.oper_(self.id_(), a)

    def left_id_rhs(self, a: T):
        return a

    @relation()
    def right_id(self, a: T):
        return self.oper_(a, self.id_())

    def right_id_rhs(self, a: T):
        return a

    @relation()
    def assoc(self, a: T, b: T, c: T):
        return self.oper_(self.oper_(a, b), c)
    
    def assoc_rhs(self, a: T, b: T, c: T):
        return self.oper_(a, self.oper_(b, c))

class CommutativeMonoid(Monoid):
    pass

class AdditiveMonoid(Monoid):
    def oper_(self, a: T, b: T) -> T:
        return a + b

class MultiplicativeMonoid(Monoid):
    def oper_(self, a: T, b: T) -> T:
        return a * b

class IntAddition(CommutativeMonoid, AdditiveMonoid):
    """
    The monoid of integers under addition

    .. attribute:: T = int

    .. attribute:: generators = [1]
    .. attribute:: relations = []
    """

    T = int

    generators = [1]
    relations = []

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
    r"""
    Homomorphism of monoids

    A ``MonoidHomomorphism`` is a homomorphism between two
    :class:`~mathdonewrong.monoids.monoids.Monoid`\s (represented as a Python
    function), equipped with a domain and codomain.

    If the domain of a ``MonoidHomomorphism`` has the ``generators`` attribute,
    you can call ``on_generators`` to see what it does to them:

    >>> int_addition_to_bool_disjunction.on_generators()
    [(1, True)]
    """
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

    def on_generators(self) -> list[tuple[domain.T, codomain.T]]:
        return [(1, True)]

@MonoidHomomorphism
def string_length(x: string_monoid) -> int_addition:
    return len(x)

def int_scale(x: int) -> MonoidHomomorphism:
    r"""
    Create a monoid homomorphism :math:`\mathbb{Z} \to \mathbb{Z}` which maps
    each integer :math:`y` to :math:`xy`.
    """

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

class BoolDisjunction(CommutativeMonoid):
    """
    The monoid of booleans under disjunction

    .. attribute:: T = bool

    .. attribute:: generators = [True]
    .. attribute:: relations = [True | True == True]
    """

    T = bool

    generators = [True]
    relations = [(MonOper(Literal(True), Literal(True)), Literal(True))]

    @property
    def id(self) -> bool:
        return False

    @property
    def oper_(self, a: bool, b: bool):
        return a | b

class BoolXor(CommutativeMonoid):
    """
    The monoid of booleans under exclusive disjunction (XOR)

    .. attribute:: T = bool

    .. attribute:: generators = [True]
    .. attribute:: relations = [True | True == False]
    """

    T = bool

    generators = [True]
    relations = [(MonOper(Literal(True), Literal(True)), Id())]

    @property
    def id(self) -> bool:
        return False

    @property
    def oper_(self, a: bool, b: bool):
        return a ^ b

class TrivialMonoid(Monoid):
    # TODO: implement this correctly
    pass

@MonoidHomomorphism
def int_addition_to_bool_disjunction(i: int) -> bool:
    # TODO: implement this correctly
    pass

@MonoidHomomorphism
def int_addition_to_bool_xor(i: int) -> bool:
    # TODO: implement this correctly
    pass

def trivial_to(m: Monoid) -> MonoidHomomorphism:
    @MonoidHomomorphism
    def hom(a: TrivialMonoid) -> m:
        # TODO: implement this correctly
        pass

    return hom
