# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

r"""
The primitive recursive category

This module is intended to represent the 2-category of primitive recursive
types, functions, and equality proofs. This 2-category consists of

- 0-cells (objects), which represent types such as :math:`\mathbb{N} \times
  \mathbb{N}`,
- 1-cells (arrows), which represent primitive recursive functions from one type
  to another, and
- 2-cells, which represent proofs that one primitive recursive function is equal
  to another.

We actually don't distinguish between the three types of cells. Every 0-cell
:math:`A` is also the 1-cell representing the identity function :math:`A \to A`,
and every 1-cell :math:`f` is also the 2-cell representing the proof by
reflexivity that :math:`f = f`. Likewise, every operation that can be performed
on 0-cells can also be performed on 1-cells, and every operation on 1-cells can
be performed on 2-cells.

All of the major classes here are (or at least should be) subclasses of
:class:`~mathdonewrong.expressions.Expression`. Usually, we define behavior in
algebras, not in expressions, but for this case, it seemed to make more sense to
take the object-oriented approach and define the behaviors right in the
expression classes. This will probably come back to bite us, but we'll cross
that set of teeth when we get to it.

Core classes
============

.. autoclass:: PrimRecCell
   :members:

.. autoclass:: Unit

.. autoclass:: Nat

.. autoclass:: Zero

.. autoclass:: Succ

.. autoclass:: Pair

List of members
===============
"""

from __future__ import annotations

from mathdonewrong.expressions import NamedOper

class PrimRecCell:
    """
    Primitive recursive cell
    
    A primitive recursive 0-cell (type), 1-cell (function), or 2-cell (equality
    proof).
    """

    def domain(self) -> PrimRecCell:
        """
        Domain of a function
        
        Get the domain of this cell. A 1-cell is a function, so its domain is
        just the domain of the function. The domain of a 0-cell is the 0-cell
        itself. The domain of a 2-cell is the domain of its LHS or RHS
        (presumably, both have the same domain).
        """
        raise NotImplementedError

    def codomain(self) -> PrimRecCell:
        """
        Codomain of a function
        
        Get the codomain of this cell. See :meth:`domain` for details.
        """
        raise NotImplementedError

    def lhs(self) -> PrimRecCell:
        """
        Left-hand side of an equation
        
        Get the left-hand side of this cell. A 2-cell is an equation, so its
        left-hand side is just the left-hand side of the equation. The left-hand
        side of a 0-cell or 1-cell is that 0-cell or 1-cell itself.
        """
        raise NotImplementedError

    def rhs(self) -> PrimRecCell:
        """
        Right-hand side of an equation
        
        Get the right-hand side of this cell. See :meth:`lhs` for details.
        """
        raise NotImplementedError

    def apply(self, x: domain) -> codomain:
        """
        Apply (evaluate) a function
        
        Evaluate the application of this cell to the given parameter value. A
        1-cell is a function, so applying it just means applying the function.
        Applying a 0-cell to any value returns the same value (in other words, a
        0-cell behaves as the identity function). Applying a 2-cell gives the
        same result as applying its left-hand side (which, presumably, is
        equivalent to applying its right-hand side).
        """
        raise NotImplementedError

class PrimRec_1_Cell(PrimRecCell):
    def lhs(self):
        return self
    
    def rhs(self):
        return self

class PrimRec_0_Cell(PrimRec_1_Cell):
    def domain(self):
        return self

    def codomain(self):
        return self

class Unit(NamedOper, PrimRec_0_Cell):
    r"""
    The unit type
    
    The unit type, or type of 0-tuples, often denoted :math:`\mathbf{1}`.

    The sole value of the unit type is represented as the Python value ``None``.
    """

    def __init__(self):
        super().__init__()

    def apply(self, x: None) -> None:
        return x

class Nat(NamedOper, PrimRec_0_Cell):
    """The natural numbers"""

    def __init__(self):
        super().__init__()

    def apply(self, x: int) -> int:
        return x

class Zero(NamedOper, PrimRec_1_Cell):
    """The natural number 0"""

    def __init__(self):
        super().__init__()

    def domain(self):
        return Unit()

    def codomain(self):
        return Nat()

    def apply(self, x: None) -> int:
        return 0

class Succ(NamedOper, PrimRec_1_Cell):
    """The successor function on natural numbers"""

    def __init__(self):
        super().__init__()

    def domain(self):
        return Nat()

    def codomain(self):
        return Nat()

    def apply(self, x: int) -> int:
        return x + 1

class Pair(NamedOper, PrimRecCell):
    r"""
    The cartesian product

    For 0-cells :math:`A` and :math:`B`, this is the cartesian product :math:`A
    \times B`. For 1-cells :math:`f` and :math:`g`, this is the function
    :math:`(f \times g)` defined by :math:`(f \times g)(x, y) = (f(x), g(y))`.
    For 2-cells asserting that :math:`f = h` and :math:`g = i`, this is the
    2-cell asserting that :math:`f \times g = h \times i`.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right
        super().__init__(left, right)

    def domain(self):
        return Pair(self.left.domain(), self.right.domain())

    def codomain(self):
        return Pair(self.left.codomain(), self.right.codomain())

    def apply(self, x: tuple[left.domain, right.domain]) -> tuple[left.codomain, right.codomain]:
        xleft, xright = x
        return (self.left.apply(xleft), self.right.apply(xright))
