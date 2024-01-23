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

Var = None

class BoolExpr(ex.Expression):
    def evaluate(self):
        return self.evaluate_in(StandardBooleanAlgebra(), {})

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)

class Const(BoolExpr, ex.Const):
    value: bool

    def __init__(self, value):
        ex.Const.__init__(self, str(value))
        self.value = value

    def __repr__(self):
        return f'Const({self.value})'

F = Const('False')
T = Const('True')

class And(BoolExpr, ex.Oper):
    precedence = 60

    def __init__(self, left, right):
        ex.Oper.__init__(self, '&', (left, right))

    def __str__(self):
        return f'{self.operands[0]:60} & {self.operands[1]:61}'

    def __repr__(self):
        return f'And({", ".join(repr(operand) for operand in self.operands)})'

class Or(BoolExpr, ex.Oper):
    precedence = 50

    def __init__(self, left, right):
        ex.Oper.__init__(self, '|', (left, right))

    def __str__(self):
        return f'{self.operands[0]:50} | {self.operands[1]:51}'

    def __repr__(self):
        return f'Or({", ".join(repr(operand) for operand in self.operands)})'

class Not(BoolExpr, ex.Oper):
    precedence = 80

    def __init__(self, operand):
        ex.Oper.__init__(self, '~', (operand,))

    def __str__(self):
        return f'~{self.operands[0]:80}'

    def __repr__(self):
        return f'Not({self.operands[0]!r})'

class StandardBooleanAlgebra(Algebra):
    @implement('True')
    def true(self):
        return True

    @implement('False')
    def false(self):
        return False

    @implement('&')
    def and_(self, left, right):
        return left and right

    @implement('|')
    def or_(self, left, right):
        return left or right

    @implement('~')
    def not_(self, operand):
        return not operand
