# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.expressions import NamedOper

class Compose(NamedOper):
    r""""End-to-end" composition

    This operation corresponds to composition of morphisms in a category.
    Generally, if ``f`` is something of type :math:`A \to B` and ``g`` is
    something of type :math:`B \to C`, then ``Compose(f, g)`` is something of
    type :math:`A \to C`.

    A good Python operator to use for ``Compose`` may be the ``@`` operator, since
    that operator traditionally represents matrix multiplication, and matrix
    multiplication can be thought of as a kind of composition.

    Note that, at least for functions, this is left-to-right composition—the
    first function goes first and the second function goes second.

    "Compose" is one of many plausible names for the sole operator of a monoid.
    """

class Stack(NamedOper):
    r""""Side-by-side" composition
    
    This operation corresponds to the monoidal product in a monoidal category.
    Generally, if ``f`` is something of type :math:`A \to C` and ``g`` is something
    of type :math:`B \to D`, then ``Stack(f, g)`` is something of type :math:`(A
    \otimes B) \to (C \otimes D)`.

    "Stack" is one of many plausible names for the sole operator of a monoid.
    """

class Plus(NamedOper):
    r"""Addition

    This operation corresponds to addition in a ring.

    The obvious Python operator to use for ``Plus`` is the ``+`` operator.

    "Plus" is one of many plausible names for the sole operator of a monoid.
    """

class Zero(NamedOper):
    r"""Additive identity

    This operation corresponds to the additive identity in a ring.
    """

class Times(NamedOper):
    r"""Multiplication

    This operation corresponds to multiplication in a ring.

    The obvious Python operator to use for ``Times`` is the ``*`` operator.

    "Times" is one of many plausible names for the sole operator of a monoid.
    """

class One(NamedOper):
    r"""Multiplicative identity

    This operation corresponds to the multiplicative identity in a ring.
    """

class Min(NamedOper):
    r"""Minimum, meet, conjunction, intersection
    
    This operation corresponds to the minimum or meet operation in a lattice, or
    the conjunction operation in a Boolean algebra.

    The best Python operator to use for ``Min`` is probably the ``&`` operator;
    booleans and sets in Python both use the ``&`` operator that way. It's worth
    noting that ints in Python use ``&`` for bitwise AND, not for the minimum.

    It is generally impossible to use Python's ``and`` operator to represent this
    operator, since Python doesn't give us very much flexibility in customizing
    what the ``and`` operator does.

    "Min" is one of many plausible names for the sole operator of a monoid.
    """

class Top(NamedOper):
    r"""Greatest element, "true," universal set

    This operation corresponds to the greatest element in a lattice, or 1 in a
    Boolean algebra. This may be the identity element for the "Min" operator.
    """

class Max(NamedOper):
    r"""Maximum, join, disjunction, union
    
    This operation corresponds to the maximum or join operation in a lattice, or
    the disjunction operation in a Boolean algebra.

    The best Python operator to use for ``Max`` is probably the ``|`` operator;
    booleans and sets in Python both use the ``|`` operator that way. It's worth
    noting that ints in Python use ``|`` for bitwise OR, not for the maximum.

    It is generally impossible to use Python's ``or`` operator to represent this
    operator, since Python doesn't give us very much flexibility in customizing
    what the ``or`` operator does.

    "Max" is one of many plausible names for the sole operator of a monoid.
    """

class Bottom(NamedOper):
    r"""Least element, "false," empty set
    
    This operation corresponds to the least element in a lattice, or 0 in a
    Boolean algebra. This may be the identity element for the "Max" operator.
    """
