# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

import mathdonewrong.expressions as ex

class MonoidalExpr(ex.Expression):
    pass

class Id(MonoidalExpr, ex.Oper):
    # ==> A -> A
    pass

class Compose(MonoidalExpr, ex.Oper):
    # A -> B, B -> C ==> A -> C
    pass

class Stack(MonoidalExpr, ex.Oper):
    # A -> C, B -> D ==> A | B -> C | D
    pass

class AssocRight(MonoidalExpr, ex.Oper):
    # ==> (A | B) | C -> A | (B | C)
    pass

class AssocLeft(MonoidalExpr, ex.Oper):
    # ==> A | (B | C) -> (A | B) | C
    pass

class Unit(MonoidalExpr, ex.Oper):
    # 1
    pass

class UnitLeft(MonoidalExpr, ex.Oper):
    # ==> A -> 1 | A
    pass

class UnitRight(MonoidalExpr, ex.Oper):
    # ==> A -> A | 1
    pass

class UnitLeftInv(MonoidalExpr, ex.Oper):
    # ==> 1 | A -> A
    pass

class UnitRightInv(MonoidalExpr, ex.Oper):
    # ==> A | 1 -> A
    pass

class Braid(MonoidalExpr, ex.Oper):
    # ==> A | B -> B | A
    pass

class BraidInv(MonoidalExpr, ex.Oper):
    # ==> B | A -> A | B
    pass

class Drop(MonoidalExpr, ex.Oper):
    # ==> A -> 1
    pass

class Diagonal(MonoidalExpr, ex.Oper):
    # ==> A -> A | A
    pass
