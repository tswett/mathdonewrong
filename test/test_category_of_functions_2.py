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
from mathdonewrong.monoidal_categories.category_of_functions_2 import CategoryOfUnaryFunctions

cat = CategoryOfUnaryFunctions()

def test_id():
    expr = Id(Var('A'))

    func = expr.evaluate_in(cat, {'A': int})
    assert func(42) == 42

def test_category_of_functions_compose():
    expr = Compose(Var('f'), Var('g'))

    func = expr.evaluate_in(cat, {'f': str, 'g': len})
    assert func(1000) == 4
