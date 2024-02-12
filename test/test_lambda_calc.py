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
from mathdonewrong.expressions import Var
from mathdonewrong.lambda_calc.lambda_exprs import Apply, BoundExpr, EvalAlgebra, Lambda, LVar

I = Lambda('x', LVar('x'))
K = Lambda('x', Lambda('y', LVar('x')))

def test_repr():
    assert repr(LVar('x')) == "LVar('x')"
    assert repr(Lambda('x', Var('y'))) == "Lambda('x', Var('y'))"
    assert repr(Lambda('x', LVar('x'))) == "Lambda('x', LVar('x'))"

def test_l_evaluate_with():
    assert I.l_evaluate_with('x', LVar('y')) == I
    assert LVar('x').l_evaluate_with('x', LVar('y')) == LVar('y')

def test_BoundExpr():
    assert BoundExpr(K).apply(BoundExpr(I)) == BoundExpr(Lambda('y', LVar('x')), {'x': I})
    assert BoundExpr(I).apply(BoundExpr(I)) == BoundExpr(I)

@pytest.mark.skip("Not implemented yet")
def test_EvalAlgebra():
    alg = EvalAlgebra()

    assert LVar('x').evaluate_in(alg) == BoundExpr(LVar('x'))

    assert I.evaluate_in(alg) == BoundExpr(I)

    assert Apply(I,I).evaluate_in(alg) == BoundExpr(I)
    assert Apply(I,K).evaluate_in(alg) == BoundExpr(K)

    assert Apply(K,I).evaluate_in(alg) == BoundExpr(Lambda('y', LVar('x')), {'x': I})
