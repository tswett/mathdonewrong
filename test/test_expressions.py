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
from mathdonewrong.algebras import Algebra
from mathdonewrong.expressions import Expression, Literal, NamedOper, Oper, Var

class MyVar(Var):
    pass

def test_var_name():
    assert Var('x').name == 'x'



class MyLiteral(Literal):
    pass

class MyVarWithValue(Var):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

class MyOperX(Oper):
    def __init__(self, *operands):
        super().__init__('x', operands)

class NotAnExpression:
    def __init__(self, tag, name=None):
        self.tag = tag
        if name is not None:
            self.name = name

def test_different_things_not_equal():
    assert Var('x') != Var('y')

    assert Literal(1) != Literal(2)

    assert Oper('x', ()) != Oper('y', ())
    assert Oper('x', (Var('y'),)) != Oper('x', (Var('z'),))

def test_subclass_things_are_equal():
    assert MyVar('x') == Var('x')
    assert Var('x') == MyVar('x')
    assert MyVar('x') == MyVar('x')

    assert MyLiteral(1) == Literal(1)
    assert Literal(1) == MyLiteral(1)
    assert MyLiteral(1) == MyLiteral(1)

    assert MyOperX(Var('y')) == Oper('x', (Var('y'),))
    assert MyOperX(Var('y')) == MyOperX(Var('y'))

def test_variable_not_equal_to_operator():
    assert Var('x') != Oper('x', ())
    assert Oper('x', ()) != Var('x')

def test_literal_not_equal_to_var():
    assert Literal(1) != MyVarWithValue('x', 1)

def test_can_compare_to_non_expressions():
    assert Var('x') != 'x'
    assert Var('x') != NotAnExpression('var')

    assert Literal(1) != 1
    assert Literal(1) != NotAnExpression('literal')
    assert Literal(None) != NotAnExpression('literal')

    assert Oper('x', ()) != 'x'
    assert Oper('x', ()) != NotAnExpression('oper')
    assert Oper('x', ()) != NotAnExpression('oper', name='x')



def test_Oper_converts_operands_to_tuple():
    assert Oper('Plus', Var('x'), Var('y')).operands == (Var('x'), Var('y'))



class TestAlgebra(Algebra):
    def t(self):
        return True

def test_can_evaluate_things_without_context():
    assert Oper('T').evaluate_in(TestAlgebra()) == True
    assert Literal(50).evaluate_in(TestAlgebra()) == 50



class MyNamedOper(NamedOper):
    pass

def test_NamedOper_str():
    assert str(MyNamedOper(Var('x'), Var('y'))) == 'MyNamedOper(x, y)'




if __name__ == '__main__':
    pytest.main([__file__])
