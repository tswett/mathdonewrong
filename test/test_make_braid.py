# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.monoidal_categories.make_braid import make_braid
from mathdonewrong.monoidal_categories.monoidalexpr import Braid, Drop, Id, Stack, Unit, Var

def test_make_braid_nothing_to_nothing():
    expr = make_braid(None, None)
    assert expr == Id(Unit())

def test_make_braid_var_to_same_var():
    expr = make_braid('x', 'x')
    assert expr == Id(Var('x'))

    expr = make_braid('y', 'y')
    assert expr == Id(Var('y'))

def test_make_braid_pair_to_same_pair():
    expr = make_braid(('x', 'y'), ('x', 'y'))
    assert expr == Id(Stack(Var('x'), Var('y')))

def test_make_braid_var_to_nothing():
    expr = make_braid('x', None)
    assert expr == Drop(Var('x'))

def test_make_braid_pair_swap():
    expr = make_braid(('x', 'y'), ('y', 'x'))
    assert expr == Braid(Var('x'), Var('y'))
