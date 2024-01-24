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

class Var(MonoidalExpr, ex.Var):
    pass

class Id(MonoidalExpr, ex.NamedOper):
    # ==> A -> A
    pass

class Compose(MonoidalExpr, ex.NamedOper):
    # A -> B, B -> C ==> A -> C
    pass

class Stack(MonoidalExpr, ex.NamedOper):
    # A -> C, B -> D ==> A | B -> C | D
    pass

class AssocRight(MonoidalExpr, ex.NamedOper):
    # ==> (A | B) | C -> A | (B | C)
    pass

class AssocLeft(MonoidalExpr, ex.NamedOper):
    # ==> A | (B | C) -> (A | B) | C
    pass

class Unit(MonoidalExpr, ex.NamedOper):
    # 1
    pass

class UnitLeft(MonoidalExpr, ex.NamedOper):
    # ==> A -> 1 | A
    pass

class UnitRight(MonoidalExpr, ex.NamedOper):
    # ==> A -> A | 1
    pass

class UnitLeftInv(MonoidalExpr, ex.NamedOper):
    # ==> 1 | A -> A
    pass

class UnitRightInv(MonoidalExpr, ex.NamedOper):
    # ==> A | 1 -> A
    pass

class Braid(MonoidalExpr, ex.NamedOper):
    # ==> A | B -> B | A
    pass

class BraidInv(MonoidalExpr, ex.NamedOper):
    # ==> B | A -> A | B
    pass

class Drop(MonoidalExpr, ex.NamedOper):
    # ==> A -> 1
    pass

class Diagonal(MonoidalExpr, ex.NamedOper):
    # ==> A -> A | A
    pass
