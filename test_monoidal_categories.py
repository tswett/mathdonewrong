# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.monoidal_categories import AssocLeft, AssocRight, Compose, Id, Stack, Unit, Var
from mathdonewrong.monoidal_categories.category_of_functions import CategoryOfFunctions, tfunction
from mathdonewrong.monoidal_categories.monoidalexpr import Braid, BraidInv, Diagonal, Drop, UnitLeft, UnitLeftInv, UnitRight, UnitRightInv

cat = CategoryOfFunctions()

@tfunction(str, int)
def length(s: str) -> tuple[int]:
    return len(s),

@tfunction(int, str)
def announce_number(n: int) -> tuple[str]:
    return f"The number is {n}.",

@tfunction(str, (str, str))
def split_at_first_space(s: str) -> tuple[str, str]:
    x, y = s.split(' ', 1)
    return x, y

@tfunction((str, str), str)
def join_backwards(x: str, y: str) -> tuple[str]:
    return y + ' ' + x,

@tfunction(int, ())
def ignore_number(n: int) -> tuple[()]:
    return ()

@tfunction((), str)
def return_michigan() -> tuple[str]:
    return 'Michigan',

def test_category_of_functions_id():
    expr = Id(Var('A'))

    func = expr.evaluate_in(cat, {'A': ()})
    assert func() == ()

    func = expr.evaluate_in(cat, {'A': int})
    assert func(42) == (42,)

    func = expr.evaluate_in(cat, {'A': (int, str)})
    assert func(42, 'hello') == (42, 'hello')

def test_category_of_functions_compose():
    expr = Compose(Var('f'), Var('g'))

    func = expr.evaluate_in(cat, {'f': length, 'g': announce_number})
    assert func('hello') == ("The number is 5.",)

    func = expr.evaluate_in(cat, {'f': split_at_first_space, 'g': join_backwards})
    assert func('what do we have here') == ('do we have here what',)

    func = expr.evaluate_in(cat, {'f': ignore_number, 'g': return_michigan})
    assert func(18) == ('Michigan',)

def test_category_of_functions_stack():
    expr = Stack(Var('f'), Var('g'))

    func = expr.evaluate_in(cat, {'f': join_backwards, 'g': join_backwards})
    assert func('this', 'that', 'these', 'those') == ('that this', 'those these')

def test_category_of_functions_assoc_right():
    expr = AssocRight(Var('A'), Var('B'), Var('C'))

    func = expr.evaluate_in(cat, {'A': int, 'B': str, 'C': float})
    assert func.domain == ((int, str), float)
    assert func.codomain == (int, (str, float))
    assert func(80, 'carrot', 1.2) == (80, 'carrot', 1.2)

def test_category_of_functions_assoc_left():
    expr = AssocLeft(Var('A'), Var('B'), Var('C'))

    func = expr.evaluate_in(cat, {'A': int, 'B': str, 'C': float})
    assert func.domain == (int, (str, float))
    assert func.codomain == ((int, str), float)
    assert func(80, 'carrot', 1.2) == (80, 'carrot', 1.2)

def test_category_of_functions_unit():
    expr = Unit()

    assert expr.evaluate_in(cat, {}) == ()

def test_category_of_functions_unit_left():
    expr = UnitLeft(Var('A'))

    func = expr.evaluate_in(cat, {'A': int})
    assert func.domain == int
    assert func.codomain == ((), int)
    assert func(42) == (42,)

def test_category_of_functions_unit_right():
    expr = UnitRight(Var('A'))

    func = expr.evaluate_in(cat, {'A': int})
    assert func.domain == int
    assert func.codomain == (int, ())
    assert func(42) == (42,)

def test_category_of_functions_unit_left_inv():
    expr = UnitLeftInv(Var('A'))

    func = expr.evaluate_in(cat, {'A': int})
    assert func.domain == ((), int)
    assert func.codomain == int
    assert func(42) == (42,)

def test_category_of_functions_unit_right_inv():
    expr = UnitRightInv(Var('A'))

    func = expr.evaluate_in(cat, {'A': int})
    assert func.domain == (int, ())
    assert func.codomain == int
    assert func(42) == (42,)

def test_category_of_functions_braid():
    expr = Braid(Var('A'), Var('B'))

    func = expr.evaluate_in(cat, {'A': (int, str), 'B': ((str, float), int)})
    assert func.domain == ((int, str), ((str, float), int))
    assert func.codomain == (((str, float), int), (int, str))
    assert func(42, 'carrot', 'apple', 1.2, 84) == ('apple', 1.2, 84, 42, 'carrot')

def test_category_of_functions_braid_inv():
    expr = BraidInv(Var('A'), Var('B'))

    func = expr.evaluate_in(cat, {'A': (int, str), 'B': ((str, float), int)})
    assert func.domain == (((str, float), int), (int, str))
    assert func.codomain == ((int, str), ((str, float), int))
    assert func('apple', 1.2, 84, 42, 'carrot') == (42, 'carrot', 'apple', 1.2, 84)

def test_category_of_functions_drop():
    expr = Drop(Var('A'))

    func = expr.evaluate_in(cat, {'A': (str, int)})
    assert func.domain == (str, int)
    assert func.codomain == ()
    assert func('ladybug', 90) == ()

def test_category_of_functions_diagonal():
    expr = Diagonal(Var('A'))

    func = expr.evaluate_in(cat, {'A': (int, float)})
    assert func.domain == (int, float)
    assert func.codomain == ((int, float), (int, float))
    assert func(28, 8.6) == (28, 8.6, 28, 8.6)
