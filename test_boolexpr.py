# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.boolexpr import And, Const, Or

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

def test_shortcuts_for_and():
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

def test_shortcuts_for_or():
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
