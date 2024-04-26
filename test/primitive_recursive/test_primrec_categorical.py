# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.primitive_recursive.primrec_categorical import (
    Nat, Pair, Succ, Unit, Zero)

unit = Unit()
nat = Nat()
zero = Zero()
succ = Succ()

def test_Unit():
    assert unit.domain() == unit
    assert unit.codomain() == unit
    assert unit.lhs() == unit
    assert unit.rhs() == unit
    assert unit.apply(None) == None

def test_Nat():
    assert nat.domain() == nat
    assert nat.codomain() == nat
    assert nat.lhs() == nat
    assert nat.rhs() == nat
    assert nat.apply(2) == 2
    assert nat.apply(3) == 3

def test_Zero():
    assert zero.domain() == Unit()
    assert zero.codomain() == Nat()
    assert zero.lhs() == zero
    assert zero.rhs() == zero
    assert zero.apply(None) == 0

def test_Succ():
    assert succ.domain() == Nat()
    assert succ.codomain() == Nat()
    assert succ.lhs() == succ
    assert succ.rhs() == succ
    assert succ.apply(2) == 3
    assert succ.apply(3) == 4

def test_Pair():
    assert Pair(nat, nat).domain() == Pair(nat, nat)
    assert Pair(zero, succ).domain() == Pair(unit, nat)
    assert Pair(zero, succ).codomain() == Pair(nat, nat)
    assert Pair(succ, Pair(succ, succ)).codomain() == Pair(nat, Pair(nat, nat))

    assert Pair(zero, succ).apply((None, 5)) == (0, 6)
