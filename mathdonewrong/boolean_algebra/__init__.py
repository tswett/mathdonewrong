# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.algebras import Algebra, implement
import mathdonewrong.expressions as ex

And = Not = Or = Var = None

class BoolExpr(ex.Expression):
    def evaluate(self):
        return self.evaluate_in(StandardBooleanAlgebra(), {})

class Const(BoolExpr, ex.Const):
    value: bool

    def __init__(self, value):
        ex.Const.__init__(self, str(value))
        self.value = value

    def __repr__(self):
        return f'Const({self.value})'

F = Const('False')
T = Const('True')

class StandardBooleanAlgebra(Algebra):
    @implement('True')
    def true(self):
        return True

    @implement('False')
    def false(self):
        return False
