# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.algebras import Algebra, operator
import mathdonewrong.expressions as ex

class BoolExpr(ex.Expression):
    def evaluate(self, context=None):
        return self.evaluate_in(StandardBooleanAlgebra(), context or {})

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

class Var(BoolExpr, ex.Var):
    pass

class And(BoolExpr, ex.BinaryOper):
    name = '&'
    precedence = 60

class Or(BoolExpr, ex.BinaryOper):
    name = '|'
    precedence = 50

class Not(BoolExpr, ex.PrefixOper):
    name = '~'
    precedence = 80

class BooleanAlgebra(Algebra):
    @operator('True')
    def true(self):
        raise NotImplementedError

    @operator('False')
    def false(self):
        raise NotImplementedError

    @operator('&')
    def and_(self, left, right):
        raise NotImplementedError

    @operator('|')
    def or_(self, left, right):
        raise NotImplementedError

    @operator('~')
    def not_(self, operand):
        raise NotImplementedError

class StandardBooleanAlgebra(BooleanAlgebra):
    def true(self):
        return True

    def false(self):
        return False

    def and_(self, left, right):
        return left and right

    def or_(self, left, right):
        return left or right

    def not_(self, operand):
        return not operand
