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

from mathdonewrong.expressions import Expression, Literal, NamedOper

class PythonExpr(Expression):
    pass

class PyName(PythonExpr, NamedOper):
    pass

def PyNameL(name):
    return PyName(Literal(name))

class PyAttr(PythonExpr, NamedOper):
    pass

def PyAttrL(target, name):
    return PyAttr(target, Literal(name))

class ExpressionizeNodeVisitor(NodeVisitor):
    def generic_visit(self, node):
        raise NotImplementedError(f"Node type {type(node).__name__} not implemented")

    def visit_Attribute(self, node: ast.Attribute) -> PythonExpr:
        target = self.visit(node.value)
        return PyAttrL(target, node.attr)

    def visit_Expression(self, node: ast.Expression) -> PythonExpr:
        return self.visit(node.body)

    def visit_Name(self, node: ast.Name) -> PythonExpr:
        return PyNameL(node.id)

def source_expr_to_expr(source):
    # Parse "source" as an expression
    tree = ast.parse(source, mode='eval')
    return ExpressionizeNodeVisitor().visit(tree)

def source_module_to_expr(source):
    pass
