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

.. autoclass:: mathdonewrong.monoidlike.monoids.Monoid
   :members:

.. autoclass:: mathdonewrong.monoidlike.monoids.MonoidHomomorphism

Example monoids
===============

.. autoclass:: mathdonewrong.monoidlike.monoids.IntAddition

.. autoclass:: mathdonewrong.monoidlike.monoids.BoolDisjunction

Monoid equality
===============

.. autoclass:: MonoidEquation
   :members:
   :special-members: __mul__

.. autoclass:: MonoidEqualityAlgebra
   :members:

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
        return Mop(self, other)

class MonLiteral(MonoidExpr, Literal):
    pass

class MonVar(MonoidExpr, Var):
    pass

class Id(MonoidExpr, NamedOper):
    pass

class Mop(MonoidExpr, NamedOper):
    def __init__(self, left: MonoidExpr, right: MonoidExpr):
        super().__init__(left, right)

class Assoc(MonoidExpr, NamedOper):
    pass

class Monoid(Algebra):
    """
    Set with associative operator with identity
    """

    T: type
    """The underlying set or type of this monoid"""

    @property
    def id(self) -> T:
        return self.id_()

    @operator('Id')
    def id_(self) -> T:
        """Get the identity element of this monoid"""
        raise NotImplementedError

    @operator('Mop')
    def mop_(self, a: T, b: T) -> T:
        """Perform the monoid operation on two elements of this monoid"""
        raise NotImplementedError

    def mop(self, *args: T) -> T:
        return reduce(self.mop_, args, self.id)

    @relation()
    def left_id(self, a: T):
        return self.mop_(self.id_(), a)

    def left_id_rhs(self, a: T):
        return a

    @relation()
    def right_id(self, a: T):
        return self.mop_(a, self.id_())

    def right_id_rhs(self, a: T):
        return a

    @relation()
    def assoc(self, a: T, b: T, c: T):
        return self.mop_(self.mop_(a, b), c)

    def assoc_rhs(self, a: T, b: T, c: T):
        return self.mop_(a, self.mop_(b, c))

class CommutativeMonoid(Monoid):
    pass

class AdditiveMonoid(Monoid):
    def mop_(self, a: T, b: T) -> T:
        return a + b

class MultiplicativeMonoid(Monoid):
    def mop_(self, a: T, b: T) -> T:
        return a * b

