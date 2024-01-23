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

from mathdonewrong.boolean_algebra import And, F, Not, Or, T, Var

def test_const_str_and_repr():
    assert str(T) == 'True'
    assert str(F) == 'False'

    assert repr(T) == "Const(True)"
    assert repr(F) == "Const(False)"

def test_can_evaluate_const():
    assert T.evaluate() == True
    assert F.evaluate() == False



def test_AND_str_and_repr():
    assert str(And(T, T)) == 'True & True'
    assert str(And(T, F)) == 'True & False'
    assert str(And(F, F)) == 'False & False'

    assert repr(And(T, T)) == 'And(Const(True), Const(True))'
    assert repr(And(T, F)) == 'And(Const(True), Const(False))'
    assert repr(And(F, F)) == 'And(Const(False), Const(False))'

def test_shortcut_for_AND():
    assert T & T == And(T, T)
    assert T & F == And(T, F)
    assert F & F == And(F, F)

def test_nested_AND_str():
    assert str((T & T) & T) == 'True & True & True'

    assert str(T & (T & T)) == 'True & (True & True)'

    assert str(T & (T & (T & T))) == 'True & (True & (True & True))'

    assert str((T & (T & T)) & T) == 'True & (True & True) & True'

def test_AND_evaluate():
    assert (T & T).evaluate() == True
    assert (T & F).evaluate() == False
    assert (F & T).evaluate() == False
    assert (F & F).evaluate() == False



def test_OR_str_and_repr():
    assert str(Or(T, T)) == 'True | True'
    assert str(Or(T, F)) == 'True | False'
    assert str(Or(F, F)) == 'False | False'

    assert repr(Or(T, T)) == 'Or(Const(True), Const(True))'
    assert repr(Or(T, F)) == 'Or(Const(True), Const(False))'
    assert repr(Or(F, F)) == 'Or(Const(False), Const(False))'

def test_shortcut_for_OR():
    assert T | T == Or(T, T)
    assert T | F == Or(T, F)
    assert F | F == Or(F, F)

def test_nested_OR_str():
    assert str((T | T) | T) == 'True | True | True'

    assert str(T | (T | T)) == 'True | (True | True)'

    assert str(T | (T | (T | T))) == 'True | (True | (True | True))'

    assert str((T | (T | T)) | T) == 'True | (True | True) | True'

def test_AND_binds_more_tightly_than_OR():
    assert str((T & T) | T) == 'True & True | True'
    assert str(T & (T | T)) == 'True & (True | True)'

    assert str(T | (T & T)) == 'True | True & True'
    assert str((T | T) & T) == '(True | True) & True'

def test_OR_evaluate():
    assert (T | T).evaluate() == True
    assert (T | F).evaluate() == True
    assert (F | T).evaluate() == True
    assert (F | F).evaluate() == False



def test_NOT_str_and_repr():
    assert str(Not(T)) == '~True'
    assert str(Not(F)) == '~False'

    assert repr(Not(T)) == 'Not(Const(True))'
    assert repr(Not(F)) == 'Not(Const(False))'

def test_shortcut_for_NOT():
    assert ~T == Not(T)
    assert ~F == Not(F)

def test_nested_NOT_str():
    assert str(~(~T)) == '~~True'

def test_NOT_binds_more_tightly_than_AND():
    assert str((~T) & T) == '~True & True'
    assert str(~(T & T)) == '~(True & True)'

def test_NOT_emits_at_precedence_80():
    assert f'{~T:80}' == '~True'
    assert f'{~T:81}' == '(~True)'

def test_NOT_evaluate():
    assert (~T).evaluate() == False
    assert (~F).evaluate() == True



def test_var_str_and_repr():
    assert str(Var('x')) == 'x'
    assert str(Var('y')) == 'y'

    assert repr(Var('x')) == "Var('x')"
    assert repr(Var('y')) == "Var('y')"

def test_nested_var_str():
    assert str(Var('x') & Var('y')) == 'x & y'

def test_var_evaluate():
    x, y = Var('x'), Var('y')

    assert x.evaluate({'x': True, 'y': False}) == True
    assert x.evaluate({'x': False, 'y': True}) == False
    assert y.evaluate({'x': True, 'y': False}) == False
    assert y.evaluate({'x': False, 'y': True}) == True

def test_complex_evaluate():
    x, y = Var('x'), Var('y')

    expr = (x & ~y) | (~x & y)

    assert expr.evaluate({'x': True, 'y': True}) == False
    assert expr.evaluate({'x': True, 'y': False}) == True
    assert expr.evaluate({'x': False, 'y': True}) == True
    assert expr.evaluate({'x': False, 'y': False}) == False

if __name__ == '__main__':
    pytest.main([__file__])
