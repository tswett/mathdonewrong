# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from mathdonewrong.expressions import Const, Expression, NamedOper, Var

class LambdaExpr(Expression):
    pass

class LamVar(LambdaExpr, Var):
    pass

class LamConst(LambdaExpr, Const):
    pass

class Apply(LambdaExpr, NamedOper):
    pass

class Lambda(LambdaExpr, NamedOper):
    def __init__(self, var_name: str, body: LambdaExpr):
        super().__init__(LamVar(var_name), body)

    def __repr__(self):
        var, body = self.operands
        return f'Lambda({var.name!r}, {body!r})'