class IntAddition(CommutativeMonoid, AdditiveMonoid):
    """
    The monoid of integers under addition

    TODO: As described, this is actually the monoid of natural numbers under
    addition. Oops! We need to fix that.

    .. attribute:: T = int

    .. attribute:: generators = [1]
    .. attribute:: relations = []
    """

    T = int

    generators = [1]
    relations = []

    def id_(self) -> int:
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

    def id_(self) -> str:
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
    :class:`~mathdonewrong.monoidlike.monoids.Monoid`\s (represented as a Python
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
        return [(x, self(x)) for x in self.domain.generators]

def mk_monoid_homomorphism(domain: Monoid = None, codomain: Monoid = None):
    def decorator(f: Callable[[domain.T], codomain.T]) -> MonoidHomomorphism[domain, codomain]:
        return MonoidHomomorphism(f, domain, codomain)

    return decorator

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
    r"""
    Equation of monoid expressions

    A ``MonoidEquation`` consists of two :class:`MonoidExpr`\s along with a
    boolean stating whether or not the equation is considered to be valid.

    It is, of course, possible to create a ``MonoidEquation`` with arbitrary
    ``lhs``, ``rhs``, and ``valid`` flag. However, the methods provide the
    "official" ways to create a ``MonoidEquation``; any equation created using
    these methods will be ``valid`` only if it is correct according to the
    axioms of a monoid.

    With the exception of :meth:`trans`, the equation produced by each of these
    methods is have their ``valid`` flag set to ``True`` if and only if all of
    the input equations have their ``valid`` flags set to ``True``. (For those
    methods that take no equations as inputs, ``valid`` is always ``True``.)

    TODO: Add ``left_id`` and ``right_id`` methods.
    """
    lhs: MonoidExpr
    rhs: MonoidExpr
    valid: bool

    @staticmethod
    def id() -> MonoidEquation:
        r"""
        The identity element

        Create the equation :math:`e = e`, where :math:`e` is the identity element.
        """
        return MonoidEquation.refl(Id())

    def __mul__(self, other: MonoidEquation) -> MonoidEquation:
        r"""
        Multiplication of equations

        Given the equations :math:`A = B` and :math:`C = D`, create the equation
        :math:`A C = B D`.
        """
        return MonoidEquation(
            self.lhs * other.lhs,
            self.rhs * other.rhs,
            self.valid and other.valid)

    def assoc(self, b: MonoidEquation, c: MonoidEquation) -> MonoidEquation:
        r"""
        Associativity

        Given the equations :math:`A_1 = A_2`, :math:`B_1 = B_2`, and :math:`C_1
        = C_2`, create the equation :math:`(A_1 B_1) C_1 = A_2 (B_2 C_2)`.
        """
        return MonoidEquation(
            ((self * b) * c).lhs,
            (self * (b * c)).rhs,
            valid=self.valid and b.valid and c.valid)

    @staticmethod
    def refl(a: MonoidExpr) -> MonoidEquation:
        r"""
        Reflexivity

        Given any expression :math:`A`, create the equation :math:`A = A`.
        """
        return MonoidEquation(a, a, valid=True)

    def symm(self) -> MonoidEquation:
        r"""
        Symmetry

        Given any equation :math:`A = B`, create the equation :math:`B = A`.
        """
        return MonoidEquation(self.rhs, self.lhs, self.valid)

    def trans(self, other: MonoidEquation) -> MonoidEquation:
        r"""
        Transitivity

        Given equations :math:`A = B` and :math:`C = D`, create the equation
        :math:`A = D`. The resulting equation is ``valid`` if and only if both
        input equations are ``valid`` *and* the expression :math:`B` is exactly
        the same expression as the expression :math:`C`.
        """
        valid = self.valid and other.valid and self.rhs == other.lhs
        return MonoidEquation(self.lhs, other.rhs, valid)

class MonoidEqualityAlgebra(Monoid):
    r"""The "monoid equality algebra"

    Any instance of ``MonoidEqualityAlgebra`` is the "monoid" whose elements are
    equations of monoid expressions.

    This is a "fake monoid." In other words, this class is a subclass of
    :class:`Monoid`, and it implements all of the members of ``Monoid``
    (including ``assoc``, which is supposed to be the associativity law), but
    instances of this class are not actually monoids, because they don't satisfy
    any of the monoid laws. For example, given an equation :math:`A = B`,
    multiplying by ``id`` on the left will produce the equation :math:`e A = e
    B` instead of giving back :math:`A = B`.

    (actually, it doesn't implement ``left_id`` and ``right_id`` yet, but those
    will be pretty easy to add)

    I think that this "monoid" is actually a monoidal category. Objects are
    monoid expressions (:class:`MonoidExpr`\s), and morphisms are assertions
    that one expression (the domain or LHS) is equivalent to another expression
    (the codomain or RHS). The :meth:`id_` method produces (the identity
    morphism for) the monoidal unit; the :meth:`mop_` method is the monoidal
    product; the :meth:`assoc` method is a version of the associator; and the
    :meth:`left_id` and :meth:`right_id` methods are the left and right unitors.
    """
    T = MonoidEquation

    def id_(self) -> MonoidEquation:
        return MonoidEquation.id()

    def mop_(self, a: MonoidEquation, b: MonoidEquation) -> MonoidEquation:
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
    relations = [(Mop(Literal(True), Literal(True)), Literal(True))]

    def id_(self) -> bool:
        return False

    def mop_(self, a: bool, b: bool):
        return a | b

bool_disjunction = BoolDisjunction()

class BoolXor(CommutativeMonoid):
    """
    The monoid of booleans under exclusive disjunction (XOR)

    .. attribute:: T = bool

    .. attribute:: generators = [True]
    .. attribute:: relations = [True | True == False]
    """

    T = bool

    generators = [True]
    relations = [(Mop(Literal(True), Literal(True)), Id())]

    def id_(self) -> bool:
        return False

    def mop_(self, a: bool, b: bool):
        return a ^ b

bool_xor = BoolXor()

class TrivialMonoid(Monoid):
    T = None

    generators = []

    def id_(self) -> None:
        return None

    def mop_(self, x: None, y: None) -> None:
        return None

trivial_monoid = TrivialMonoid()

@MonoidHomomorphism
def int_addition_to_bool_disjunction(i: int_addition) -> bool_disjunction:
    # TODO: change this from int_addition to nat_addition, because this doesn't
    # work on negative integers!
    return i != 0

@MonoidHomomorphism
def int_addition_to_bool_xor(i: int_addition) -> bool_xor:
    return i % 2 == 1

def trivial_to(m: Monoid) -> MonoidHomomorphism:
    # TODO: this should be trivial_monoid, not TrivialMonoid
    @mk_monoid_homomorphism(TrivialMonoid, m)
    def hom(a: TrivialMonoid) -> m:
        return m.id_()

    return hom
