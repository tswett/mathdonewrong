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

from mathdonewrong.expressions import Expression, Var

def expressionize(f: Callable) -> Callable:
    tree = ast.parse(inspect.getsource(f))
    f.expression = ExpressionizeNodeVisitor().visit(tree)
    return f

class ExpressionizeNodeVisitor(NodeVisitor):
    def visit_Module(self, node) -> Expression:
        return self.visit(node.body[0])

    def visit_FunctionDef(self, node) -> Expression:
        return self.visit(node.body[0])

    def visit_Return(self, node) -> Expression:
        return self.visit(node.value)

    def visit_Name(self, node) -> Expression:
        return Var(node.id)
