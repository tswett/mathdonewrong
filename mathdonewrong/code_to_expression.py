# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

import ast
from ast import NodeVisitor
import inspect
from typing import Callable

from mathdonewrong.expressions import Expression, NamedOper, Oper, Var

class Apply(NamedOper):
    # TODO: This should be defined somewhere else, but I'm not sure where yet
    pass

class SubstitutionVisitor:
    def __init__(self, context: dict[str, Expression]):
        self.context = context

    def visit_var(self, expr: Var) -> Expression:
        if expr.name in self.context:
            return self.context[expr.name]
        else:
            return expr

    def visit_oper(self, expr: Oper) -> Expression:
        new_operands = [operand.traverse(self) for operand in expr.operands]
        return expr.copy_with_new_operands(new_operands)

def substitute_vars(expr: Expression, context: dict[str, Expression]) -> Expression:
    return expr.traverse(SubstitutionVisitor(context))

class ExpressionizeNodeVisitor(NodeVisitor):
    def __init__(self):
        self.locals = {}

    def visit_Module(self, node) -> Expression:
        return self.visit(node.body[0])

    def visit_FunctionDef(self, node) -> Expression:
        for statement in node.body:
            expr_maybe = self.visit(statement)
            if expr_maybe is not None:
                return expr_maybe

    def visit_Return(self, node) -> Expression:
        return_expression = self.visit(node.value)
        return substitute_vars(return_expression, self.locals)

    def visit_Assign(self, node) -> Expression:
        target_name = node.targets[0].id
        self.locals[target_name] = self.visit(node.value)

    def visit_Name(self, node) -> Expression:
        return Var(node.id)

    def visit_Call(self, node) -> Expression:
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return Apply(func, *args)

def expressionize(f: Callable) -> Callable:
    tree = ast.parse(inspect.getsource(f))
    f.expression = ExpressionizeNodeVisitor().visit(tree)
    return f
