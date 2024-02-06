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

from mathdonewrong.algebras import Algebra, attr_name_to_operator_name, operator, relation
from mathdonewrong.expressions import NamedOper, Var

def test_funcname_to_operator_name():
    assert attr_name_to_operator_name('my_favorite_operator') == 'MyFavoriteOperator'

class Mult(NamedOper):
    pass

class TestMagma(Algebra):
    @operator()
    def mult(self, x, y):
        raise NotImplementedError

@pytest.mark.skip("not implemented yet")
def test_magma_variety():
    oper, = TestMagma.variety.operators
    assert oper.name == 'Mult'

def test_subclassing_Algebra_does_not_alter_it():
    assert Algebra.members == {}

class TestMagmaNewAttrName(TestMagma):
    @operator('Mult')
    def mult2(self, x, y):
        return x * y

def test_subclass_can_override_operator_attr_name():
    member = TestMagmaNewAttrName.members['Mult'] 
    assert member.attr_name == 'mult2'

class TestMagmaDifferentAttrName(Algebra):
    @operator('Mult')
    def multiply(self, x, y):
        return x * y

def test_can_invoke_operator_by_name():
    magma = TestMagmaDifferentAttrName()
    assert magma.operate('Mult', (3, 5)) == 15

class TestSemigroup(TestMagma):
    @relation()
    def assoc(self, x, y, z):
        return self.mult(self.mult(x, y), z)

    def assoc_rhs(self, x, y, z):
        return self.mult(x, self.mult(y, z))

x, y, z = Var('x'), Var('y'), Var('z')

@pytest.mark.skip("not implemented yet")
def test_semigroup_algebra_info():
    rel, = TestSemigroup.relations.values()
    assert rel.name == 'Assoc'

@pytest.mark.skip("not implemented yet")
def test_semigroup_variety():
    oper, = TestSemigroup.variety.operators
    assert oper.name == 'Mult'

    rel, = TestSemigroup.variety.relations
    assert rel.lhs == Mult(Mult(x, y), z)
    assert rel.rhs == Mult(x, Mult(y, z))

if __name__ == '__main__':
    pytest.main([__file__])
