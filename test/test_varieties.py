# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.expressions import NamedOper, Oper
from mathdonewrong.varieties import Relation

class MyOper(NamedOper):
    pass

def test_variety_equality():
    # We want to make sure that two varieties are equal if and only if their lhs's are equivalent and their rhs's are equivalent.

    assert Relation(MyOper(), MyOper()) == Relation(Oper('MyOper', ()) , Oper('MyOper', ()))
    assert Relation(MyOper(), MyOper()) != Relation(Oper('NotMyOper', ()) , Oper('MyOper', ()))
    assert Relation(MyOper(), MyOper()) != Relation(Oper('MyOper', ()) , Oper('NotMyOper', ()))
