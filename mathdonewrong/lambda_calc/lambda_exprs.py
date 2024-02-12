# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from dataclasses import dataclass, field
from mathdonewrong.algebras import Algebra, operator
from mathdonewrong.expressions import Const, Expression, Literal, NamedOper, Var

class LambdaExpr:
    def l_evaluate_with(self, var, value):
        return self

# TODO: these should all inherit from LambdaExpr

class Lambda(LambdaExpr, NamedOper):
    def __init__(self, var, body):
        super().__init__(Literal(var), body)
        self.free_vars = body.free_vars

    def __repr__(self):
        return f"Lambda({self.operands[0].value!r}, {self.operands[1]!r})"

    @property
    def body(self):
        var, body = self.operands
        return body

class LVar(NamedOper):
    def __init__(self, name):
        super().__init__(Literal(name))
        self.free_vars = (name,)

    def __repr__(self):
        return f"LVar({self.operands[0].value!r})"

    def l_evaluate_with(self, var, value):
        # TODO: check if var == self.name
        return value

class Apply(NamedOper):
    pass

@dataclass
class BoundExpr:
    expr: LambdaExpr
    context: dict[str, LambdaExpr] = field(default_factory=dict)

    def apply(self, arg):
        # TODO: obviously the parameter isn't always named 'x'
        new_body = self.expr.body.l_evaluate_with('x', arg.expr)

        if 'x' in new_body.free_vars:
            # TODO: carry the rest of the context over, too
            return BoundExpr(new_body, {'x': arg.expr})
        else:
            return BoundExpr(new_body)

class EvalAlgebra(Algebra):
    @operator('Lambda')
    def lambda_(self, var, body):
        return BoundExpr(Lambda(var, body.expr))

    def l_var(self, name):
        return BoundExpr(LVar(name))

    def apply(self, fun, arg):
        return fun.apply(arg)
