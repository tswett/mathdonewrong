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
from mathdonewrong.expressions import Expression, Literal, Oper, Var

class MyVar(Var):
    pass

class MyLiteral(Literal):
    pass

class MyOperX(Oper):
    def __init__(self, *operands):
        super().__init__('x', operands)

class BadExpression(Expression):
    @property
    def tag(self):
        return 'bad'

def test_from_expr():
    assert Expression.from_expr(Var('x')) == Var('x')
    assert Expression.from_expr(MyVar('y')) == Var('y')

    assert Expression.from_expr(Literal(1)) == Literal(1)
    assert Expression.from_expr(MyLiteral(2)) == Literal(2)

    assert Expression.from_expr(Oper('x', ())) == Oper('x', ())
    assert Expression.from_expr(Oper('y', ())) == Oper('y', ())
    assert Expression.from_expr(MyOperX()) == Oper('x', ())

    assert Expression.from_expr(Oper('x', (MyVar('y'),))) == Oper('x', (Var('y'),))

    with pytest.raises(ValueError):
        Expression.from_expr(BadExpression())

def test_identical_variables_are_equivalent():
    assert Var('x').is_equiv(Var('x'))

def test_different_variables_not_equivalent():
    assert not Var('x').is_equiv(Var('y'))

def test_subclass_variable_is_equivalent():
    assert MyVar('x').is_equiv(Var('x'))
    assert Var('x').is_equiv(MyVar('x'))
