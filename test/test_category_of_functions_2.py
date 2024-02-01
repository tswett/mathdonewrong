# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.monoidal_categories import AssocLeft, AssocRight, Braid, BraidInv, Compose, Curry, CurryInv, Diagonal, Drop, Id, Into, Stack, Unit, UnitRight, UnitRightInv, UnitLeft, UnitLeftInv, Var
from mathdonewrong.monoidal_categories.category_of_functions_2 import CategoryOfUnaryFunctions

cat = CategoryOfUnaryFunctions()

# Category operations

def test_id():
    expr = Id(Var('A'))

    func = expr.evaluate_in(cat, {'A': int})
    assert func(42) == 42

def test_compose():
    expr = Compose(Var('f'), Var('g'))

    func = expr.evaluate_in(cat, {'f': lambda x: x * 2, 'g': lambda x: x + 100})
    assert func(1) == 102

# Monoidal category operations

def test_stack():
    expr = Stack(Var('f'), Var('g'))

    func = expr.evaluate_in(cat, {'f': lambda x: x * 2, 'g': lambda x: x + ' and dogs'})
    assert func((10, 'cats')) == (20, 'cats and dogs')

def test_assoc_right():
    expr = AssocRight(Var('A'), Var('B'), Var('C'))

    func = expr.evaluate_in(cat, {'A': int, 'B': str, 'C': float})
    assert func(((80, 'carrot'), 1.2)) == ((80, ('carrot', 1.2)))

def test_assoc_left():
    expr = AssocLeft(Var('A'), Var('B'), Var('C'))

    func = expr.evaluate_in(cat, {'A': int, 'B': str, 'C': float})
    assert func((80, ('carrot', 1.2))) == (((80, 'carrot'), 1.2))

def test_functions_unit():
    expr = Unit()

    assert expr.evaluate_in(cat, {}) == None

def test_functions_unit_left():
    expr = UnitLeft(Var('A'))

    func = expr.evaluate_in(cat, {'A': str})
    assert func('pizza') == (None, 'pizza')

def test_functions_unit_right():
    expr = UnitRight(Var('A'))

    func = expr.evaluate_in(cat, {'A': str})
    assert func('pie') == ('pie', None)

def test_functions_unit_left_inv():
    expr = UnitLeftInv(Var('A'))

    func = expr.evaluate_in(cat, {'A': str})
    assert func((None, 'cake')) == 'cake'

def test_functions_unit_right_inv():
    expr = UnitRightInv(Var('A'))

    func = expr.evaluate_in(cat, {'A': str})
    assert func(('pasta', None)) == 'pasta'

# Braided monoidal category operations

def test_braid():
    expr = Braid(Var('A'), Var('B'))

    func = expr.evaluate_in(cat, {'A': str, 'B': int})
    assert func(('kittens', 83)) == (83, 'kittens')

def test_braid_inv():
    expr = BraidInv(Var('A'), Var('B'))

    func = expr.evaluate_in(cat, {'A': str, 'B': int})
    assert func((101, 'dalmatians')) == ('dalmatians', 101)

# Cartesian monoidal category operations

def test_drop():
    expr = Drop(Var('A'))

    func = expr.evaluate_in(cat, {'A': str})
    assert func('barrels') == None

def test_diagonal():
    expr = Diagonal(Var('A'))

    func = expr.evaluate_in(cat, {'A': str})
    assert func('boxes') == ('boxes', 'boxes')

# Closed monoidal category operations

def test_into():
    expr = Into(Var('A'), Var('f'))

    func = expr.evaluate_in(cat, {'A': int, 'f': lambda x: x + 1000})
    assert func(lambda x: x * 3)(2) == 1006

def test_curry():
    expr = Curry(Var('f'))

    func = expr.evaluate_in(cat, {'f': lambda x, y: x * 100 + y})
    assert func(2)(3) == 203

def test_curry_inv():
    expr = CurryInv(Var('f'))

    func = expr.evaluate_in(cat, {'f': lambda x: lambda y: x * 100 + y})
    assert func((2, 3)) == 203
