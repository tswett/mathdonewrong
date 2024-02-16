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

from mathdonewrong.primitive_recursive.primrec_exprs_typed import Comp, Succ, Zero

def test_succ():
    assert Succ().typecheck() == Callable[[int], int]
    assert Succ().to_func()(0) == 1
    assert Succ().to_func()(1) == 2
    assert Succ().to_func()(2) == 3

def test_zero():
    assert Zero().typecheck() == Callable[[], int]
    assert Zero().to_func()() == 0

def test_comp():
    # Note: this is left-to-right composition

    assert Comp(Zero(), Succ()).typecheck() == Callable[[], int]
    assert Comp(Zero(), Succ()).to_func()() == 1

    assert Comp(Succ(), Succ()).typecheck() == Callable[[int], int]
    assert Comp(Succ(), Succ()).to_func()(0) == 2

    assert Comp(Succ(), Comp(Succ(), Succ())).to_func()(0) == 3

    assert Comp(Succ(), Zero()).typecheck() == None
