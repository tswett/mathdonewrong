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
from typing import Any, Callable

from mathdonewrong.expressions import Expression, Oper, Var
from mathdonewrong.lambda_calc.lambda_exprs import Apply, LamConst, LamVar, Lambda

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

    def generic_visit(self, node):
        raise NotImplementedError(f"Node type {type(node)} not implemented")

    # Compound statements and the like

    def visit_FunctionDef(self, node) -> Expression:
        for statement in node.body:
            expr_maybe = self.visit(statement)
            if expr_maybe is not None:
                return expr_maybe

    def visit_Module(self, node) -> Expression:
        return self.visit(node.body[0])

    # Simple statements

    def visit_Assign(self, node) -> Expression:
        target_name = node.targets[0].id
        self.locals[target_name] = self.visit(node.value)

    def visit_Return(self, node) -> Expression:
        return_expression = self.visit(node.value)
        return substitute_vars(return_expression, self.locals)

    # Expressions

    def visit_Call(self, node) -> Expression:
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return Apply(func, *args)

    def visit_Constant(self, node) -> Expression:
        return LamConst(repr(node.value))

    def visit_Lambda(self, node) -> Expression:
        param, = node.args.args
        param_name = param.arg
        body = self.visit(node.body)
        return Lambda(param_name, body)

    def visit_Name(self, node) -> Expression:
        return LamVar(node.id)

def code_to_expression(f: Callable) -> Expression:
    tree = ast.parse(inspect.getsource(f))
    return ExpressionizeNodeVisitor().visit(tree)

def expressionize(f: Callable) -> Callable:
    f.expression = code_to_expression(f)
    return f
