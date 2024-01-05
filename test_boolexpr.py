# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.boolexpr import And, Const, Not, Or, Var

T, F = Const(True), Const(False)

def test_const_str_and_repr():
    assert str(T) == 'True'
    assert str(F) == 'False'

    assert repr(T) == 'Const(True)'
    assert repr(F) == 'Const(False)'

def test_can_evaluate_const():
    assert T.evaluate() == True
    assert F.evaluate() == False



def test_and_str_and_repr():
    assert str(And(T, T)) == 'True & True'
    assert str(And(T, F)) == 'True & False'
    assert str(And(F, F)) == 'False & False'

    assert repr(And(T, T)) == 'And(Const(True), Const(True))'
    assert repr(And(T, F)) == 'And(Const(True), Const(False))'
    assert repr(And(F, F)) == 'And(Const(False), Const(False))'

def test_shortcut_for_and():
    assert T & T == And(T, T)
    assert T & F == And(T, F)
    assert F & F == And(F, F)

def test_nested_and_str():
    assert str((T & T) & T) == 'True & True & True'

    assert str(T & (T & T)) == 'True & (True & True)'

    assert str(T & (T & (T & T))) == 'True & (True & (True & True))'

    assert str((T & (T & T)) & T) == 'True & (True & True) & True'

def test_and_evaluate():
    assert (T & T).evaluate() == True
    assert (T & F).evaluate() == False
    assert (F & T).evaluate() == False
    assert (F & F).evaluate() == False



def test_or_str_and_repr():
    assert str(Or(T, T)) == 'True | True'
    assert str(Or(T, F)) == 'True | False'
    assert str(Or(F, F)) == 'False | False'

    assert repr(Or(T, T)) == 'Or(Const(True), Const(True))'
    assert repr(Or(T, F)) == 'Or(Const(True), Const(False))'
    assert repr(Or(F, F)) == 'Or(Const(False), Const(False))'

def test_shortcut_for_or():
    assert T | T == Or(T, T)
    assert T | F == Or(T, F)
    assert F | F == Or(F, F)

def test_nested_or_str():
    assert str((T | T) | T) == 'True | True | True'

    assert str(T | (T | T)) == 'True | (True | True)'

    assert str(T | (T | (T | T))) == 'True | (True | (True | True))'

    assert str((T | (T | T)) | T) == 'True | (True | True) | True'

def test_and_binds_more_tightly_than_or():
    assert str((T & T) | T) == 'True & True | True'
    assert str(T & (T | T)) == 'True & (True | True)'

    assert str(T | (T & T)) == 'True | True & True'
    assert str((T | T) & T) == '(True | True) & True'

def test_or_evaluate():
    assert (T | T).evaluate() == True
    assert (T | F).evaluate() == True
    assert (F | T).evaluate() == True
    assert (F | F).evaluate() == False



def test_not_str_and_repr():
    assert str(Not(T)) == '~True'
    assert str(Not(F)) == '~False'

    assert repr(Not(T)) == 'Not(Const(True))'
    assert repr(Not(F)) == 'Not(Const(False))'

def test_shortcut_for_not():
    assert ~T == Not(T)
    assert ~F == Not(F)

def test_nested_not_str():
    assert str(~(~T)) == '~~True'

def test_not_binds_more_tightly_than_and():
    assert str((~T) & T) == '~True & True'
    assert str(~(T & T)) == '~(True & True)'

def test_not_emits_at_precedence_80():
    assert f'{~T:80}' == '~True'
    assert f'{~T:81}' == '(~True)'

def test_not_evaluate():
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
