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
from mathdonewrong.equality.equality_exprs import EqSymm, EqTrans
from mathdonewrong.expressions import Expression
from mathdonewrong.monoidlike.monoids import (
    Assoc, Id, MonLiteral, Mop, MonVar, Monoid, MonoidEqualityAlgebra,
    MonoidEquation, MonoidHomomorphism,
    bool_disjunction, bool_xor, int_addition,
    int_addition_to_bool_disjunction, int_addition_to_bool_xor,
    int_multiplication, int_scale, string_monoid,
    trivial_monoid, trivial_to, tuple_monoid
)
from mathdonewrong.varieties import Operator, Relation



# Test various monoid machinery

def test_MonOper_requires_two_operands():
    with pytest.raises(TypeError):
        Mop(1)
    with pytest.raises(TypeError):
        Mop(1, 2, 3)

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

def test_trivial_to_homomorphism():
    assert trivial_to(int_addition)(None) == 0
    assert trivial_to(string_monoid)(None) == ''

def test_monoid_variety_is_correct():
    a, b, c = MonVar('a'), MonVar('b'), MonVar('c')

    vty = Monoid.variety

    assert vty.operators == [
        Operator('Id'),
        Operator('Mop'),
    ]

    assert vty.relations == [
        Relation(Id() * a, a),
        Relation(a * Id(), a),
        Relation((a * b) * c, a * (b * c)),
    ]

def test_homomorphism_on_generators():
    assert int_addition_to_bool_disjunction.on_generators() == [(1, True)]
    assert int_addition_to_bool_xor.on_generators() == [(1, True)]
    assert trivial_to(int_addition).on_generators() == []
    assert int_scale(3).on_generators() == [(1, 3)]



# Test various particular monoids

L = MonLiteral

def test_int_addition():
    assert int_addition.mop() == 0
    assert int_addition.mop(5) == 5
    assert int_addition.mop(5, 7) == 12
    assert int_addition.mop(5, 7, 3) == 15

def test_int_multiplication():
    assert int_multiplication.mop() == 1
    assert int_multiplication.mop(5) == 5
    assert int_multiplication.mop(5, 7) == 35
    assert int_multiplication.mop(5, 7, 3) == 105

def test_string_monoid():
    assert string_monoid.mop() == ''
    assert string_monoid.mop('boots') == 'boots'
    assert string_monoid.mop('boots', ' and') == 'boots and'
    assert string_monoid.mop('boots', ' and', ' cats') == 'boots and cats'

def test_tuple_monoid():
    assert tuple_monoid.mop() == ()
    assert tuple_monoid.mop((1, 'hello')) == (1, 'hello')
    assert tuple_monoid.mop((1, 'hello'), (), ('world',)) == (1, 'hello', 'world')

def test_evaluation():
    assert (L(5) * L(7) * L(3)).evaluate_in(int_addition, {}) == 15
    assert (L(5) * L(7) * L(3)).evaluate_in(int_multiplication, {}) == 105
    assert (L('boots') * L(' and') * L(' cats')).evaluate_in(string_monoid, {}) == 'boots and cats'
    assert (L((1, 'hello')) * L(()) * L(('world',))).evaluate_in(tuple_monoid, {}) == (1, 'hello', 'world')

def test_trivial_monoid():
    assert Id().evaluate_in(trivial_monoid) == None
    assert (Id() * Id()).evaluate_in(trivial_monoid) == None

def test_bool_disjunction():
    assert Id().evaluate_in(bool_disjunction) == False
    assert (Id() * Id()).evaluate_in(bool_disjunction) == False
    assert (Id() * L(True)).evaluate_in(bool_disjunction) == True
    assert (L(True) * Id()).evaluate_in(bool_disjunction) == True
    assert (L(True) * L(True)).evaluate_in(bool_disjunction) == True

def test_bool_xor():
    assert Id().evaluate_in(bool_xor) == False
    assert (Id() * Id()).evaluate_in(bool_xor) == False
    assert (Id() * L(True)).evaluate_in(bool_xor) == True
    assert (L(True) * Id()).evaluate_in(bool_xor) == True
    assert (L(True) * L(True)).evaluate_in(bool_xor) == False

