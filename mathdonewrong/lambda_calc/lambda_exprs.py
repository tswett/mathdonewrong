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
from mathdonewrong.algebras import Algebra, operator
from mathdonewrong.expressions import Literal, NamedOper

class LambdaExpr:
    pass

# TODO: these should all inherit from LambdaExpr

class Lambda(NamedOper):
    def __init__(self, param, body):
        super().__init__(Literal(param), body)

    def __repr__(self):
        return f"Lambda({self.operands[0].value!r}, {self.operands[1]!r})"

    @property
    def param(self):
        param_, body = self.operands
        return param_.value

    @property
    def body(self):
        param_, body = self.operands
        return body

    def l_eval(self, context=None):
        context = context or {}
        return Closure(self.param, self.body, context)

class LVar(NamedOper):
    def __init__(self, varname):
        super().__init__(Literal(varname))

    def __repr__(self):
        return f"LVar({self.operands[0].value!r})"

    @property
    def varname(self):
        varname_, = self.operands
        return varname_.value

    def l_eval(self, context=None):
        context = context or {}
        return context[self.varname]

class Apply(NamedOper):
    @property
    def func(self):
        func, arg = self.operands
        return func

    @property
    def arg(self):
        func, arg = self.operands
        return arg

    def l_eval(self, context=None):
        context = context or {}

        func_ev = self.func.l_eval(context)
        arg_ev = self.arg.l_eval(context)

        return func_ev.body.l_eval(func_ev.env | {func_ev.param: arg_ev})



@dataclass
class Closure:
    param: str
    body: LambdaExpr
    env: dict
