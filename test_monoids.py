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
from mathdonewrong.monoids import MonoidHomomorphism, int_addition, int_multiplication, int_scale, string_monoid, tuple_monoid

def test_int_addition():
    assert int_addition.oper() == 0
    assert int_addition.oper(5) == 5
    assert int_addition.oper(5, 7) == 12
    assert int_addition.oper(5, 7, 3) == 15

def test_int_multiplication():
    assert int_multiplication.oper() == 1
    assert int_multiplication.oper(5) == 5
    assert int_multiplication.oper(5, 7) == 35
    assert int_multiplication.oper(5, 7, 3) == 105

def test_string_monoid():
    assert string_monoid.oper() == ''
    assert string_monoid.oper('boots') == 'boots'
    assert string_monoid.oper('boots', ' and') == 'boots and'
    assert string_monoid.oper('boots', ' and', ' cats') == 'boots and cats'

def test_tuple_monoid():
    assert tuple_monoid.oper() == ()
    assert tuple_monoid.oper((1, 'hello')) == (1, 'hello')
    assert tuple_monoid.oper((1, 'hello'), (), ('world',)) == (1, 'hello', 'world')

def test_a_homomorphism():
    @MonoidHomomorphism
    def int_to_unary(x: int_addition) -> string_monoid:
        return '.' * x

    assert int_to_unary.domain == int_addition
    assert int_to_unary.codomain == string_monoid

    assert int_to_unary(6) == '......'

def test_int_scale_homomorphism():
    for x in [1, 5, 0, -1]:
        hom = int_scale(x)

        assert hom.domain == int_addition
        assert hom.codomain == int_addition

        for y in [1, 5, 0, -1]:
            assert hom(y) == x * y

if __name__ == '__main__':
    pytest.main([__file__])
