# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.expressions import Literal, Oper, Var

class MyVar(Var):
    pass

class MyOperX(Oper):
    def __init__(self, *operands):
        super().__init__('x', operands)

def test_different_variables_not_equivalent():
    assert not Var('x').is_equiv(Var('y'))

def test_identical_variables_are_equivalent():
    assert Var('x').is_equiv(Var('x'))

def test_subclass_variable_is_equivalent():
    assert MyVar('x').is_equiv(Var('x'))

def test_variable_not_equivalent_to_operator():
    assert not Var('x').is_equiv(Oper('x', ()))

def test_identical_opers_are_equivalent():
    assert Oper('x', ()).is_equiv(Oper('x', ()))

def test_different_opers_not_equivalent():
    assert not Oper('x', ()).is_equiv(Oper('y', ()))

def test_subclass_oper_is_equivalent():
    assert MyOperX().is_equiv(Oper('x', ()))

def test_operator_not_equivalent_to_variable():
    assert not Oper('x', ()).is_equiv(Var('x'))

def test_operator_different_operands_not_equivalent():
    assert not Oper('x', (Var('y'),)).is_equiv(Oper('x', (Var('z'),)))

def test_operator_subclass_operand_is_equivalent():
    assert Oper('x', (MyVar('y'),)).is_equiv(Oper('x', (Var('y'),)))

def test_operator_different_operand_counts_not_equivalent():
    assert not Oper('x', ()).is_equiv(Oper('x', (Var('y'),)))

def test_different_literals_not_equivalent():
    assert not Literal(1).is_equiv(Literal(2))
