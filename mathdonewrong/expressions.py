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
from typing import Any

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

    def traverse(self, visitor):
        raise NotImplementedError

    def is_equiv(self, other):
        raise NotImplementedError

    @property
    def tag(self):
        raise NotImplementedError

@dataclass
class Var(Expression):
    name: str

    def evaluate_in(self, algebra, context):
        return context[self.name]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r})"

    def traverse(self, visitor):
        return visitor.visit_var(self)

    def is_equiv(self, other):
        return other.tag == 'var' and self.name == other.name

    @property
    def tag(self):
        return 'var'

@dataclass
class Literal(Expression):
    value: Any

    def evaluate_in(self, algebra, context):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{type(self).__name__}({self.value!r})"

    def traverse(self, visitor):
        return visitor.visit_literal(self)

    def is_equiv(self, other):
        # TODO: finish implementing this
        return False

@dataclass
class Oper(Expression):
    name: str
    operands: tuple[Expression, ...]

    def evaluate_in(self, algebra, context):
        operand_values = [operand.evaluate_in(algebra, context) for operand in self.operands]
        return algebra.operate(self.name, operand_values)

    def traverse(self, visitor):
        return visitor.visit_oper(self)

    def copy_with_new_operands(self, new_operands):
        # This feels like an awful hack, but it seems to work.
        copy = type(self).__new__(type(self))
        for name, value in self.__dict__.items():
            setattr(copy, name, value)
        copy.operands = tuple(new_operands)
        return copy

    def repr_like_named_oper(self):
        return f'{type(self).__name__}({", ".join(repr(operand) for operand in self.operands)})'

    def is_equiv(self, other):
        if not (other.tag == 'oper' and self.name == other.name and len(self.operands) == len(other.operands)):
            return False

        return all(self.operands[i].is_equiv(other.operands[i]) for i in range(len(self.operands)))

    @property
    def tag(self):
        return 'oper'

class Const(Oper):
    def __init__(self, value):
        super().__init__(str(value), ())

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{type(self).__name__}({self.name!r})'

class BinaryOper(Oper):
    def __init__(self, left, right):
        super().__init__(self.name, (left, right))

    def __str__(self):
        return f'{self.operands[0]:{self.precedence}} {self.name} {self.operands[1]:{self.precedence + 1}}'

    def __repr__(self):
        return self.repr_like_named_oper()

class PrefixOper(Oper):
    def __init__(self, operand):
        super().__init__(self.name, (operand,))

    def __str__(self):
        operand, = self.operands
        return f'{self.name}{operand:{self.precedence}}'

    def __repr__(self):
        return self.repr_like_named_oper()

class NamedOper(Oper):
    def __init__(self, *operands):
        super().__init__(type(self).__name__, operands)

    def __repr__(self):
        return self.repr_like_named_oper()
