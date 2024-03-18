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
Varieties of algebras

This module defines "varieties of algebras." A `variety of algebras` is a formal
description of some kind of algebraic structure. For example, there is a variety
which defines what a monoid is (the "variety of monoids"), a variety which
defines what a ring is, and so forth.

.. autoclass:: mathdonewrong.varieties.Variety
"""

from dataclasses import dataclass

from mathdonewrong.expressions import Expression

@dataclass
class Operator:
    name: str

@dataclass
class Relation:
    lhs: Expression
    rhs: Expression

@dataclass
class Variety:
    """
    Variety of algebras

    A ``Variety`` is a formal description of some kind of algebraic structure.
    As of this writing, a ``Variety`` consists of a list of
    :class:`~mathdonewrong.varieties.Operator`\s and a list of
    :class:`~mathdonewrong.varieties.Relation`\s.

    As an example, here is what the ``Variety`` of semigroups may look like::

       variety_of_semigroups = Variety(
           operators=[Operator('Mult')],
           relations=[Relation(
               lhs=Oper('Mult', Var('x'), Oper('Mult', Var('y'), Var('z'))),
               rhs=Oper('Mult', Oper('Mult', Var('x'), Var('y')), Var('z'))
           )]
       )

    The property ``variety`` of :class:`~mathdonewrong.algebras.AlgebraClass` is
    intended to automatically extract a ``Variety`` object from a class which
    defines a variety of algebras. The goal is that it should almost never be
    necessary to define a ``Variety`` object explicitly; we should be able to
    just write a variety as a class definition and then access its ``variety``
    object.

    Future plans for ``Variety``:

    * Allow listing the *sorts* that a variety has (for example, a graph has two
      sorts: vertices and edges).
    * Allow specifying the domain and codomain of each operator.
    * Allow explicitly specifying the context of each relation.
    """
    operators: list[Operator]
    relations: list[Relation]

    def __init__(self, operators=None, relations=None):
        self.operators = operators or []
        self.relations = relations or []

    def __str__(self) -> str:
        head =             'variety:'
        operators_head =   '    operators:'
        operators_body = [f'        {oper.name}' for oper in self.operators]
        relations_head =   '    relations:'
        relations_body = [f'        {rel.lhs} = {rel.rhs}' for rel in self.relations]

        result = '\n'.join([head, operators_head] + operators_body + [relations_head] + relations_body)

        return result
