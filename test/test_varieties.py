# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

import textwrap

from mathdonewrong.common.common_opers import Times
from mathdonewrong.expressions import NamedOper, Oper, Var
from mathdonewrong.varieties import Operator, Relation, Variety

class MyOper(NamedOper):
    pass

def test_variety_equality():
    # We want to make sure that two varieties are equal if and only if their lhs's are equivalent and their rhs's are equivalent.

    assert Relation(MyOper(), MyOper()) == Relation(Oper('MyOper') , Oper('MyOper'))
    assert Relation(MyOper(), MyOper()) != Relation(Oper('NotMyOper') , Oper('MyOper'))
    assert Relation(MyOper(), MyOper()) != Relation(Oper('MyOper') , Oper('NotMyOper'))

x, y, z = Var('x'), Var('y'), Var('z')

variety_of_semigroups = Variety(
    operators=[Operator('Times')],
    relations=[Relation(
        lhs=Times(x, Times(y, z)),
        rhs=Times(Times(x, y), z)
    )]
)

def test_variety_str():
    assert str(variety_of_semigroups) == textwrap.dedent('''\
        variety:
            operators:
                Times
            relations:
                Times(x, Times(y, z)) = Times(Times(x, y), z)''')

def test_Monoid_variety():
    from mathdonewrong.monoids.monoids import Monoid
    str(Monoid.variety)
