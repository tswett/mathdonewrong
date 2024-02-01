# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.code_to_expression import Apply, expressionize
from mathdonewrong.expressions import Var

@expressionize
def t_var(x):
    return x

def test_expressionize_var():
    assert t_var.expression == Var('x')

@expressionize
def t_var_with_decoy(x):
    y = 2
    return x

def test_expressionize_var_with_decoy():
    assert t_var_with_decoy.expression == Var('x')

@expressionize
def t_var_with_temp(x):
    y = x
    return y

def test_expressionize_var_with_temp():
    assert t_var_with_temp.expression == Var('x')

@expressionize
def t_apply(f, x):
    return f(x)

def test_expressionize_apply():
    assert t_apply.expression == Apply(Var('f'), Var('x'))
