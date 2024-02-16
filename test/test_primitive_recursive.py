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
from mathdonewrong.primitive_recursive.primrec_exprs import Comp, PConst, Proj, StandardPrimitiveRecursiveAlgebra, Succ

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
    assert PConst(0).evaluate_in(alg, {})() == 0
    assert PConst(1).evaluate_in(alg, {})() == 1
    assert PConst(2).evaluate_in(alg, {})() == 2
    assert PConst(3).evaluate_in(alg, {})() == 3

    assert PConst(4).evaluate_in(alg, {})(3) == 4

def test_successor():
    assert Succ().evaluate_in(alg, {})(0) == 1
    assert Succ().evaluate_in(alg, {})(1) == 2
    assert Succ().evaluate_in(alg, {})(2) == 3
    assert Succ().evaluate_in(alg, {})(3) == 4

def test_projection():
    assert Proj(0).evaluate_in(alg, {})(3) == 3

    assert Proj(0).evaluate_in(alg, {})(3, 1) == 3
    assert Proj(1).evaluate_in(alg, {})(3, 1) == 1

    assert Proj(0).evaluate_in(alg, {})(3, 1, 4) == 3
    assert Proj(1).evaluate_in(alg, {})(3, 1, 4) == 1
    assert Proj(2).evaluate_in(alg, {})(3, 1, 4) == 4

def test_composition():
    assert Comp(Proj(0), Succ(), PConst(2)).evaluate_in(alg, {})(10) == 11
    assert Comp(Proj(1), Succ(), PConst(2)).evaluate_in(alg, {})(10) == 2

    assert Comp(Proj(0), Proj(1), Proj(0)).evaluate_in(alg, {})(10, 20) == 20
    assert Comp(Proj(1), Proj(1), Proj(0)).evaluate_in(alg, {})(10, 20) == 10
