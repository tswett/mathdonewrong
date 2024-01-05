# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.boolexpr import And, Const

T, F = Const(True), Const(False)

def test_can_create_constant_boolexpr():
    Const(True)
    Const(False)

def test_const_str_and_repr():
    assert str(T) == 'True'
    assert str(F) == 'False'

    assert repr(T) == 'Const(True)'
    assert repr(F) == 'Const(False)'

def test_can_evaluate_const():
    assert Const(True).evaluate() == True
    assert Const(False).evaluate() == False

def test_can_create_and_expression():
    And(Const(True), Const(False))

def test_and_str_and_repr():
    assert str(And(T, T)) == 'True & True'
    assert str(And(T, F)) == 'True & False'
    assert str(And(F, F)) == 'False & False'

    assert repr(And(T, T)) == 'And(Const(True), Const(True))'
    assert repr(And(T, F)) == 'And(Const(True), Const(False))'
    assert repr(And(F, F)) == 'And(Const(False), Const(False))'

#def test_nested_and_str():
#    assert str(And(And(T, T), T)) == 'True & True & True'
#    assert str(And(T, And(T, T))) == 'True & (True & True)'
