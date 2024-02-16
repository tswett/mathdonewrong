# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from typing import Callable

import pytest

from mathdonewrong.primitive_recursive.primrec_exprs_typed import Comp, Const, Fork, Select, Succ, Zero

def test_succ():
    assert Succ().typecheck() == Callable[[int], int]
    assert Succ().to_func()(0) == 1
    assert Succ().to_func()(1) == 2
    assert Succ().to_func()(2) == 3

def test_zero():
    assert Zero().typecheck() == Callable[[], int]
    assert Zero().to_func()() == 0

def test_fork():
    assert Fork(Zero(), Zero()).typecheck() == Callable[[], tuple[int, int]]
    assert Fork(Zero(), Zero()).to_func()() == (0, 0)

    assert Fork(Succ(), Succ()).typecheck() == Callable[[int], tuple[int, int]]
    assert Fork(Succ(), Succ()).to_func()(0) == (1, 1)
    assert Fork(Succ(), Succ()).to_func()(1) == (2, 2)

    assert Fork(Succ(), Fork(Succ(), Succ())).typecheck() == Callable[[int], tuple[int, tuple[int, int]]]
    assert Fork(Succ(), Fork(Succ(), Succ())).to_func()(0) == (1, (1, 1))
    assert Fork(Succ(), Fork(Succ(), Succ())).to_func()(1) == (2, (2, 2))

    assert Fork(Zero(), Succ()).typecheck() == None

def test_select():
    assert repr(Select(0, int, tuple[int, int])) == "Select(0, <class 'int'>, tuple[int, int])"

    assert Select(0, int, tuple[int, int]).typecheck() == Callable[[tuple[int, tuple[int, int]]], int]
    assert Select(0, int, tuple[int, int]).to_func()((0, (1, 2))) == 0

    assert Select(1, int, tuple[int, int]).typecheck() == Callable[[tuple[int, tuple[int, int]]], tuple[int, int]]
    assert Select(1, int, tuple[int, int]).to_func()((0, (1, 2))) == (1, 2)

def test_comp():
    # Note: this is left-to-right composition

    assert Comp(Zero(), Succ()).typecheck() == Callable[[], int]
    assert Comp(Zero(), Succ()).to_func()() == 1

    assert Comp(Succ(), Succ()).typecheck() == Callable[[int], int]
    assert Comp(Succ(), Succ()).to_func()(0) == 2

    assert Comp(Succ(), Comp(Succ(), Succ())).to_func()(0) == 3

    assert Comp(Succ(), Zero()).typecheck() == None

    assert Comp(Succ(), Fork(Succ(), Succ())).typecheck() == Callable[[int], tuple[int, int]]
    assert Comp(Succ(), Fork(Succ(), Succ())).to_func()(0) == (2, 2)
    assert Comp(Succ(), Fork(Succ(), Succ())).to_func()(1) == (3, 3)

def test_const():
    assert repr(Const(None, int, 10)) == "Const(None, <class 'int'>, 10)"

    assert Const(None, int, 10).typecheck() == Callable[[None], int]
    assert Const(None, int, 10).to_func()(None) == 10

    assert Const(int, None, None).typecheck() == Callable[[int], None]
    assert Const(int, None, None).to_func()(18) == None

@pytest.mark.skip("Not implemented yet")
def test_natrecurse():
    # Double-plus-ten

    base = Const(None, int, 10)
    assert base.typecheck() == Callable[[None], int]

    step = Select(0, None, int)
    assert step.typecheck() == Callable[[tuple[None, int]], int]

    double_plus_ten = NatRecurse(base, step)
    assert double_plus_ten.typecheck() == Callable[[tuple[None, int]], int]

    assert double_plus_ten.to_func()((None, 0)) == 10
    assert double_plus_ten.to_func()((None, 1)) == 12
    assert double_plus_ten.to_func()((None, 2)) == 14