def test_int_addition_to_bool_disjunction():
    h = int_addition_to_bool_disjunction
    assert h(0) == False
    assert h(1) == True
    assert h(2) == True

def test_int_addition_to_bool_xor():
    h = int_addition_to_bool_xor
    assert h(0) == False
    assert h(1) == True
    assert h(2) == False
    assert h(3) == True



# Test the monoid equality algebra

eq = MonoidEqualityAlgebra()
x, y, z = MonVar('x'), MonVar('y'), MonVar('z')
context = {
    'x': MonoidEquation.refl(x),
    'y': MonoidEquation.refl(y),
    'z': MonoidEquation.refl(z)
}

def test_equality_algebra_reflexivity():
    exprs = [
        Id(),
        x,
        x * y,
        (x * y) * z,
        x * (y * z),
    ]

    for expr in exprs:
        equation = expr.evaluate_in(eq, context)
        assert equation.valid
        assert equation.lhs == expr
        assert equation.rhs == expr

def test_equality_algebra_associativity():
    expr = Assoc(x, y, z)

    equation = expr.evaluate_in(eq, context)
    assert equation.valid
    assert equation.lhs == (x * y) * z
    assert equation.rhs == x * (y * z)

def test_equality_algebra_associativity_complex():
    expr = y * Assoc(x * z, x, y)

    equation = expr.evaluate_in(eq, context)
    assert equation.valid
    assert equation.lhs == y * (((x * z) * x) * y)
    assert equation.rhs == y * ((x * z) * (x * y))

def test_equality_algebra_associativity_very_complex():
    expr = x * Assoc(y * x, z, Assoc(z, y, z))

    equation = expr.evaluate_in(eq, context)
    assert equation.valid
    assert equation.lhs == x * (((y * x) * z) * ((z * y) * z))
    assert equation.rhs == x * ((y * x) * (z * (z * (y * z))))

def test_equality_algebra_symmetry():
    expr = EqSymm(Assoc(x, y, z))

    equation = expr.evaluate_in(eq, context)
    assert equation.valid
    assert equation.lhs == x * (y * z)
    assert equation.rhs == (x * y) * z

def test_equality_algebra_transitivity_valid():
    expr = EqTrans(Assoc(x * z, x, y), Assoc(x, z, x * y))

    equation = expr.evaluate_in(eq, context)
    assert equation.valid
    assert equation.lhs == ((x * z) * x) * y
    assert equation.rhs == x * (z * (x * y))

def test_equality_algebra_transitivity_invalid():
    expr = EqTrans(Assoc(x, z, x * y), Assoc(x * z, x, y))

    equation = expr.evaluate_in(eq, context)
    assert not equation.valid

def test_equality_algebra_transitivity_of_reflexivity_valid():
    expr = EqTrans(x, x)

    equation = expr.evaluate_in(eq, context)
    assert equation.valid
    assert equation.lhs == x
    assert equation.rhs == x

def test_equality_algebra_transitivity_of_reflexivity_invalid():
    expr = EqTrans(x, y)

    equation = expr.evaluate_in(eq, context)
    assert not equation.valid

def test_equality_algebra_transitivity_of_reflexivity_invalid_nested():
    exprs = [EqTrans(EqTrans(x, y), y), EqTrans(x, EqTrans(x, y))]

    for expr in exprs:
        equation = expr.evaluate_in(eq, context)
        assert not equation.valid

def test_equality_algebra_associativity_of_invalid():
    exprs = [
        Assoc(EqTrans(x, y), y, z),
        Assoc(x, EqTrans(y, z), z),
        Assoc(x, y, EqTrans(z, x))
    ]

    for expr in exprs:
        equation = expr.evaluate_in(eq, context)
        assert not equation.valid

def test_equality_algebra_symmetry_of_reflexivity():
    expr = EqSymm(x)

    equation = expr.evaluate_in(eq, context)
    assert equation.valid
    assert equation.lhs == x
    assert equation.rhs == x

def test_equality_algebra_symmetry_of_invalid():
    expr = EqSymm(EqTrans(x, y))

    equation = expr.evaluate_in(eq, context)
    assert not equation.valid



if __name__ == '__main__':
    pytest.main([__file__])
