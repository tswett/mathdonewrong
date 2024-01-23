# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from dataclasses import dataclass

class Expression:
    precedence = 100

    def __str__(self):
        raise NotImplementedError

    def __format__(self, format_spec: str):
        """Format using the specified precedence

        Format this boolean expression using the specified precedence limit,
        specified as a string containing an integer.

        The precedence limit is the minimum (loosest) precedence of any operator
        that can appear in the output outside of parentheses. If the expression
        contains an operator that binds more loosely than the limit, then
        parentheses will be added around it in at least one place.
        """

        if format_spec == '':
            precedence = 0
        else:
            precedence = int(format_spec)

        if precedence <= self.precedence:
            return str(self)
        else:
            return f'({str(self)})'

    def evaluate_in(self, algebra, context):
        raise NotImplementedError

@dataclass
class Var(Expression):
    name: str

    def evaluate_in(self, algebra, context):
        return context[self.name]

@dataclass
class Oper(Expression):
    name: str
    operands: tuple[Expression, ...]

    def evaluate_in(self, algebra, context):
        operand_values = [operand.evaluate_in(algebra, context) for operand in self.operands]
        return algebra.operate(self.name, operand_values)

class Const(Oper):
    def __init__(self, value):
        super().__init__(str(value), ())

    def __str__(self):
        return self.name
