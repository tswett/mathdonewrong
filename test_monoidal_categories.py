# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.monoidal_categories import Compose, Id, Var
from mathdonewrong.monoidal_categories.category_of_functions import CategoryOfFunctions, tfunction

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
