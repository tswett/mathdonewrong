# Copyright 2023 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from __future__ import annotations
from dataclasses import dataclass

class BoolExpr:
    def __str__(self):
        return self.__format__('')

    def __format__(self, format_spec: str):
        """Format using the specified precedence

        Format this boolean expression using the specified precedence limit,
        specified as a string containing an integer.

        The precedence limit is the maximum precedence of any operator that can
        appear in the output outside of parentheses. If the precedence of any
        operator in the expression is greater than the specified limit, then the
        expression will be parenthesized.
        """

        raise NotImplementedError

    def __and__(self, other: BoolExpr) -> BoolExpr:
        return And(self, other)

    def __or__(self, other: BoolExpr) -> BoolExpr:
        return Or(self, other)

    def __invert__(self) -> BoolExpr:
        return Not(self)

    def evaluate(self) -> bool:
        raise NotImplementedError

@dataclass
class Const(BoolExpr):
    value: bool

    def __repr__(self):
        return f'Const({self.value})'

    def __format__(self, format_spec: str):
        return str(self.value)

    def evaluate(self) -> bool:
        return self.value

@dataclass
class And(BoolExpr):
    left: BoolExpr
    right: BoolExpr

    def __repr__(self):
        return f'And({self.left!r}, {self.right!r})'

    def __format__(self, format_spec: str):
        if format_spec == '':
            precedence = 0
        else:
            precedence = int(format_spec)

        if precedence <= 60:
            return f'{self.left:60} & {self.right:61}'
        else:
            return f'({self.left:60} & {self.right:61})'

    def evaluate(self) -> bool:
        return self.left.evaluate() and self.right.evaluate()

@dataclass
class Or(BoolExpr):
    left: BoolExpr
    right: BoolExpr

    def __repr__(self):
        return f'Or({self.left!r}, {self.right!r})'

    def __format__(self, format_spec: str):
        if format_spec == '':
            precedence = 0
        else:
            precedence = int(format_spec)

        if precedence <= 50:
            return f'{self.left:50} | {self.right:51}'
        else:
            return f'({self.left:50} | {self.right:51})'

    def evaluate(self) -> bool:
        return self.left.evaluate() or self.right.evaluate()

@dataclass
class Not(BoolExpr):
    operand: BoolExpr

    def __repr__(self):
        return f'Not({self.operand!r})'

    def __format__(self, format_spec: str):
        if format_spec == '':
            precedence = 0
        else:
            precedence = int(format_spec)

        if precedence <= 80:
            return f'~{self.operand:80}'
        else:
            return f'(~{self.operand:80})'

    def evaluate(self) -> bool:
        return not self.operand.evaluate()
