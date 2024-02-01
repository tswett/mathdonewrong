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
import inspect
from typing import Callable
from mathdonewrong.algebras import Algebra

from mathdonewrong.code_to_expression import code_to_expression
from mathdonewrong.lambda_calc.lambda_exprs import LambdaExpr
from mathdonewrong.monoidal_categories.monoidalexpr import Compose, Drop, Id, MonoidalExpr, Stack, Unit, Var

def context_to_object_expr(context: tuple[str, ...]) -> MonoidalExpr:
    expr = None

    for var_name in context:
        if expr is None:
            expr = Var(var_name)
        else:
            expr = Stack(expr, Var(var_name))

    return expr or Unit()

@dataclass
class MonoidalExprWithContext():
    context: tuple[str, ...]
    expr: MonoidalExpr

    @staticmethod
    def var(name: str) -> MonoidalExprWithContext:
        return MonoidalExprWithContext((name,), Var(name))

    def adjust_context(self, new_context: tuple[str, ...]) -> MonoidalExprWithContext:
        if self.context == new_context:
            return self
        else:
            adjustment = MonoidalExprWithContext.make_adjustment(self.context, new_context)
            new_expr = Compose(adjustment, self)
            return MonoidalExprWithContext(new_context, new_expr)

    @staticmethod
    def make_adjustment(old_context: tuple[str, ...], new_context: tuple[str, ...]) -> MonoidalExpr:
        if old_context == new_context:
            domain = context_to_object_expr(new_context)
            return Id(domain)

        elif len(old_context) == 0:
            domain = context_to_object_expr(new_context)
            return Drop(domain)

class LambdaToMonoidalAlgebra(Algebra):
    pass

class LambdaToMonoidalVarDict():
    def __getitem__(self, key: str):
        return MonoidalExprWithContext.var(key)

def expression_to_monoidal(context: tuple[str, ...], expr: LambdaExpr) -> MonoidalExpr:
    """Convert a lambda expression to an equivalent monoidal expression

    Given a lambda expression, potentially with some free variables, produce a
    monoidal expression. The domain of the monoidal expression corresponds to
    the given context, and the codomain corresponds to the return type of the
    lambda expression.
    """

    monoidal_w_context = expr.evaluate_in(LambdaToMonoidalAlgebra(), LambdaToMonoidalVarDict())
    monoidal_w_context_adjusted = monoidal_w_context.adjust_context(context)
    return monoidal_w_context_adjusted.expr

def expressionize_m(f: Callable) -> Callable:
    lambda_expr = code_to_expression(f)
    params = tuple(inspect.signature(f).parameters)
    f.expression = expression_to_monoidal(params, lambda_expr)
    return f
