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

x, y, z = LVar('x'), LVar('y'), LVar('z')

def test_repr():
    assert repr(LVar('x')) == "LVar('x')"
    assert repr(Lambda('x', Var('y'))) == "Lambda('x', Var('y'))"
    assert repr(Lambda('x', LVar('x'))) == "Lambda('x', LVar('x'))"

def test_apply_shortcut():
    assert x(y) == Apply(x, y)
    assert x(y)(z) == Apply(Apply(x, y), z)
    assert Lambda('x', y)(z) == Apply(Lambda('x', y), z)

Lx = lambda arg: Lambda('x', arg)
Ly = lambda arg: Lambda('y', arg)
Lz = lambda arg: Lambda('z', arg)

B = Lx(Ly(Lz(x(y(z)))))
C = Lx(Ly(Lz(x(z)(y))))
I = Lx(x)
K = Lx(Ly(x))
S = Lx(Ly(Lz(x(z)(y(z)))))
W = Lx(Ly(x(y)(y)))

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

def test_bciksw():
    true = K
    false = K(I)

    true_ev = Closure('x', Ly(x), {})
    false_ev = Closure('y', x, {'x': I.l_eval()})

    assert true.l_eval() == true_ev
    assert false.l_eval() == false_ev

    not_ = C(C(I)(false))(true)

    assert not_(true).l_eval() == false_ev
    assert not_(false).l_eval() == true_ev

    notnot = B(not_)(not_)

    assert notnot(true).l_eval() == true_ev
    assert notnot(false).l_eval() == false_ev

    # I'm calling that good for now.





if __name__ == '__main__':
    pytest.main([__file__])
