# Copyright 2024 Tanner Swett.
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
from typing import Optional

class BoolExpr:
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

    def __and__(self, other: BoolExpr) -> BoolExpr:
        return And(self, other)

    def __or__(self, other: BoolExpr) -> BoolExpr:
        return Or(self, other)

    def __invert__(self) -> BoolExpr:
        return Not(self)

    @property
    def precedence(self) -> int:
        raise NotImplementedError

    def evaluate(self, context: Optional[dict[str, bool]] = None) -> bool:
        context = context or {}
        return self.evaluate_in(context)

    def evaluate_in(self, context: dict[str, bool]) -> bool:
        raise NotImplementedError

@dataclass
class Const(BoolExpr):
    value: bool

    precedence = 100

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'Const({self.value})'

    def evaluate_in(self, context: dict[str, bool]) -> bool:
        return self.value

F = Const(False)
T = Const(True)

@dataclass
class And(BoolExpr):
    left: BoolExpr
    right: BoolExpr

    precedence = 60

    def __str__(self):
        return f'{self.left:60} & {self.right:61}'

    def __repr__(self):
        return f'And({self.left!r}, {self.right!r})'

    def evaluate_in(self, context: dict[str, bool]) -> bool:
        return self.left.evaluate_in(context) and self.right.evaluate_in(context)

@dataclass
class Or(BoolExpr):
    left: BoolExpr
    right: BoolExpr

    precedence = 50

    def __str__(self):
        return f'{self.left:50} | {self.right:51}'

    def __repr__(self):
        return f'Or({self.left!r}, {self.right!r})'

    def evaluate_in(self, context: dict[str, bool]) -> bool:
        return self.left.evaluate_in(context) or self.right.evaluate_in(context)

@dataclass
class Not(BoolExpr):
    operand: BoolExpr

    precedence = 80

    def __str__(self):
        return f'~{self.operand:80}'

    def __repr__(self):
        return f'Not({self.operand!r})'

    def evaluate_in(self, context: dict[str, bool]) -> bool:
        return not self.operand.evaluate_in(context)

@dataclass
class Var(BoolExpr):
    name: str

    precedence = 100

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Var({self.name!r})'

    def evaluate_in(self, context: dict[str, bool]) -> bool:
        return context[self.name]
