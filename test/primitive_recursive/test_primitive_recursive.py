# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.expressions import Literal, Oper
from mathdonewrong.primitive_recursive.primrec_exprs import Comp, PConst, PrimRec, Proj, Stack, StandardPrimitiveRecursiveAlgebra, Succ

alg = StandardPrimitiveRecursiveAlgebra()

def test_pconst():
    assert PConst(0) == Oper('PConst', Literal(0))
    assert PConst(1) == Oper('PConst', Literal(1))
    assert repr(PConst(0)) == 'PConst(0)'
    assert repr(PConst(1)) == 'PConst(1)'

def test_proj():
    assert Proj(0) == Oper('Proj', Literal(0))
    assert Proj(1) == Oper('Proj', Literal(1))
    assert repr(Proj(0)) == 'Proj(0)'
    assert repr(Proj(1)) == 'Proj(1)'

def test_constant():
    assert PConst(0).evaluate_in(alg)() == 0
    assert PConst(1).evaluate_in(alg)() == 1
    assert PConst(2).evaluate_in(alg)() == 2
    assert PConst(3).evaluate_in(alg)() == 3

    assert PConst(4).evaluate_in(alg)(3) == 4

def test_successor():
    assert Succ().evaluate_in(alg)(0) == 1
    assert Succ().evaluate_in(alg)(1) == 2
    assert Succ().evaluate_in(alg)(2) == 3
    assert Succ().evaluate_in(alg)(3) == 4

def test_projection():
    assert Proj(0).evaluate_in(alg)(3) == 3

    assert Proj(0).evaluate_in(alg)(3, 1) == 3
    assert Proj(1).evaluate_in(alg)(3, 1) == 1

    assert Proj(0).evaluate_in(alg)(3, 1, 4) == 3
    assert Proj(1).evaluate_in(alg)(3, 1, 4) == 1
    assert Proj(2).evaluate_in(alg)(3, 1, 4) == 4

def test_stacking():
    assert Stack(Succ()).evaluate_in(alg)(10) == [11]

    assert Stack(Succ(), PConst(2)).evaluate_in(alg)(10) == [11, 2]

    assert Stack(Proj(1), Proj(0)).evaluate_in(alg)(10, 20) == [20, 10]

    assert Stack(Proj(1), Stack(PConst(128), Proj(0))).evaluate_in(alg)(10, 20) == [20, [128, 10]]

    assert Stack(Proj(3), Proj(2), Proj(1), Proj(0)).evaluate_in(alg)(10, 20, 30, 40) == [40, 30, 20, 10]

def test_composition():
    assert Comp(Succ(), Stack(PConst(2))).evaluate_in(alg)(10) == 3

    assert Comp(Succ(), Stack(Proj(1))).evaluate_in(alg)(10, 20) == 21
    assert Comp(Proj(1), Stack(PConst(128), Succ())).evaluate_in(alg)(10) == 11

def test_primitive_recursion():
    const_10 = PConst(10)
    twice_second_arg = Comp(Comp(Succ(), Stack(Succ())), Stack(Proj(1)))
    double_plus_10 = PrimRec(const_10, twice_second_arg)

    assert double_plus_10.evaluate_in(alg)(0) == 10
    assert double_plus_10.evaluate_in(alg)(1) == 12
    assert double_plus_10.evaluate_in(alg)(2) == 14
    assert double_plus_10.evaluate_in(alg)(3) == 16



    # Addition

    # g(y) = y
    g = Proj(0)

    # h(x, f(x, y), y) = succ(f(x, y))
    h = Comp(Succ(), Stack(Proj(1)))

    # f(0, y) = g(y) = y
    # f(S(x), y) = h(x, f(x, y), y) = succ(f(x, y))
    add2 = PrimRec(g, h)

    assert add2.evaluate_in(alg)(0, 0) == 0
    assert add2.evaluate_in(alg)(3, 0) == 3
    assert add2.evaluate_in(alg)(0, 5) == 5
    assert add2.evaluate_in(alg)(3, 5) == 8



    # Multiplication

    # g(y) = 0
    g = PConst(0)

    # h(x, f(x, y), y) = f(x, y) + y
    h = Comp(add2, Stack(Proj(1), Proj(2)))

    # f(0, y) = g(y) = 0
    # f(S(x), y) = h(x, f(x, y), y) = f(x, y) + y
    mult2 = PrimRec(g, h)

    assert mult2.evaluate_in(alg)(0, 0) == 0
    assert mult2.evaluate_in(alg)(3, 0) == 0
    assert mult2.evaluate_in(alg)(0, 5) == 0
    assert mult2.evaluate_in(alg)(3, 5) == 15



    # Triangular numbers

    # g() = 0
    g = PConst(0)

    # h(x, f(x)) = S(x) + f(x)
    h = Comp(add2, Stack(Comp(Succ(), Stack(Proj(0))), Proj(1)))

    # f(0) = g() = 0
    # f(S(x)) = h(x, f(x)) = S(x) + f(x)
    triang = PrimRec(g, h)

    assert triang.evaluate_in(alg)(0) == 0
    assert triang.evaluate_in(alg)(1) == 1
    assert triang.evaluate_in(alg)(2) == 3
    assert triang.evaluate_in(alg)(3) == 6
    assert triang.evaluate_in(alg)(4) == 10



    # Predecessor-or-10

    # g() = 10
    g = PConst(10)

    # h(x, f(x)) = x
    h = Proj(0)

    # f(0) = g() = 10
    # f(S(x)) = h(x, f(x)) = x
    pred_or_10 = PrimRec(g, h)

    assert pred_or_10.evaluate_in(alg)(0) == 10
    assert pred_or_10.evaluate_in(alg)(1) == 0
    assert pred_or_10.evaluate_in(alg)(2) == 1
    assert pred_or_10.evaluate_in(alg)(3) == 2
