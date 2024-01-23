# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

import pytest

from mathdonewrong.boolexpr import And, F, Not, Or, T, Var
from mathdonewrong.code_to_boolexpr import code_to_boolexpr

def test_from_code_constant():
    assert code_to_boolexpr(lambda x, y: True) == T
    assert code_to_boolexpr(lambda x, y: False) == F

def test_from_code_variable():
    assert code_to_boolexpr(lambda x, y: x) == Var('x')
    assert code_to_boolexpr(lambda x, y: y) == Var('y')

def test_from_code_binary_operators():
    assert code_to_boolexpr(lambda x, y: x & y) == Var('x') & Var('y')
    assert code_to_boolexpr(lambda x, y: x | y) == Var('x') | Var('y')

@pytest.mark.skip(reason="This is going to be pretty complicated to implement.")
def test_from_code_short_circuiting_operators():
    assert code_to_boolexpr(lambda x, y: x and y) == Var('x') & Var('y')
    assert code_to_boolexpr(lambda x, y: x or y) == Var('x') | Var('y')

def test_from_code_unary_operators():
    assert code_to_boolexpr(lambda x, y: ~x) == ~Var('x')

def test_from_code_complex_expression():
    assert code_to_boolexpr(lambda x, y: x & ~y | ~x & y) == (Var('x') & ~Var('y')) | (~Var('x') & Var('y'))

if __name__ == '__main__':
    pytest.main([__file__])
