# Copyright 2024 Tanner Swett.
#
# This file is part of mathdonewrong. mathdonewrong is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU GPL
# as published by the Free Software Foundation.
#
# mathdonewrong is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See version 3 of the GNU GPL for more details.

from ast import NodeVisitor
import ast
from typing import Any

from mathdonewrong.expressions import Expression, Literal, NamedOper

class PythonExpr(Expression):
    pass

class PyName(PythonExpr, NamedOper):
    pass

def PyNameL(name):
    return PyName(Literal(name))

class PyAttr(PythonExpr, NamedOper):
    pass

def PyAttrL(target, attr_name):
    return PyAttr(target, Literal(attr_name))

class PyCall(PythonExpr, NamedOper):
    pass

class PyArgs(PythonExpr, NamedOper):
    pass

def PyCallL(target, *args):
    return PyCall(target, PyArgs(*args))

class PyReturn(PythonExpr, NamedOper):
    pass

class PyBlock(PythonExpr, NamedOper):
    pass

class PyFunctionDef(PythonExpr, NamedOper):
    pass

class PyDecorators(PythonExpr, NamedOper):
    pass

def PyFunctionDefL(decorators, name, args, body):
    return PyFunctionDef(
        PyDecorators(*decorators),
        Literal(name),
        PyArgs(*args),
        PyBlock(*body))

class ExpressionizeNodeVisitor(NodeVisitor):
    def generic_visit(self, node):
        raise NotImplementedError(f"Node type {type(node).__name__} not implemented")

    def visit_arg(self, node: ast.arg) -> PythonExpr:
        return PyNameL(node.arg)

    def visit_Attribute(self, node: ast.Attribute) -> PythonExpr:
        target = self.visit(node.value)
        return PyAttrL(target, node.attr)

    def visit_Call(self, node: ast.Call) -> PythonExpr:
        target = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return PyCallL(target, *args)

    def visit_Expr(self, node: ast.Expr) -> PythonExpr:
        return self.visit(node.value)

    def visit_Expression(self, node: ast.Expression) -> PythonExpr:
        return self.visit(node.body)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> PythonExpr:
        decorators = [self.visit(decorator) for decorator in node.decorator_list]
        args = [self.visit(arg) for arg in node.args.args]
        body = [self.visit(statement) for statement in node.body]
        return PyFunctionDefL(decorators, node.name, args, body)

    def visit_Module(self, node: ast.Module) -> PythonExpr:
        statements = [self.visit(statement) for statement in node.body]
        return PyBlock(*statements)

    def visit_Name(self, node: ast.Name) -> PythonExpr:
        return PyNameL(node.id)

    def visit_Return(self, node: ast.Return) -> PythonExpr:
        return PyReturn(self.visit(node.value))

def source_expr_to_expr(source):
    tree = ast.parse(source, mode='eval')
    return ExpressionizeNodeVisitor().visit(tree)

def source_block_to_expr(source):
    tree = ast.parse(source)
    return ExpressionizeNodeVisitor().visit(tree)
