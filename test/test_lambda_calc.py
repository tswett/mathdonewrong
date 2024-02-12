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
from mathdonewrong.lambda_calc.lambda_exprs import Apply, Closure, Lambda, LVar

B = Lambda('x', Lambda('y', Lambda('z', Apply(LVar('x'), Apply(LVar('y'), LVar('z'))))))
C = Lambda('x', Lambda('y', Lambda('z', Apply(Apply(LVar('x'), LVar('z')), LVar('y')))))
I = Lambda('x', LVar('x'))
K = Lambda('x', Lambda('y', LVar('x')))
S = Lambda('x', Lambda('y', Lambda('z', Apply(Apply(LVar('x'), LVar('z')), Apply(LVar('y'), LVar('z'))))))
W = Lambda('x', Lambda('y', Apply(Apply(LVar('x'), LVar('y')), LVar('y'))))

def test_repr():
    assert repr(LVar('x')) == "LVar('x')"
    assert repr(Lambda('x', Var('y'))) == "Lambda('x', Var('y'))"
    assert repr(Lambda('x', LVar('x'))) == "Lambda('x', LVar('x'))"

def test_l_eval():
    I_ev = Closure('x', LVar('x'), {})
    K_ev = Closure('x', Lambda('y', LVar('x')), {})

    assert I.l_eval() == I_ev
    assert K.l_eval() == K_ev

    assert Apply(K, I).l_eval() == Closure('y', LVar('x'), {'x': I_ev})
    assert Apply(I, I).l_eval() == I_ev
    assert Apply(I, K).l_eval() == K_ev

    assert Apply(Apply(K, K), I).l_eval() == K_ev
    assert Apply(Apply(K, I), K).l_eval() == I_ev

    assert Apply(Apply(Lambda('y', Lambda('y', LVar('y'))), I), K).l_eval() == K_ev

    assert Apply(Lambda('x', Apply(Apply(K, LVar('x')), LVar('x'))), I).l_eval() == I_ev



if __name__ == '__main__':
    pytest.main([__file__])
