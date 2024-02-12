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
from mathdonewrong.code_to_expression import expressionize
#from mathdonewrong.lambda_calc.lambda_exprs import Apply, Lambda, LamConst, LamVar

pytest.skip(allow_module_level=True)

@expressionize
def t_var(x):
    return x

def test_expressionize_var():
    assert t_var.expression == LamVar('x')

@expressionize
def t_const_5():
    return 5

@expressionize
def t_const_hello():
    return 'hello'

def test_expressionize_const():
    assert t_const_5.expression == LamConst('5')
    assert t_const_hello.expression == LamConst(repr('hello'))

@expressionize
def t_var_with_decoy(x):
    y = 2
    return x

def test_expressionize_var_with_decoy():
    assert t_var_with_decoy.expression == LamVar('x')

@expressionize
def t_var_with_temp(x):
    y = x
    return y

def test_expressionize_var_with_temp():
    assert t_var_with_temp.expression == LamVar('x')

@expressionize
def t_apply(f, x):
    return f(x)

def test_expressionize_apply():
    assert t_apply.expression == Apply(LamVar('f'), LamVar('x'))

@expressionize
def t_lambda_x_x():
    return lambda x: x

@expressionize
def t_lambda_x_y_x():
    return lambda x: lambda y: x

def test_expressionize_lambda():
    assert t_lambda_x_x.expression == Lambda('x', LamVar('x'))
    assert t_lambda_x_y_x.expression == Lambda('x', Lambda('y', LamVar('x')))

@expressionize
def t_apply_lambda_to_lambda():
    return (lambda x: x)(lambda y: y)

def test_expressionize_apply_lambda_to_lambda():
    assert t_apply_lambda_to_lambda.expression == Apply(Lambda('x', LamVar('x')), Lambda('y', LamVar('y')))



if __name__ == '__main__':
    pytest.main([__file__])
